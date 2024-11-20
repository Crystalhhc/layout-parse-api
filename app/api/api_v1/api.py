from fastapi import APIRouter
from .endpoints import parse_layout

router = APIRouter()
router.include_router(parse_layout.router, prefix='/parse-layout', tags=['lp'])
