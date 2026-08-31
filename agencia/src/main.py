import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from services.lamport_clock import RelogioLamport
from services.event_log import RegistroEventos
from controllers import auth_controller, contas_controller, transferencias_controller

id_agencia = int(os.environ.get("AGENCIA_ID", "0"))
agencia_config = next((a for a in config.AGENCIAS if a["id"] == id_agencia), None)

if agencia_config is None:
    raise SystemExit(f"Agencia {id_agencia} nao configurada em config.py")

app = FastAPI(title=f"ICEIBank - Agencia {id_agencia}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.id_agencia = id_agencia
app.state.relogio = RelogioLamport()
app.state.registro = RegistroEventos(f"agencia-{id_agencia}")
app.state.contas = {}

app.include_router(auth_controller.router)
app.include_router(contas_controller.router)
app.include_router(transferencias_controller.router)

if __name__ == "__main__":
    import uvicorn

    porta = int(agencia_config["url"].rsplit(":", 1)[1])
    print(f"[Agencia {id_agencia}] ouvindo na porta {porta}")
    uvicorn.run(app, host="0.0.0.0", port=porta)
