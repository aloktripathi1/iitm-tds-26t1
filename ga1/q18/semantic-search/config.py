import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AI Pipe Configuration
    AIPIPE_TOKEN = os.getenv('AIPIPE_TOKEN')
    AIPIPE_BASE_URL = os.getenv('AIPIPE_BASE_URL', 'https://aipipe.org/openai/v1')
    
    # Model Configuration
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
    RERANK_MODEL = os.getenv('RERANK_MODEL', 'gpt-4o-mini')
    
    # Search Configuration
    DEFAULT_K = 5
    DEFAULT_RERANK_K = 3
    
    # File Paths
    DATA_PATH = 'data/api_docs.json'
    EMBEDDINGS_CACHE = 'cache/embeddings.pkl'
    
    # Performance
    MAX_CONTENT_LENGTH = 500  # Characters for re-ranking
    EMBEDDING_BATCH_SIZE = 100