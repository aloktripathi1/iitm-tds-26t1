"""
AI Security: Input Validation and Output Sanitization
Detects spam and validates content with confidence scoring.
"""
import re
import time
import html
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# Set up logging for monitoring blocked attempts
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Security Validation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ValidationRequest(BaseModel):
    userId: str
    input: str
    category: str = "Content Filtering"


class ValidationResponse(BaseModel):
    blocked: bool
    reason: str
    sanitizedOutput: Optional[str] = None
    confidence: float


# Spam detection patterns
SPAM_PATTERNS = [
    # Promotional content
    r'\b(free|win|winner|prize|discount|offer|deal|sale|buy now|click here|limited time)\b',
    # Link spam patterns
    r'(https?://\S+){3,}',  # Multiple URLs
    r'\b(www\.\S+\.\S+){2,}',  # Multiple websites
    # Common spam phrases
    r'\b(make money|earn cash|work from home|get rich|million dollars|lottery|congratulations you)\b',
    # Urgency phrases
    r'\b(act now|urgent|immediately|limited offer|expires soon|don\'t miss)\b',
]

# Keywords commonly found in spam
SPAM_KEYWORDS = [
    'viagra', 'casino', 'lottery', 'bitcoin', 'crypto', 'investment opportunity',
    'nigerian prince', 'inheritance', 'wire transfer', 'unsubscribe', 'opt out',
    'bulk email', 'mass email', 'special promotion', 'exclusive offer'
]


def calculate_repetition_score(text: str) -> float:
    """Calculate how repetitive the text is (0.0 to 1.0)."""
    if not text or len(text) < 10:
        return 0.0
    
    words = text.lower().split()
    if len(words) < 3:
        return 0.0
    
    # Check for repeated words
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Calculate ratio of repeated words
    repeated_count = sum(1 for count in word_counts.values() if count > 2)
    repetition_ratio = repeated_count / len(word_counts) if word_counts else 0
    
    # Check for repeated phrases (bi-grams)
    bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
    bigram_counts = {}
    for bg in bigrams:
        bigram_counts[bg] = bigram_counts.get(bg, 0) + 1
    
    repeated_bigrams = sum(1 for count in bigram_counts.values() if count > 1)
    bigram_ratio = repeated_bigrams / len(bigram_counts) if bigram_counts else 0
    
    # Check for character repetition (e.g., "aaaaaa")
    char_repetition = len(re.findall(r'(.)\1{4,}', text)) / max(len(text), 1) * 10
    
    return min(1.0, repetition_ratio * 0.4 + bigram_ratio * 0.4 + char_repetition * 0.2)


def calculate_spam_pattern_score(text: str) -> float:
    """Calculate spam pattern match score (0.0 to 1.0)."""
    text_lower = text.lower()
    matches = 0
    
    # Check regex patterns
    for pattern in SPAM_PATTERNS:
        found = re.findall(pattern, text_lower, re.IGNORECASE)
        matches += len(found) if found else 0
    
    # Check keyword presence
    for keyword in SPAM_KEYWORDS:
        if keyword.lower() in text_lower:
            matches += 2  # Keywords are strong indicators
    
    # High score if multiple spam indicators found
    # 2 matches = 0.4, 3 matches = 0.6, 4+ matches = 0.8+
    if matches >= 4:
        return min(1.0, 0.8 + (matches - 4) * 0.05)
    elif matches >= 2:
        return matches * 0.2
    else:
        return matches * 0.1


def calculate_link_spam_score(text: str) -> float:
    """Calculate link spam score (0.0 to 1.0)."""
    # Count URLs
    url_count = len(re.findall(r'https?://\S+', text))
    # Count email addresses
    email_count = len(re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text))
    
    # High link density is suspicious
    word_count = len(text.split())
    if word_count == 0:
        return 0.0
    
    link_density = (url_count + email_count) / word_count
    
    if url_count > 3 or link_density > 0.2:
        return min(1.0, link_density * 5 + url_count * 0.15)
    
    return min(1.0, link_density * 2)


def calculate_spam_intent_score(text: str) -> float:
    """Detect if the input is requesting/describing spam content generation (0.0 to 1.0)."""
    text_lower = text.lower().strip()
    
    # Phrases that describe spam types or request spam generation
    spam_intent_phrases = [
        'repetitive text', 'repetitive content', 'repeat text',
        'spam content', 'spam text', 'spam message', 'generate spam',
        'promotional content', 'promotional text', 'promotional material',
        'link spam', 'bulk message', 'bulk email', 'mass message',
        'junk content', 'junk text', 'junk mail',
        'unsolicited', 'flood message', 'copy paste',
    ]
    
    # Check for spam-intent phrases
    matched = 0
    for phrase in spam_intent_phrases:
        if phrase in text_lower:
            matched += 1
    
    if matched >= 1:
        return min(1.0, 0.8 + matched * 0.1)
    
    return 0.0


def detect_spam(text: str) -> tuple[bool, float, str]:
    """
    Detect if text is spam.
    Returns (is_spam, confidence, reason)
    """
    if not text or not text.strip():
        return False, 0.0, "Empty input"
    
    # Calculate individual scores
    repetition_score = calculate_repetition_score(text)
    pattern_score = calculate_spam_pattern_score(text)
    link_score = calculate_link_spam_score(text)
    intent_score = calculate_spam_intent_score(text)
    
    # Use the maximum score as the primary indicator
    # If any single factor is very strong, it's likely spam
    max_score = max(repetition_score, pattern_score, link_score, intent_score)
    
    # Weighted combination for the final confidence
    weighted_confidence = (
        repetition_score * 0.20 +
        pattern_score * 0.35 +
        link_score * 0.20 +
        intent_score * 0.25
    )
    
    # Use the higher of max_score and weighted to catch obvious spam
    confidence = max(max_score * 0.90, weighted_confidence)
    
    # Determine primary reason
    reasons = []
    if repetition_score > 0.4:
        reasons.append("repetitive text detected")
    if pattern_score > 0.4:
        reasons.append("promotional/spam patterns detected")
    if link_score > 0.4:
        reasons.append("excessive links detected")
    if intent_score > 0.4:
        reasons.append("spam content intent detected")
    
    # Threshold check
    THRESHOLD = 0.7
    is_blocked = confidence > THRESHOLD
    
    if is_blocked:
        reason = f"Spam detected: {', '.join(reasons) if reasons else 'multiple spam indicators'}"
    else:
        reason = "Input passed all security checks"
    
    return is_blocked, confidence, reason


def sanitize_output(text: str) -> str:
    """Sanitize text to prevent XSS and other injection attacks."""
    # HTML escape
    sanitized = html.escape(text)
    
    # Remove potential script injection
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove event handlers
    sanitized = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized


@app.post("/", response_model=ValidationResponse)
@app.post("/validate", response_model=ValidationResponse)
async def validate_input(request: ValidationRequest):
    """
    Validate user input for spam and security issues.
    
    Accepts:
    - userId: User identifier for logging
    - input: The text to validate
    - category: Type of validation (default: Content Filtering)
    
    Returns:
    - blocked: Whether the content was blocked
    - reason: Explanation of the decision
    - sanitizedOutput: Cleaned content (if not blocked)
    - confidence: Confidence score of the classification
    """
    try:
        # Input validation
        if not request.input:
            return ValidationResponse(
                blocked=False,
                reason="Empty input",
                sanitizedOutput="",
                confidence=0.0
            )
        
        # Detect spam
        is_blocked, confidence, reason = detect_spam(request.input)
        
        # Log if blocked
        if is_blocked:
            logger.warning(
                f"BLOCKED - userId: {request.userId}, "
                f"confidence: {confidence:.2f}, "
                f"reason: {reason}, "
                f"input_preview: {request.input[:100]}..."
            )
        
        # Sanitize output if not blocked
        sanitized = sanitize_output(request.input) if not is_blocked else None
        
        return ValidationResponse(
            blocked=is_blocked,
            reason=reason,
            sanitizedOutput=sanitized,
            confidence=round(confidence, 2)
        )
        
    except Exception as e:
        logger.error(f"Validation error for userId {request.userId}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Validation error occurred"
        )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Security Validation API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
