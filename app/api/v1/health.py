from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
)
async def get():
    return {"ok": True}
