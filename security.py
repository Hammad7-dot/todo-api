from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from supabase_client import supabase

# This is what makes the "Authorize" padlock appear in Swagger UI (/docs).
# auto_error=False so we control the exact status code + message ourselves
# instead of FastAPI's default (403 "Not authenticated") when the header
# is missing/malformed.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    The reusable guard (FastAPI's version of middleware).
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Access token required")

    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
    except Exception:
        # Supabase's client raises on an invalid/expired/tampered token
        # rather than returning None — treat any failure the same way.
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if response is None or response.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Attach the token too, in case a route needs it (e.g. sign-out)
    user = response.user
    user_dict = {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at),
        "token": token,
    }
    return user_dict
