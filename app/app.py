from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config.config import settings


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
)

# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/status")
def get_status():
    return {"status": "OK"}

# app.include_router(router)
