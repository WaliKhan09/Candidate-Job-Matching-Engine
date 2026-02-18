from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import settings

model = SentenceTransformer(settings.MODEL_NAME)

async def get_embedding(text: str) -> np.ndarray:
    return model.encode(text)
