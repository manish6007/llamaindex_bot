from fastapi import APIRouter
from backend.models.schemas import ChartDataResponse
import pandas as pd

router = APIRouter()

@router.get("/data", response_model=ChartDataResponse)
def get_chart_data():
    df = pd.read_csv("llamaIndex/inventory_data.csv")
    # Example: return summary stats for charting
    summary = df.describe().to_dict()
    return ChartDataResponse(summary=summary)
