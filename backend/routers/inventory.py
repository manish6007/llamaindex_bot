from fastapi import APIRouter
from backend.models.schemas import InventoryResponse
import pandas as pd

router = APIRouter()

@router.get("/", response_model=InventoryResponse)
def get_inventory():
    df = pd.read_csv("llamaIndex/inventory_data.csv")
    data = df.to_dict(orient="records")
    return InventoryResponse(data=data)
