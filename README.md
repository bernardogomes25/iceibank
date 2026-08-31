# ICEIBank

Projeto da disciplina de Laboratório de Desenvolvimento de Aplicações Móveis e Distribuídas (PUC Minas).

Um banco simplificado dividido em agências, onde cada agência é um serviço independente responsável por uma partição de contas. O projeto evolui em 4 sprints ao longo do semestre; este repositório contém a implementação de cada etapa.

## Sprint 1 — API REST/MVC com relógio de Lamport

Detalhes completos do que essa etapa exige estão em [ROTEIRO.md](ROTEIRO.md). Resumo do que foi implementado:

- Backend em Python (FastAPI), executado 3 vezes com identidades diferentes para simular 3 agências
- Particionamento de contas entre as agências (`id_conta % 3`)
- CRUD de contas, depósito e saque, cada operação registrada com relógio lógico de Lamport
- Transferência entre contas da mesma agência e entre agências diferentes
- Script para juntar os logs das 3 agências em uma linha do tempo única, ordenada por Lamport
- Autenticação via JWT protegendo as rotas da API
- Frontend simples (HTML/CSS/JS) que consome a API autenticada

## Como rodar

Instruções detalhadas de instalação e execução estão em [agencia/README.md](agencia/README.md) e [frontend/README.md](frontend/README.md).

As respostas das perguntas de cada parte do roteiro estão em [RESPOSTAS.md](RESPOSTAS.md).
