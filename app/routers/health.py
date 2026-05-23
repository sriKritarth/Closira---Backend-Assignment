from fastapi import APIRouter
from app.database import get_connection


router = APIRouter()

@router.get("/health")
async def check_health():
    try :
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()

        return {
            "api" : "ok",
            "database" : "Connected"
        }

    except Exception:
        
        return {
            "api" : "ok",
            "database" : "Not Connected"
        }
        





        
    