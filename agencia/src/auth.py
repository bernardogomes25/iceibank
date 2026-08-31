from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Header, HTTPException

import config


def criar_token(usuario: str) -> str:
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRACAO_MINUTOS)
    payload = {"sub": usuario, "exp": expira_em}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITMO)


def exigir_token(authorization: str = Header(default=None)) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token nao informado.")

    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITMO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido.")

    return payload["sub"]
