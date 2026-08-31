from pydantic import BaseModel


class CriarContaBody(BaseModel):
    id: int
    nomeAluno: str
    saldoInicial: float = 0


class ValorBody(BaseModel):
    valor: float
