# Respostas - Sprint 1: ICEIBank

## Funcionalidade adicional (seção 2.1)

_Preencher na Parte extra._

## Parte B - Relógio de Lamport (seção 6.4)

**1. Por que usar `max(contador_local, timestampRecebido) + 1` em vez de simplesmente adotar o timestamp recebido?**

Porque o relógio de Lamport precisa ser sempre crescente para cada processo, e adotar direto o valor recebido poderia até fazer o contador andar para trás. Se a agência que está recebendo já processou mais eventos do que a que enviou a mensagem, o timestamp recebido pode ser menor que o contador atual - nesse caso, simplesmente copiar o valor recebido quebraria a regra de que o tempo nunca volta atrás. Usando o `max` mais 1, o contador sempre respeita as duas condições: fica maior que o que a própria agência já tinha e maior que o evento que causou o recebimento da mensagem.

**2. Se a Agência 0 está no contador 10 e recebe uma mensagem com timestamp 3, qual o novo valor?**

O novo valor fica `max(10, 3) + 1 = 11`. Ou seja, o timestamp recebido (3) praticamente não teve efeito nenhum no cálculo, porque a Agência 0 já estava muito mais "adiantada". Isso mostra que agências que processam muitos eventos rapidamente vão sempre ter contadores mais altos, enquanto agências mais lentas ficam com contadores mais baixos - só quando uma agência lenta manda uma mensagem para uma mais rápida (ou vice-versa) é que o `max` realmente serve para sincronizar as duas.

## Parte D - Transferências (seção 8.3)

**1. Por que a transferência local não precisa de `ao_enviar`/`ao_receber`, mas a entre agências precisa?**

Porque `ao_enviar` e `ao_receber` só fazem sentido quando existe uma mensagem trocada entre dois processos diferentes. Na transferência local, o débito e o crédito acontecem dentro do mesmo processo (a mesma agência), então basta usar `evento_local()` duas vezes - não existe uma mensagem "saindo" e "chegando". Já na transferência entre agências, a agência de origem manda uma requisição HTTP para a agência de destino, e são dois processos separados, cada um com seu próprio contador. É aí que as regras 2 e 3 do relógio de Lamport entram: quem envia incrementa e manda o timestamp junto, quem recebe ajusta o contador com base nesse timestamp.

**2. O saldo foi revertido depois da falha?**

Não. Testei derrubando a agência de destino e tentando transferir para uma conta dela: a resposta foi um erro 502, mas o saldo da conta de origem já tinha sido descontado antes da tentativa de chamar a outra agência, e continuou descontado depois do erro. Isso significa que o sistema, hoje, não garante atomicidade entre agências - o dinheiro literalmente some da conta de origem sem chegar em lugar nenhum, o que numa aplicação bancária de verdade seria um problema sério.

**3. Duas formas de corrigir isso (ideia, sem implementar agora):**

Uma opção é usar duas fases (2PC): antes de aplicar qualquer débito, a agência de origem pergunta para a de destino se ela está pronta para receber o valor, e só executa o débito de fato depois que as duas confirmarem que conseguem completar a operação. Outra opção é usar uma Saga: a transferência é dividida em passos, e se um passo falhar, o sistema executa uma operação de compensação (nesse caso, devolver o valor para a conta de origem) em vez de tentar garantir que tudo aconteça de uma vez só.

## Parte E - Linha do tempo (seção 10.3)

**Observação do passo 3 (evento concorrente):** ao criar uma conta em cada uma das 3 agências quase ao mesmo tempo, as três operações de `CRIAR_CONTA` ficaram todas com `timestampLamport = 1`, cada uma na sua própria agência. Faz sentido: são operações totalmente independentes, nenhuma das três sabia da existência da outra, então não existe relação de causa e efeito entre elas - são eventos genuinamente concorrentes, e por isso o relógio de Lamport não tinha motivo nenhum pra diferenciar os timestamps.

Comparando com `horaParede`, os três eventos aconteceram em milissegundos de diferença (uma ordem real de fato existiu no relógio da máquina), mas essa ordem não aparece no timestamp de Lamport - os três ficaram empatados em 1. Isso reforça que o Lamport não captura uma ordem "real" no tempo, só a ordem causal quando ela existe.

**1. O que significa ver dois timestamps diferentes sem saber se um influenciou o outro?**

Significa que não dá pra confiar cegamente no timestamp de Lamport para concluir causalidade. Se `timestamp(A) < timestamp(B)`, não necessariamente A causou B ou aconteceu antes dele na prática - pode ser só coincidência dos contadores. A única coisa garantida é a implicação em um sentido: se A realmente causou B, então o timestamp de A é menor. A volta não é garantida.

**2. O relógio de Lamport sozinho seria suficiente para distinguir concorrência de causalidade?**

Não. No teste que fiz, três eventos concorrentes (sem nenhuma relação entre si) ficaram com o mesmo timestamp, o que ajudou a identificar a concorrência nesse caso - mas isso foi mais coincidência da ordem de chegada do que uma garantia do algoritmo. Em outros casos, dois eventos concorrentes podem acabar com timestamps diferentes só por causa da ordem em que os contadores foram incrementados, e aí não tem como saber, só olhando o número, se são realmente concorrentes ou se um influenciou o outro. É exatamente essa limitação que motiva o relógio vetorial: ele guarda um contador por processo (não só um valor global), permitindo comparar dois timestamps e saber com certeza se um aconteceu antes do outro ou se são concorrentes.

## Parte F - Autenticação JWT (seção 11.3)

**Sobre o formato de credenciais escolhido:** como as contas do banco não têm dono nem senha (são só `id + nome + saldo`), criei um único usuário de demonstração (`aluno` / `1234`, definido em `config.py`) que representa "alguém logado no sistema", sem estar amarrado a uma conta específica. É uma simplificação proposital para este sprint, já que ainda não existe uma tabela de usuários.

**Sobre a chamada entre agências:** decidi que a chamada `creditar-remoto` também precisa de um token, igual às chamadas vindas do frontend. A agência que inicia a transferência gera um token pra si mesma (usando a mesma chave secreta) antes de chamar a agência de destino. Isso evita ter uma rota "sem porteira" no meio do sistema - toda rota que mexe em conta passa pelo mesmo bloqueio, sem precisar de uma exceção especial só pra chamadas internas.

**1. Diferença entre autenticação e autorização. Minha implementação cobre as duas?**

Autenticação é confirmar quem está fazendo a requisição (a pessoa realmente é quem diz ser). Autorização é decidir o que essa pessoa pode fazer depois de identificada. Minha implementação só cobre autenticação: o JWT garante que quem está chamando a API tem um login válido, mas não existe nenhuma checagem de "essa conta pertence a esse usuário". Na prática, hoje, um usuário autenticado consegue sacar ou consultar qualquer conta de qualquer agência, mesmo que não seja "dele" - já que as contas nem têm um dono formal associado ao login. Isso seria o próximo passo natural (amarrar cada conta a um usuário e checar isso em cada operação).

**2. Por que o servidor não precisa consultar um banco pra validar a assinatura do JWT?**

Porque a assinatura do token já garante matematicamente que ele foi gerado por quem tem a chave secreta e não foi alterado depois. Bastando reprocessar essa assinatura com a mesma chave, o servidor confirma a validade sem precisar guardar nada sobre aquela sessão. Isso é uma vantagem de escalabilidade grande comparado a guardar sessões em memória: com sessão em memória, cada requisição de um usuário precisaria cair sempre no mesmo servidor (ou todos os servidores teriam que compartilhar essa memória); com JWT, qualquer instância da agência consegue validar o token sozinha, sem depender de estado compartilhado.

**3. O que aconteceria se a chave secreta vazasse?**

Qualquer pessoa que tivesse a chave conseguiria gerar tokens válidos pra qualquer usuário, sem precisar saber a senha de ninguém - ou seja, conseguiria se autenticar como se fosse um usuário legítimo e usar a API normalmente. Seria basicamente perder o controle de quem pode entrar no sistema, e a única forma de resolver seria trocar a chave (o que invalida todos os tokens já emitidos, inclusive os de usuários legítimos).

## Parte G - Frontend (seção 12.3)

_Preencher após implementar a Parte G._
