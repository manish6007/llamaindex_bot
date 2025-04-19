from fastapi import APIRouter, Query
from backend.models.schemas import KnowledgebaseSearchResponse

router = APIRouter()

@router.get("/search", response_model=KnowledgebaseSearchResponse)
def search_knowledgebase(query: str = Query(..., description="Search query")):
    # Dummy implementation: search in a text file
    kb_path = "data/knowledgebase.txt"
    results = []
    with open(kb_path, "r", encoding="utf-8") as f:
        for line in f:
            if query.lower() in line.lower():
                results.append(line.strip())
    return KnowledgebaseSearchResponse(results=results)
