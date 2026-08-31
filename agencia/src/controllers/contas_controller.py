from fastapi import APIRouter, HTTPException, Request

import config
from schemas import CriarContaBody, ValorBody

router = APIRouter()


@router.post("/contas", status_code=201)
def criar_conta(body: CriarContaBody, request: Request):
    contas = request.app.state.contas
    relogio = request.app.state.relogio
    registro = request.app.state.registro
    id_agencia = request.app.state.id_agencia

    if config.agencia_responsavel(body.id) != id_agencia:
        raise HTTPException(status_code=400, detail=f"Conta {body.id} nao pertence a esta agencia.")
    if body.id in contas:
        raise HTTPException(status_code=409, detail="Conta ja existe.")

    ts = relogio.evento_local()
    contas[body.id] = {"id": body.id, "nomeAluno": body.nomeAluno, "saldo": body.saldoInicial}
    registro.registrar(
        "CRIAR_CONTA", ts, {"id": body.id, "nomeAluno": body.nomeAluno, "saldoInicial": body.saldoInicial}
    )

    return contas[body.id]


@router.get("/contas/{id_conta}")
def consultar_saldo(id_conta: int, request: Request):
    conta = request.app.state.contas.get(id_conta)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta nao encontrada nesta agencia.")
    return conta


@router.post("/contas/{id_conta}/depositar")
def depositar(id_conta: int, body: ValorBody, request: Request):
    contas = request.app.state.contas
    relogio = request.app.state.relogio
    registro = request.app.state.registro

    conta = contas.get(id_conta)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta nao encontrada nesta agencia.")

    ts = relogio.evento_local()
    conta["saldo"] += body.valor
    registro.registrar("DEPOSITO", ts, {"id": id_conta, "valor": body.valor, "novoSaldo": conta["saldo"]})

    return conta


@router.post("/contas/{id_conta}/sacar")
def sacar(id_conta: int, body: ValorBody, request: Request):
    contas = request.app.state.contas
    relogio = request.app.state.relogio
    registro = request.app.state.registro

    conta = contas.get(id_conta)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta nao encontrada nesta agencia.")
    if conta["saldo"] < body.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente.")

    ts = relogio.evento_local()
    conta["saldo"] -= body.valor
    registro.registrar("SAQUE", ts, {"id": id_conta, "valor": body.valor, "novoSaldo": conta["saldo"]})

    return conta
