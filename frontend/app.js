function pegarAgencia() {
  return localStorage.getItem("agenciaUrl") || "http://localhost:4036";
}

function pegarToken() {
  return localStorage.getItem("token");
}

function estaLogado() {
  return Boolean(pegarToken());
}

function sair() {
  localStorage.removeItem("token");
  localStorage.removeItem("agenciaUrl");
  window.location.href = "index.html";
}

async function chamarApi(caminho, opcoes = {}) {
  const resposta = await fetch(pegarAgencia() + caminho, {
    ...opcoes,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + pegarToken(),
      ...opcoes.headers,
    },
  });

  if (resposta.status === 401) {
    sair();
    throw new Error("Sessao expirada. Faca login novamente.");
  }

  const dados = await resposta.json();
  if (!resposta.ok) {
    throw new Error(dados.detail || "Erro na requisicao.");
  }
  return dados;
}
