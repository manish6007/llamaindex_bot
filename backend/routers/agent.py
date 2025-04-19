from fastapi import APIRouter, HTTPException
from backend.models.schemas import AgentQueryRequest, AgentQueryResponse, AgentFeedbackRequest, AgentFeedbackResponse
from agent.agent import BedrockAgent
from core.logger import get_application_logger
from typing import Dict
from pydantic import BaseModel

router = APIRouter()

# Global session memory for agents
session_agents: Dict[str, BedrockAgent] = {}

def get_agent_for_session(session_id: str):
    if session_id not in session_agents:
        logger = get_application_logger()
        session_agents[session_id] = BedrockAgent(logger)
    return session_agents[session_id]

@router.get("/ping")
def ping():
    return {"message": "Agent service is alive."}

class AgentQueryRequestWithSession(AgentQueryRequest):
    session_id: str

@router.post("/query", response_model=AgentQueryResponse)
def query_agent(request: AgentQueryRequestWithSession):
    try:
        agent = get_agent_for_session(request.session_id)
        # Use generate_response for memory/context
        response = agent.generate_response(request.query)
        return AgentQueryResponse(success=response.get("success", False), response=response.get("response"))
    except Exception as e:
        logger = get_application_logger()
        logger.error(f"Agent query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class AgentFeedbackRequestWithSession(AgentFeedbackRequest):
    session_id: str

@router.post("/feedback", response_model=AgentFeedbackResponse)
def submit_feedback(request: AgentFeedbackRequestWithSession):
    # Optionally, you can access the agent for the session if needed
    # agent = get_agent_for_session(request.session_id)
    return AgentFeedbackResponse(success=True, message="Feedback received.")
