from fastapi import FastAPI
from app.routers.health import router
import uvicorn

app = FastAPI(
    title="Closira Backend API",
    description="Backend service for enquiry handling, SOP matching, follow-ups, and escalations.",
    version="1.0.0",
)


app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        reload= True
    )