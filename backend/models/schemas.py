from pydantic import BaseModel
from typing import List, Dict, Any

class AgentQueryRequest(BaseModel):
    query: str

class AgentQueryResponse(BaseModel):
    success: bool
    response: Any  # Accepts dict, str, etc.

class AgentFeedbackRequest(BaseModel):
    response_id: str
    feedback: str
    rating: int

class AgentFeedbackResponse(BaseModel):
    success: bool
    message: str

class KnowledgebaseSearchResponse(BaseModel):
    results: List[str]

class InventoryResponse(BaseModel):
    data: List[Dict[str, Any]]

class ChartDataResponse(BaseModel):
    summary: Dict[str, Any]
