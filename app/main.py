from pathlib import Path
from fastapi import FastAPI

app = FastAPI()


def get_version():
    version_file = Path("/code/version.txt")

    if version_file.exists():
        return version_file.read_text().strip()

    return "unknown"


@app.get("/version")
async def version():
    return {"version": get_version()}
