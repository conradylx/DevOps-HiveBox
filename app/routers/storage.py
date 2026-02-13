from fastapi import APIRouter, HTTPException
from app.services.minio_storage import store_temperature_data
from app.services.opensensemap import (
    fetch_temperature_data,
    calculate_average_temperature,
    get_temperature_status,
)

router = APIRouter(tags=["storage"])


@router.get("/store")
async def manual_store():
    """Manually trigger store to MinIO"""
    try:
        temp_data = await fetch_temperature_data()
        avg_temp = calculate_average_temperature(temperature_data=temp_data)
        result = {
            "average_temperature": avg_temp,
            "status": get_temperature_status(avg_temp),
            "samples": len(temp_data),
        }
        success = await store_temperature_data(result)
        if not success:
            raise HTTPException(status_code=503, detail="Storage failed")
        return {"message": "Data stored successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
