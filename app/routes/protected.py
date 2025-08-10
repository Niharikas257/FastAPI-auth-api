from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import User

router = APIRouter()


@router.get("/profile")
def read_profile(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
