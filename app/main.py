from pathlib import Path

from fastapi import FastAPI

from app.api import api_root


ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path(__file__).resolve().parent


app = FastAPI(title="ContractRegistry")
app.include_router(api_root.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
