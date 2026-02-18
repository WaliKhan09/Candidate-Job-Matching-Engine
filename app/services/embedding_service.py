from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import settings

# This is our AI model. We load it once when the app starts.
# It is like a big dictionary that turns words into lists of numbers.
model = SentenceTransformer(settings.MODEL_NAME)

async def get_embedding(text: str) -> np.ndarray:
    """
    This simple function takes text and turns it into a list of numbers (an embedding).
    """
    # model.encode() does the heavy lifting
    return model.encode(text)
