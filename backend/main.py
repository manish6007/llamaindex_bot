from fastapi import FastAPI
from backend.routers import agent, s3, knowledgebase, inventory, chart

app = FastAPI(title="Clearwater Post Trade Data API")

# Include routers
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(s3.router, prefix="/s3", tags=["S3"])
app.include_router(knowledgebase.router, prefix="/knowledgebase", tags=["Knowledgebase"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(chart.router, prefix="/chart", tags=["Chart"])

@app.get("/")
def root():
    return {"message": "Clearwater Post Trade Data API is running."}
