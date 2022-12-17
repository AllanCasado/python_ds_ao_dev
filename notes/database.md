# O que é granularidade?

Granularidade é o nível de detalhe no qual o dado é armazenado no Banco de Dados.

### Exemplo 01

| product-category | product-name | product-price |
| --- | --- | --- |
| calca | jeans slim  | 29.99
| calca | jeans flare | 89.99
| calca | jenas urban | 39.99

Nesse caso, o nível de detalhe mínimo de nossa base é o nome do produto. Portanto a granularidade é o Nome de Produto, sendo o preço um atributo do produto.

### Exemplo 02

| product-category | product-name | product-price | color-name
| --- | --- | --- | --- |
| calca | jeans slim  | 29.99 | black
| calca | jeans slim  | 29.99 | white
| calca | jenas slim  | 29.99 | blue
| calca | jeans flare | 89.99 | white
| calca | jenas urban | 39.99 | blue

Nesse caso, a granularidade é a cor do produto. Uma calça, pode ter várias linhas, por que pode possuir múltiplas cores.

### Exemplo 03

| product-category | product-name | product-price | color-name | product-size
| --- | --- | --- | --- | --- |
| calca | jeans slim  | 29.99 | black | 32
| calca | jeans slim  | 29.99 | black | 34
| calca | jeans slim  | 29.99 | black | 36
| calca | jeans slim  | 29.99 | white | 32
| calca | jenas slim  | 29.99 | blue  | 32
| calca | jeans flare | 89.99 | white | 34
| calca | jenas urban | 39.99 | blue  | 32

Nesse caso, a graunilaridade é o tamanho do produto. Uma calça, de umacor, pode possuir várias linhas, pois possuí diferentes tamanhos parauma mesma cor.

### Relevância

Isso é importante, por exemplo, na hora de lidar com linhas duplicadas. Considerando o exemplo 03, se a pessoa não tem ciência de que os valores "categoria", "nome", "preço" e "cor" estão duplicadas por que a granularidade da tabela é o tamanho, ela pode acabar tomando uma atitude errada, removendo as duplicadas.

Se eu fosse salvar a tabela do exemplo 03 em um banco de dados, sem considerar a última coluna, eu estaria adicionando linhas duplicadas, pois a granularidade da tabela estaria errada.
