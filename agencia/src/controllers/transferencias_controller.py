import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

import config
from auth import criar_token, exigir_token
from schemas import CreditarRemotoBody, TransferenciaBody

router = APIRouter(dependencies=[Depends(exigir_token)])


@router.post("/transferencias")
async def transferir(body: TransferenciaBody, request: Request):
    contas = request.app.state.contas
    relogio = request.app.state.relogio
    registro = request.app.state.registro
    id_agencia = request.app.state.id_agencia

    conta_origem = contas.get(body.idOrigem)
    if conta_origem is None:
        raise HTTPException(status_code=404, detail="Conta de origem nao encontrada nesta agencia.")
    if conta_origem["saldo"] < body.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente.")

    agencia_destino = config.agencia_responsavel(body.idDestino)

    ts_debito = relogio.evento_local()
    conta_origem["saldo"] -= body.valor
    registro.registrar(
        "TRANSFERENCIA_DEBITO",
        ts_debito,
        {"idOrigem": body.idOrigem, "idDestino": body.idDestino, "valor": body.valor},
    )

    if agencia_destino == id_agencia:
        conta_destino = contas.get(body.idDestino)
        if conta_destino is None:
            conta_origem["saldo"] += body.valor
            raise HTTPException(status_code=404, detail="Conta de destino nao encontrada.")
        ts_credito = relogio.evento_local()
        conta_destino["saldo"] += body.valor
        registro.registrar(
            "TRANSFERENCIA_CREDITO",
            ts_credito,
            {"idOrigem": body.idOrigem, "idDestino": body.idDestino, "valor": body.valor},
        )
        return {"mensagem": "Transferencia concluida (mesma agencia)."}

    ts_envio = relogio.ao_enviar()
    url_destino = config.url_da_agencia(agencia_destino)

    try:
        async with httpx.AsyncClient() as client:
            resposta = await client.post(
                f"{url_destino}/contas/{body.idDestino}/creditar-remoto",
                json={
                    "valor": body.valor,
                    "timestampLamport": ts_envio,
                    "origemAgencia": id_agencia,
                },
                headers={"Authorization": f"Bearer {criar_token(config.USUARIO_DEMO)}"},
                timeout=5,
            )
            resposta.raise_for_status()
        return {"mensagem": "Transferencia concluida (entre agencias)."}
    except httpx.HTTPError as erro:
        # limitacao conhecida deste sprint: o debito acima nao e desfeito se a chamada falhar
        registro.registrar(
            "TRANSFERENCIA_FALHOU",
            relogio.evento_local(),
            {"idOrigem": body.idOrigem, "idDestino": body.idDestino, "valor": body.valor, "erro": str(erro)},
        )
        raise HTTPException(
            status_code=502,
            detail="Falha ao contatar agencia de destino. Debito ja aplicado - inconsistencia conhecida (ver Sprint 4).",
        )


@router.post("/contas/{id_conta}/creditar-remoto")
def creditar_remoto(id_conta: int, body: CreditarRemotoBody, request: Request):
    contas = request.app.state.contas
    relogio = request.app.state.relogio
    registro = request.app.state.registro

    ts = relogio.ao_receber(body.timestampLamport)

    conta = contas.get(id_conta)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta nao encontrada nesta agencia.")

    conta["saldo"] += body.valor
    registro.registrar(
        "TRANSFERENCIA_CREDITO_REMOTO",
        ts,
        {"idConta": id_conta, "valor": body.valor, "origemAgencia": body.origemAgencia},
    )

    return {"mensagem": "Credito remoto aplicado.", "saldoAtual": conta["saldo"]}
