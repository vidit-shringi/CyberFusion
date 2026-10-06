from fastapi import APIRouter, Depends
from backend.pqc.benchmark import benchmark_liboqs
from backend.services.security import get_current_user
router = APIRouter(prefix="/api/pqc", tags=["pqc"])
@router.get("/benchmark")
def benchmark(user=Depends(get_current_user)):
    return {"module":"Experimental / Research Module","results":benchmark_liboqs()}
