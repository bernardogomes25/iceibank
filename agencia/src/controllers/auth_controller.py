from fastapi import APIRouter, HTTPException

import config
from auth import criar_token
from schemas import LoginBody

router = APIRouter()


@router.post("/auth/login")
def login(body: LoginBody):
    if body.usuario != config.USUARIO_DEMO or body.senha != config.SENHA_DEMO:
        raise HTTPException(status_code=401, detail="Usuario ou senha invalidos.")
    return {"token": criar_token(body.usuario)}
