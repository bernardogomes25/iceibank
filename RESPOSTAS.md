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

_Preencher após implementar a Parte E._

## Parte F - Autenticação JWT (seção 11.3)

_Preencher após implementar a Parte F._

## Parte G - Frontend (seção 12.3)

_Preencher após implementar a Parte G._
