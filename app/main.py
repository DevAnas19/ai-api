from fastapi import FastAPI
from app.config import APP_NAME, APP_VERSION
from app.routes.summarize import router as summarize_router
from app.routes.translate import router as translate_router
from app.routes.email_gen import router as email_router
from app.exceptions import register_exception_handlers

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered API for summarization, translation, and email generation"
)

app.include_router(summarize_router, tags=["Summarize"])
app.include_router(translate_router, tags=["Translate"])
app.include_router(email_router, tags=["Email"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {APP_NAME}", "version": APP_VERSION}