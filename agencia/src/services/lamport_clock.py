class RelogioLamport:
    def __init__(self):
        self.contador = 0

    def evento_local(self) -> int:
        self.contador += 1
        return self.contador

    def ao_enviar(self) -> int:
        self.contador += 1
        return self.contador

    def ao_receber(self, timestamp_recebido: int) -> int:
        self.contador = max(self.contador, timestamp_recebido) + 1
        return self.contador
