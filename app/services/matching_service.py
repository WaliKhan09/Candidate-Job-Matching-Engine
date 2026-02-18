import faiss
import numpy as np
from typing import List, Dict, Any
from app.services.embedding_service import get_embedding
from app.config import settings
from app.models.models import Candidate

dimension = 384

index = faiss.IndexFlatIP(dimension)

id_map = []

def add_candidate_to_index(embedding: np.ndarray, candidate_id: int):
    faiss.normalize_L2(embedding.reshape(1, -1))
    index.add(embedding.reshape(1, -1))
    id_map.append(candidate_id)

def rehydrate_index(db_session: Any):
    global id_map, index
    
    index = faiss.IndexFlatIP(dimension)
    id_map = []
    
    candidates = db_session.query(Candidate).all()
    print(f"Re-hydrating search index with {len(candidates)} candidates from Database...")
    
    for person in candidates:
        if person.embedding_vector:
            vector = np.array(person.embedding_vector, dtype='float32')
            add_candidate_to_index(vector, person.id)

async def find_matches(job_description: str, db_session: Any) -> List[Dict[str, Any]]:
    # 1. Turn the Job Description into numbers (Embeddings)
    job_vector = await get_embedding(job_description)
    faiss.normalize_L2(job_vector.reshape(1, -1))

    # 2. Ask FAISS: "Who is most similar to these numbers?"
    num_to_search = max(index.ntotal, 1)
    distances, indices = index.search(job_vector.reshape(1, -1), num_to_search)

    matches = []
    for i in range(len(indices[0])):
        pos = indices[0][i]
        
        if pos == -1: 
            continue
        
        database_id = id_map[pos]
        similarity_score = float(distances[0][i])
        
        candidate = db_session.query(Candidate).filter(Candidate.id == database_id).first()
        
        if candidate:
            matches.append({
                "candidateId": str(candidate.id),
                "similarityScore": similarity_score,
                "experience": candidate.experience
            })

    matches.sort(key=lambda x: (x["similarityScore"], x["experience"]), reverse=True)

    # 3. Return the Top 5 results only
    return matches[:5]
