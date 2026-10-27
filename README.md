# Olist — Análise de vendas e atrasos nas entregas

Projeto de portfólio desenvolvido por Caio Precioso Prado com Python, SQL Server, Excel e Power BI.

## Objetivo

Identificar quais estados concentram o valor dos produtos vendidos e quais merecem investigação por atrasos nas entregas, considerando volume de pedidos, taxa de atraso e duração dos atrasos.

## Dashboards

### Vendas

![Dashboard de vendas](Imagens/dashboard_vendas.png)

### Entregas

![Dashboard de entregas](Imagens/dashboard_entregas.png)

O relatório interativo está em [portfolio_olist.pbix](Power_BI/portfolio_olist.pbix).

## Principais resultados

| Indicador                                 |        Resultado |
| ----------------------------------------- | ---------------: |
| Pedidos entregues                         |           96.478 |
| Valor dos produtos dos pedidos entregues  | R$ 13.221.498,11 |
| Frete dos pedidos entregues               |  R$ 2.198.275,64 |
| Ticket médio sem frete                    |        R$ 137,04 |
| Pedidos avaliáveis quanto ao prazo        |           96.470 |
| Pedidos entregues com atraso              |            6.534 |
| Taxa de atraso                            |            6,77% |
| Atraso médio entre os pedidos atrasados   |       10,62 dias |
| Atraso mediano entre os pedidos atrasados |           7 dias |

São Paulo concentra 38,33% do valor dos produtos dos pedidos entregues, seguido por Rio de Janeiro, com 13,31%, e Minas Gerais, com 11,74%.

### Prioridades sugeridas para investigação

| Estado | Pedidos avaliáveis | Atrasados | Taxa de atraso | Atraso médio dos atrasados |
| ------ | -----------------: | --------: | -------------: | -------------------------: |
| RJ     |             12.350 |     1.495 |         12,11% |                 13,52 dias |
| AL     |                397 |        85 |         21,41% |                  9,54 dias |
| SP     |             40.494 |     1.820 |          4,49% |                  8,33 dias |

- **Rio de Janeiro:** reúne grande quantidade de atrasos, taxa acima da taxa geral e atrasos de maior duração média.
- **Alagoas:** apresenta a maior taxa de atraso entre os estados, embora tenha um volume menor de pedidos.
- **São Paulo:** apresenta o maior número absoluto de atrasos, mesmo com taxa inferior à taxa geral.

Esses resultados orientam a investigação. Não demonstram, isoladamente, as causas dos atrasos nem justificam uma decisão de investimento.

## Fonte dos dados

[Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Arquivos utilizados:

- `olist_orders_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_items_dataset.csv`

Os CSVs originais não são incluídos no repositório. Para executar as análises, obtenha-os na fonte e coloque-os na pasta `dados_originais`.

Consulte na página da fonte os termos de uso e a licença dos dados.

## Regras dos indicadores

- **Vendas:** considera somente pedidos com status `delivered`.
- **Valor dos produtos:** soma de `price` dos itens desses pedidos, sem frete. Não representa lucro.
- **Ticket médio:** valor dos produtos dividido pela quantidade de pedidos distintos entregues.
- **Pedido avaliável:** pedido entregue com data real de entrega ao cliente e data prevista preenchidas.
- **Entrega atrasada:** data real posterior à data prevista, comparando apenas o dia, sem considerar o horário.
- **Taxa de atraso:** pedidos atrasados divididos pelos pedidos avaliáveis do mesmo recorte.
- **Dias de atraso:** diferença em dias entre a entrega real e a previsão, somente para pedidos atrasados.
- **Análise mensal:** agrupa os pedidos pelo mês da compra.
- **Estado:** utiliza `customer_state` da tabela de clientes.

Os oito pedidos entregues sem data de entrega ao cliente permanecem na análise de vendas, mas são excluídos dos indicadores de prazo.

## Etapas do projeto

### Python

Exploração dos CSVs, verificação de campos ausentes e duplicidades, conversão de datas, ligação entre tabelas e cálculo dos indicadores.

Na análise de vendas, os valores dos itens são somados por pedido antes da ligação com a tabela de pedidos, preservando uma linha por pedido.

### SQL Server

Importação dos dados, conferência dos tipos e validação dos resultados por meio de consultas com JOIN, GROUP BY, CASE, COUNT, SUM, AVG e DATEDIFF.

Durante a importação, foi identificado um problema de conversão decimal: o valor 58.90 havia sido interpretado como 5890.00. Os valores foram corrigidos com base em uma tabela auxiliar e os totais foram conferidos antes da confirmação da transação.

### Excel

Tabela dinâmica por estado, cálculo da taxa de atraso, formatação condicional e gráfico de comparação.

### Power BI

Modelo com as tabelas de pedidos, itens e clientes, indicadores em DAX e páginas interativas de vendas e entregas, com filtro por estado.

## Organização dos arquivos

| Local              | Conteúdo                                                             |
| ------------------ | -------------------------------------------------------------------- |
| `scripts_python/`  | Scripts de exploração, vendas e preparação da base Excel             |
| `SQL/`             | Estrutura das tabelas, registro da correção e consultas de validação |
| `dados_originais/` | CSVs obtidos na fonte, mantidos localmente                           |
| `dados_tratados/`  | Resumos em CSV e arquivos Excel                                      |
| `Power_BI/`        | Relatório `.pbix`                                                    |
| `Imagens/`         | Capturas dos dashboards                                              |
| `requirements.txt` | Dependências diretas do Python                                       |

## Como executar as análises em Python

Ambiente utilizado:

- Python 3.14.2
- pandas 2.3.3
- openpyxl 3.1.5

1. Baixe o projeto e preserve a organização das pastas.
2. Crie `dados_originais` se ela não existir e adicione os três CSVs.
3. Garanta que a pasta `dados_tratados` exista.
4. Abra o terminal na pasta principal do projeto.
5. Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

6. Execute:

```bash
python scripts_python/01_exploracao.py
python scripts_python/02_analise_vendas.py
python scripts_python/03_preparacao_excel.py
```

O script 01 gera `resumo_atrasos_estado_mes.csv`.

O script 02 gera `resumo_vendas_estado.csv` e pode executar independentemente do script 01.

O script 03 depende do resumo gerado pelo script 01 e cria `base_entregas.xlsx`. Ele não recria a tabela dinâmica e o gráfico da planilha final `analise_entregas.xlsx`.

## Como consultar as análises em SQL

É necessário ter SQL Server, SSMS e o banco `portfolio_olist` com as tabelas carregadas.

A importação utilizada no desenvolvimento foi realizada pelo assistente “Importar Arquivo Simples” do SSMS:

| CSV                             | Tabela         |
| ------------------------------- | -------------- |
| `olist_orders_dataset.csv`      | `dbo.pedidos`  |
| `olist_customers_dataset.csv`   | `dbo.clientes` |
| `olist_order_items_dataset.csv` | `dbo.itens`    |

O assistente cria as tabelas durante a importação. O arquivo `00_criacao_tabelas.sql` registra a estrutura final para referência ou para uma carga alternativa em tabelas previamente criadas. Ele não importa os CSVs nem cria o banco.

Confira os tipos das colunas, os campos que permitem valores ausentes e a interpretação do ponto decimal antes de validar os resultados.

Após a carga, execute:

1. `SQL/01_validacao_vendas.sql`
2. `SQL/02_validacao_entregas.sql`

O arquivo `00_correcao_importacao_itens.sql` documenta uma correção específica do desenvolvimento. Depende de `dbo.itens_importacao` e não deve ser executado como uma etapa obrigatória em uma importação já correta.

## Como visualizar o relatório

Abra `Power_BI/portfolio_olist.pbix` no Power BI Desktop.

Para atualizar os dados, é necessário configurar a conexão com sua instância do SQL Server e ter o banco com as tabelas correspondentes. Os scripts Python não atualizam automaticamente o banco SQL.

As capturas na pasta `Imagens` permitem consultar a apresentação sem abrir o Power BI.

## Limitações e cuidados de interpretação

- Os resultados descrevem o conjunto histórico utilizado, não a operação atual da empresa.
- Os indicadores de prazo consideram somente pedidos entregues com datas disponíveis. Não medem pedidos ainda em trânsito.
- A taxa geral é calculada pelos totais, não pela média simples das taxas dos estados ou meses.
- Setembro de 2016 possui apenas um pedido avaliável, entregue com atraso, resultando em 100%. Taxas devem ser interpretadas junto ao volume.
- O Amapá possui dois pedidos atrasados, com atrasos de 144 dias e 1 dia. A média de 72,5 dias não indica que esse seja um comportamento recorrente.
- A análise não identifica causas operacionais nem estima margem de lucro.
- O gráfico do Excel utiliza uma tabela auxiliar com valores fixos. Se a base mudar, essa tabela também precisa ser atualizada.

## Aprendizados

- Distinguir quantidade de itens, unidades e pedidos distintos.
- Preservar o nível de detalhe dos dados ao realizar ligações.
- Tratar informações ausentes sem inventar valores.
- Validar indicadores entre ferramentas.
- Comparar volume, proporção e duração antes de recomendar uma investigação.
- Documentar regras, limitações e instruções de execução.
