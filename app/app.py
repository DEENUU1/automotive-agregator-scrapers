from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config.config import settings
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
)

# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/status")
def get_status():
    return {"status": "OK"}

# app.include_router(router)
