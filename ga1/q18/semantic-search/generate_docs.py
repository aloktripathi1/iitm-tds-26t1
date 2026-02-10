import json

# Base topics for technical documentation
topics = [
    "authentication", "authorization", "API keys", "OAuth", "JWT tokens",
    "rate limiting", "throttling", "error handling", "status codes", "webhooks",
    "pagination", "filtering", "sorting", "searching", "caching",
    "versioning", "deprecation", "migration", "SDK usage", "client libraries",
    "data formats", "JSON", "XML", "CSV", "encoding",
    "HTTP methods", "GET", "POST", "PUT", "DELETE", "PATCH",
    "headers", "request format", "response format", "content types",
    "security", "HTTPS", "encryption", "SSL/TLS", "CORS",
    "batch operations", "bulk processing", "async requests", "callbacks",
    "monitoring", "logging", "debugging", "testing", "troubleshooting",
    "performance", "optimization", "best practices", "guidelines",
    "data validation", "input sanitization", "output formatting",
    "user management", "permissions", "roles", "access control",
    "file upload", "file download", "streaming", "chunked transfer",
    "internationalization", "localization", "timezones", "date formats",
    "export", "import", "backup", "restore", "archiving"
]

docs = []

for i in range(124):
    topic = topics[i % len(topics)]
    doc_num = i // len(topics) + 1
    
    docs.append({
        "id": i,
        "title": f"{topic.title()} Documentation - Part {doc_num}",
        "content": f"Comprehensive guide to {topic} in our API. This section covers {topic} implementation, best practices, common patterns, and troubleshooting. Learn how to effectively use {topic} in your applications. Includes code examples, security considerations, and performance tips for {topic}. Updated with the latest features and recommendations for {topic} usage.",
        "source": f"docs/{topic.replace(' ', '_')}_part{doc_num}.md"
    })

with open('data/api_docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print(f"✓ Generated {len(docs)} documents")