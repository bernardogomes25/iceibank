# Respostas - Sprint 1: ICEIBank

## Funcionalidade adicional (seção 2.1)

_Preencher na Parte extra._

## Parte B - Relógio de Lamport (seção 6.4)

**1. Por que usar `max(contador_local, timestampRecebido) + 1` em vez de simplesmente adotar o timestamp recebido?**

Porque o relógio de Lamport precisa ser sempre crescente para cada processo, e adotar direto o valor recebido poderia até fazer o contador andar para trás. Se a agência que está recebendo já processou mais eventos do que a que enviou a mensagem, o timestamp recebido pode ser menor que o contador atual - nesse caso, simplesmente copiar o valor recebido quebraria a regra de que o tempo nunca volta atrás. Usando o `max` mais 1, o contador sempre respeita as duas condições: fica maior que o que a própria agência já tinha e maior que o evento que causou o recebimento da mensagem.

**2. Se a Agência 0 está no contador 10 e recebe uma mensagem com timestamp 3, qual o novo valor?**

O novo valor fica `max(10, 3) + 1 = 11`. Ou seja, o timestamp recebido (3) praticamente não teve efeito nenhum no cálculo, porque a Agência 0 já estava muito mais "adiantada". Isso mostra que agências que processam muitos eventos rapidamente vão sempre ter contadores mais altos, enquanto agências mais lentas ficam com contadores mais baixos - só quando uma agência lenta manda uma mensagem para uma mais rápida (ou vice-versa) é que o `max` realmente serve para sincronizar as duas.

## Parte D - Transferências (seção 8.3)

_Preencher após implementar a Parte D._

## Parte E - Linha do tempo (seção 10.3)

_Preencher após implementar a Parte E._

## Parte F - Autenticação JWT (seção 11.3)

_Preencher após implementar a Parte F._

## Parte G - Frontend (seção 12.3)

_Preencher após implementar a Parte G._
