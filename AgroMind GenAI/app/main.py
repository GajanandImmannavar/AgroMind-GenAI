from fastapi import FastAPI
from app.api.whatsapp_webhook import router
from app.utils.database import init_db

app = FastAPI()

init_db()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "AgroMind AI WhatsApp Server Running"}