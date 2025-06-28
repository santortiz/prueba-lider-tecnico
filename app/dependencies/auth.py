from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.auth import decode_token
from app.schemas.token import TokenData

# Define el esquema HTTP Bearer
security = HTTPBearer()

# Extrae y valida el token JWT
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return TokenData(role=payload["role"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Middleware para requerir un rol específico
def require_role(required_role: str):
    def role_checker(user: TokenData = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker