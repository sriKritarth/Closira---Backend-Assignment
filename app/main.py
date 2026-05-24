from fastapi import FastAPI
from app.routers.health import router
from app.database import init_db
from app.routers.enquiry import router_enquiry
import uvicorn

app = FastAPI(
    title="Closira Backend API",
    description="Backend service for enquiry handling, SOP matching, follow-ups, and escalations.",
    version="1.0.0",
)

#intialize database
init_db()

app.include_router(router=router)
app.include_router(router=router_enquiry)


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        reload= True
    )