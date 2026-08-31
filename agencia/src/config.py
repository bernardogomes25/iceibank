OFFSET = 36  # dois ultimos digitos da matricula

NUMERO_AGENCIAS = 3
PORTA_BASE = 4000 + OFFSET

AGENCIAS = [
    {"id": 0, "url": f"http://localhost:{PORTA_BASE}"},
    {"id": 1, "url": f"http://localhost:{PORTA_BASE + 1}"},
    {"id": 2, "url": f"http://localhost:{PORTA_BASE + 2}"},
]


def agencia_responsavel(id_conta: int) -> int:
    return id_conta % NUMERO_AGENCIAS


def url_da_agencia(id_agencia: int) -> str:
    return next(a["url"] for a in AGENCIAS if a["id"] == id_agencia)


JWT_SECRET = "iceibank-sprint1-segredo-de-desenvolvimento"
JWT_ALGORITMO = "HS256"
JWT_EXPIRACAO_MINUTOS = 15

USUARIO_DEMO = "aluno"
SENHA_DEMO = "1234"
