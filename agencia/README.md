# Agência ICEIBank

API REST de uma agência do ICEIBank. O mesmo código roda 3 vezes, cada vez com um `AGENCIA_ID` diferente, simulando as 3 agências do banco.

## Instalação

```powershell
cd agencia
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Rodando as 3 agências

Abra 3 terminais:

```powershell
# Terminal 1
$env:AGENCIA_ID=0; .venv\Scripts\python src\main.py

# Terminal 2
$env:AGENCIA_ID=1; .venv\Scripts\python src\main.py

# Terminal 3
$env:AGENCIA_ID=2; .venv\Scripts\python src\main.py
```

As portas usadas estão em `src/config.py` (4036, 4037, 4038 - já com o OFFSET da matrícula aplicado).

## Testando os endpoints

Todas as rotas de conta e transferência exigem login antes:

```powershell
$login = Invoke-RestMethod -Uri "http://localhost:4036/auth/login" -Method Post -ContentType "application/json" -Body '{"usuario":"aluno","senha":"1234"}'
$headers = @{ Authorization = "Bearer $($login.token)" }

Invoke-RestMethod -Uri "http://localhost:4036/contas" -Method Post -ContentType "application/json" -Headers $headers -Body '{"id":0,"nomeAluno":"Ana","saldoInicial":100}'

Invoke-RestMethod -Uri "http://localhost:4036/contas/0" -Method Get -Headers $headers
```

## Linha do tempo unificada

Depois de gerar alguns eventos, rode:

```powershell
python mesclar_logs.py
```

Isso junta os logs das 3 agências (pasta `data/`) em uma única lista ordenada pelo relógio de Lamport.
