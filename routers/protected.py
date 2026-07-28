from fastapi import APIRouter, Depends

from security import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
    }


@router.get("/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
    """
    A second protected route reusing the exact same dependency —
    proves the guard generalizes with zero new auth code.
    """
    return {"message": f"Welcome to your dashboard, {current_user['email']}!"}
