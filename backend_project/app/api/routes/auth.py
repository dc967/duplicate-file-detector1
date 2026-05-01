from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.core.dependencies import get_current_user
import secrets

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _is_bcrypt_hash(value: str) -> bool:
    return value.startswith("$2a$") or value.startswith("$2b$") or value.startswith("$2y$")


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):


    if request.email != settings.ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password!"
        )

    stored_password = settings.ADMIN_PASSWORD
    if _is_bcrypt_hash(stored_password):
        password_ok = verify_password(request.password, stored_password)
    else:
        # Backward compatibility for plain-text env values.
        password_ok = secrets.compare_digest(request.password, stored_password)

    if not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password!"
        )

    access_token = create_access_token(data={"email": request.email})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            email=settings.ADMIN_EMAIL,
            name="Admin",
            role="admin"
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Current user ki info do"""
    return UserResponse(
        email=current_user["email"],
        name="Admin",
        role="admin"
    )
