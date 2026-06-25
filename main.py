import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from config.settings import settings

app = FastAPI(
    title="LLM Agent System",
    description="Multi-agent AI system powered by LangGraph and OpenAI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "LLM Agent System is running", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)
