from pydantic import BaseModel


class CriarContaBody(BaseModel):
    id: int
    nomeAluno: str
    saldoInicial: float = 0


class ValorBody(BaseModel):
    valor: float


class TransferenciaBody(BaseModel):
    idOrigem: int
    idDestino: int
    valor: float


class CreditarRemotoBody(BaseModel):
    valor: float
    timestampLamport: int
    origemAgencia: int


class LoginBody(BaseModel):
    usuario: str
    senha: str
