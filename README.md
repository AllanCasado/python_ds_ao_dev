# Assuntos abordados no curso

* Modelo de negócio e métricas
* Pensamento analítico
* Web Scrapping
* Web Scrapping assíncrono
* Banco de Dados e SQL
* Ambiente Virtual de Python
* Agendamento de Jobs
* Análise de Dados

# Problema de negócio abordado

Eduardo e Marcelo são dois brasileiros, amigos e sócios de empreendimento. Depois de vários
negócio bem sucedidos, eles estão planejando entrar no mercado de moda dos USA como um
modelo de negócio do tipo E-commerce.

A idéia inicial é entrar no mercado com apenas um produto e para um público específico, no caso
o produto seria calças Jenas para o público masculino. O objetivo é manter o custo de operação
baixo e escalar a medida que forem conseguindo clientes.

Porém, mesmo com o produto de entrada e a audiência definidos, <b>os dois sócios não tem experiência
nesse mercado de moda e portanto não sabem definir coisas básicas como preço, o tipo de calça e
o material para a fabricação de cada peça. </b>

As principais concorrentes da empresa Start Jeans são as americadas H&M e Macys.

Assim, os dois sócios contrataram uma consultoria de Ciência de Dados para responder as seguintes
perguntas: 
1. Qual o melhor preço de venda para as calças? 
2. Quantos tipos de calças e suas cores para o produto inicial? 
3. Quais as matérias-prima necessárias para confeccionar as calças?

# Pensamento Analítico

## Etapas do Pensamento Analítico

1. <b>Identificação da causa raíz </b>: entender realmente o problema.
2. <b>Definir um escopo fechado para uma pergunta aberta </b>: definir os limites (de tempo, de produto, de preço) que você tem para realizar o projeto.
3. <b>Quebrar o problema definido em tarefas menores </b>.
4. <b>Organizar as tarefas em ordem lógica</b>: as vezes a ordem que você quebrou o problema não é a ordem que você deve realizar essas tarefas.
5. <b>Executar com uma mentalidade cíclica</b>.

## Exemplo no contexto de negócio apresentado acima

### Questão: Qual o melhor preço de venda do produto?

1. Identificação da causa raíz.
* Motivação: Qual o contexto em que essa pergunta está sendo feita?
	- A empresa está entrando no mercado de varejo de moda dosUSA e não tem expertise para precificar o produto. Definição do preço para maximizar o lucro.
* Qual é a causa raíz do problema?
	- Precificação de produto.
	- Preço ótimo para maximizar o lucro.


2. Definir um escopo fechado para uma pergunta aberta.
* Definir o escopo em termos de: Produto | Tempo | Localidade | atributo do produto.
	- Mediana dos preços dos sites concorrentes nos USA por produto, tipo e cor, dos últimos 30 dias.


3. Quebrar o problema definido em tarefas menores.
* Tarefas:
	- Calcular a mediana de preço dos sites concorrentes por produto, tipo e cor dos últimos 30 dias.
	- Montar uma base de dados que contenha informações do produto, tipo, cor e dias de exposição.
	- Define o schema do DB.
	- Define a infraestrutura (DB, csv, API...)
	- Design do ETL.
	- Agendamento da atualização da tabela.
	- Entrega do produto final.


4. Organizar as tarefas por ordem.
* Tarefas organizadas em ordem lógica:
	- Montar uma base de dados que contenha info
rmações do produto, tipo, cor e dias de exposição.  
	- Define o Schema
	- Define a infraestrutura
	- Fazer o ETL
	- Calcular a mediana de preço
	- Fazer a visualização do produto
	- Entregar o produto final


5. Executar com mentalidade cíclica.
* É preciso passar por todas as tarefas o mais rápido possível para:
	- Identificar bloqueios.
	- Identificar impeditivos que possam desvalidar o projeto.
	- Entregar valor para a empresa rapidamente.

# Planejamento da solução - o método SAPE

1. Pensar primeiro na saída, no produto final.
	- A resposta para a pergunta.
	- Formato da entrega. (um gráfico, uma tabela - quais colunas deve ter?...)
	- Local da entrega. (um bot do telegram, um dashboard no streamlit? ...)

2. Processo (passo a passo):
	- Passo a passo para construir o cálculo da mediana ou média.
	- Definir o formato da entrega (visualização, tabela, frase)
	- Definir o local de entrega (Power BI, Telegram, Email, Streamlit)

3. Entrada (fonte de dados):
	- Fonte de dados.
	- Ferramentas.





