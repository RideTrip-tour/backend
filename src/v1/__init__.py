from fastapi import APIRouter

from .auth.router import router as router_auth
from .tours.router import router as router_tours

router_v1 = APIRouter()

router_v1.include_router(router_auth)
router_v1.include_router(router_tours)
