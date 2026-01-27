from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()


@router.get("/version")
async def get_version():
    """
    Get the current application version.

    Returns:
        dict: Version information
    """
    return {"version": settings.VERSION}
