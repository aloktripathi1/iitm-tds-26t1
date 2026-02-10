import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def embed(text: str) -> np.ndarray:
    np.random.seed(abs(hash(text)) % (10**8))
    return np.random.randn(1, 384)

def similarity(vec1, vec2):
    return cosine_similarity(vec1, vec2)[0][0]
