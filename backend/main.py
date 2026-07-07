from fastapi import FastAPI

from backend.routers.chat import router as chat_router


app = FastAPI(
    title="MedIntel AI",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "MedIntel AI Backend Running"
    }


app.include_router(chat_router)