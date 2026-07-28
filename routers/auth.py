from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from supabase_client import supabase
from security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class Credentials(BaseModel):
    # Optional at the schema level so a missing field produces our own
    # 400 + JSON error, instead of FastAPI/Pydantic's automatic 422.
    email: Optional[str] = None
    password: Optional[str] = None


@router.post("/signup", status_code=201)
def signup(credentials: Credentials):
    """
    Create a new user account. Supabase hashes and stores the password —
    this code never touches it directly.
    """
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        result = supabase.auth.sign_up(
            {"email": credentials.email, "password": credentials.password}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if result.user is None:
        raise HTTPException(status_code=400, detail="Sign up failed")

    return {
        "user": {
            "id": result.user.id,
            "email": result.user.email,
            "created_at": str(result.user.created_at),
        }
    }


@router.post("/login")
def login(credentials: Credentials):
    """
    Authenticate against Supabase and return the access + refresh tokens.
    """
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        result = supabase.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    if result.session is None:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token,
        "user": {"id": result.user.id, "email": result.user.email},
    }


@router.post("/logout", status_code=204)
def logout(current_user: dict = Depends(get_current_user)):
    """
    Protected route — ends the user's session via Supabase.
    """
    try:
        supabase.auth.sign_out()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None
