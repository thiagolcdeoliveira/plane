# Plane
Projeto de uma aplicação de pedidos

## Requisitos

## Regras de negócio

**Rentabilidade
Os itens do pedido devem ser classificados em três níveis de rentabilidade, de
acordo com a diferença entre o preço do item (que é informado pelo usuário) e o
preço do produto (que é fixo):
Rentabilidade ótima: quando o preço usado no pedido é maior que o preço do
produto. Ex: se o preço do produto é de R$ 100, a rentabilidade será ótima se o item
for vendido por R$ 100,01 (inclusive) ou mais.

**Rentabilidade boa: quando o preço do item é no máximo 10% menor que o preço
do produto. Ex: se o preço do produto é de R$ 100, a rentabilidade será boa se o item
for vendido por qualquer preço entre R$ 90 (inclusive) e R$ 100 (inclusive).

**Rentabilidade ruim: quando o preço do item é inferior ao preço do produto menos
10%. Ex: se o preço do produto é de R$ 100, a rentabilidade será ruim se o preço for
menor ou igual a R$ 89,99.
Quando o usuário escolher o produto para inserir no pedido, o sistema deve calcular
e exibir a rentabilidade na tela. Sempre que o preço for modificado, a rentabilidade
deve ser recalculada e reexibida. Itens que ficarem com rentabilidade ruim não
podem ser inseridos no pedido.
