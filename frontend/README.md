# Frontend ICEIBank

Interface web em HTML, CSS e JavaScript puro (sem framework) que consome a API das agências.

## Como rodar

Com pelo menos uma agência já rodando (veja [../agencia/README.md](../agencia/README.md)), sirva esta pasta com um servidor estático simples:

```powershell
cd frontend
python -m http.server 8080
```

Depois abra `http://localhost:8080/index.html` no navegador.

## Uso

1. Na tela de login, escolha a agência (porta de entrada) e entre com o usuário de demonstração (`aluno` / `1234`).
2. No painel, é possível consultar saldo, depositar, sacar, transferir (local ou entre agências) e ver o histórico de eventos de uma conta.
3. O token fica salvo no navegador (`localStorage`); se expirar, o sistema avisa e volta para a tela de login.
