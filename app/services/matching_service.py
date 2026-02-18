import faiss
import numpy as np
from typing import List, Dict, Any
from app.services.embedding_service import get_embedding
from app.config import settings
from app.models.models import Candidate

# --- GLOBAL VARIABLES ---
# 384 is the "dimension" or size of our magic numbers (vectors)
# FAISS works with these dimensions to find similar things
dimension = 384

# This is our 'Vector Index' - imagine it as a super-fast library card catalog
index = faiss.IndexFlatIP(dimension)

# This list helps us remember which Database ID belongs to which vector in FAISS
# FAISS only knows numbers (0, 1, 2...), so we Map those to our SQL IDs (101, 102...)
id_map = []

def add_candidate_to_index(embedding: np.ndarray, candidate_id: int):
    """
    Steps to add a candidate to our fast search tool:
    1. Normalize the numbers (make them standard size)
    2. Add them to the FAISS index
    3. Save the database ID in our map
    """
    # FAISS works better when we 'normalize' vectors to length 1
    faiss.normalize_L2(embedding.reshape(1, -1))
    
    # Add to index
    index.add(embedding.reshape(1, -1))
    
    # Remember the ID
    id_map.append(candidate_id)

def rehydrate_index(db_session: Any):
    """
    This function is called when the server starts.
    It reads all candidates from our SQL database and puts them back into FAISS.
    Without this, every time the server restarts, our search engine would be empty!
    """
    global id_map, index
    
    # Reset both to start from scratch
    index = faiss.IndexFlatIP(dimension)
    id_map = []
    
    # Get everyone from the database
    candidates = db_session.query(Candidate).all()
    print(f"🔄 Re-hydrating search index with {len(candidates)} candidates from Database...")
    
    for person in candidates:
        if person.embedding_vector:
            # Convert the list we stored in SQL back into a format FAISS understands (numpy)
            vector = np.array(person.embedding_vector, dtype='float32')
            add_candidate_to_index(vector, person.id)

async def find_matches(job_description: str, db_session: Any) -> List[Dict[str, Any]]:
    """
    How we find the best candidates for a job:
    """
    # 1. Turn the Job Description into numbers (Embeddings)
    job_vector = await get_embedding(job_description)
    faiss.normalize_L2(job_vector.reshape(1, -1))

    # 2. Ask FAISS: "Who is most similar to these numbers?"
    # We ask for all candidates so we can re-rank them with experience later
    num_to_search = max(index.ntotal, 1)
    distances, indices = index.search(job_vector.reshape(1, -1), num_to_search)

    matches = []
    # indices[0] contains the positions in our id_map
    for i in range(len(indices[0])):
        pos = indices[0][i]
        
        # -1 means FAISS didn't find anyone
        if pos == -1: 
            continue
        
        # Get the database ID we saved earlier in our list
        database_id = id_map[pos]
        similarity_score = float(distances[0][i])
        
        # Search the database for the rest of the info (Name, Experience)
        candidate = db_session.query(Candidate).filter(Candidate.id == database_id).first()
        
        if candidate:
            # We build a simple dictionary for the response
            matches.append({
                "candidateId": str(candidate.id),
                "similarityScore": similarity_score,
                "experience": candidate.experience
            })

    # 3. RE-RANKING:
    # If two people have the same score, the one with more experience wins!
    # Primary sort: similarityScore (Highest first)
    # Secondary sort: experience (Highest first)
    matches.sort(key=lambda x: (x["similarityScore"], x["experience"]), reverse=True)

    # 4. Return the Top 5 results only
    return matches[:5]
