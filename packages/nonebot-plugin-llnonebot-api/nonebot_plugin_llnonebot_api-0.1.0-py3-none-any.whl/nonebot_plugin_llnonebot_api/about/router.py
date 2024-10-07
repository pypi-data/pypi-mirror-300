from importlib.metadata import version

from fastapi import APIRouter

from .schema import ResponseModel

router = APIRouter(tags=["About"])


@router.get("/about", response_model=ResponseModel)
async def _get_about() -> ResponseModel:
    return ResponseModel(version=version("nonebot-plugin-llnonebot-api"))
