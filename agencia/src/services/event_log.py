import json
import os
from datetime import datetime, timezone


class RegistroEventos:
    def __init__(self, nome_agencia: str):
        self.nome_agencia = nome_agencia
        pasta_servicos = os.path.dirname(os.path.abspath(__file__))
        pasta_dados = os.path.join(pasta_servicos, "..", "..", "data")
        os.makedirs(pasta_dados, exist_ok=True)
        self.caminho_arquivo = os.path.join(pasta_dados, f"eventos-{nome_agencia}.jsonl")

    def registrar(self, tipo: str, timestamp_lamport: int, detalhes: dict) -> dict:
        evento = {
            "agencia": self.nome_agencia,
            "tipo": tipo,
            "timestampLamport": timestamp_lamport,
            "horaParede": datetime.now(timezone.utc).isoformat(),
            "detalhes": detalhes,
        }
        with open(self.caminho_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
        print(f"[Lamport {timestamp_lamport}] {tipo} {detalhes}")
        return evento

    def listar(self) -> list:
        if not os.path.exists(self.caminho_arquivo):
            return []
        eventos = []
        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    eventos.append(json.loads(linha))
        return eventos
