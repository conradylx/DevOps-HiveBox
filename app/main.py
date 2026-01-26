from fastapi import FastAPI
from app.config.settings import settings
from app.routers import version, temperature

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API to track environmental sensor data for beekeepers",
)

app.include_router(version.router, tags=["version"])
app.include_router(temperature.router, tags=["temperature"])


@app.get("/")
async def root():
    """Root endpoint - returns version."""
    return {"version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
