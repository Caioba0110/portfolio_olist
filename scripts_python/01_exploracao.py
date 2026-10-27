from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent.parent

arquivo = (
    pasta_projeto
    / "dados_originais"
    / "olist_orders_dataset.csv"
)

pedidos = pd.read_csv(arquivo)

print("\nPrimeiras cinco linhas:")
print(pedidos.head())

# print("\nDimensões da tabela:")
# print(pedidos.shape)

# print("\nNomes das colunas:")
# print(pedidos.columns.tolist())

# print("\nPedidos distintos:")
# print(pedidos["order_id"].nunique())

# print("\nIdentificadores de pedidos ausentes:")
# print(pedidos["order_id"].isna().sum())

# print("\nIdentificadores de pedidos repetidos:")
# print(pedidos["order_id"].duplicated().sum())

print("\nQuantidade de pedidos por status:")
print(pedidos["order_status"].value_counts())

print("\nValores ausentes por coluna:")
print(pedidos.isna().sum())

entregues_sem_data = pedidos[
    (pedidos["order_status"] == "delivered")
    & (pedidos["order_delivered_customer_date"].isna())
].copy()

print("\nPedidos entregues sem data:")
print(len(entregues_sem_data))

pedidos["order_delivered_customer_date"] = pd.to_datetime(
    pedidos["order_delivered_customer_date"]
)

pedidos["order_estimated_delivery_date"] = pd.to_datetime(
    pedidos["order_estimated_delivery_date"]
)

print("\nTipos das colunas após a conversão")
print(
    pedidos[
        ["order_delivered_customer_date", "order_estimated_delivery_date"]
    ].dtypes
)

print(
    entregues_sem_data[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ].to_string(index=False)
)

pedidos_avaliaveis = pedidos[
    (pedidos["order_status"] == "delivered")
    & (pedidos["order_delivered_customer_date"].notna())
    & (pedidos["order_estimated_delivery_date"].notna())
].copy()

print("\nQuantidade de pedidos avaliáveis:")
print(len(pedidos_avaliaveis))

pedidos_avaliaveis["entregas_atrasadas"] = (
    pedidos_avaliaveis["order_delivered_customer_date"].dt.normalize()
    > pedidos_avaliaveis["order_estimated_delivery_date"].dt.normalize()
)

print("\nCLassificação das entregas:")
print(pedidos_avaliaveis["entregas_atrasadas"].value_counts())

taxa_entregas_atrasadas = (
    pedidos_avaliaveis["entregas_atrasadas"].sum()
    / len(pedidos_avaliaveis) * 100
)

print(f"\nTaxa de entregas atrasadas: {taxa_entregas_atrasadas:.2f}%")

pedidos_atrasados = pedidos_avaliaveis[
    pedidos_avaliaveis["entregas_atrasadas"] == True
].copy()

print("\nQuantidade de pedidos atrasados:")
print(len(pedidos_atrasados))

pedidos_atrasados["dias_atraso"] = (
    pedidos_atrasados["order_delivered_customer_date"].dt.normalize()
    - pedidos_atrasados["order_estimated_delivery_date"].dt.normalize()
).dt.days

print(
    pedidos_atrasados[
        [
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "dias_atraso"
        ]
    ].head().to_string(index=False)
)

media_dias_atraso = pedidos_atrasados["dias_atraso"].mean()


mediana_dias_atraso = pedidos_atrasados["dias_atraso"].median()


moda_dias_atraso = pedidos_atrasados["dias_atraso"].mode()

print("\nMedia de dias atrasados:")
print(f"{media_dias_atraso:.2f}")

print("\nMediana dias atrasados:")
print(mediana_dias_atraso)

print("\nModa dias atrasados:")
print(moda_dias_atraso)

pedidos_atrasos_1_dia  = pedidos_atrasados[
    pedidos_atrasados["dias_atraso"] == 1
].copy()

# print(len(qtd_atrasos_1_dia))

percentual_atrasos_1_dia = (
        len(pedidos_atrasos_1_dia) / len(pedidos_atrasados) * 100
)

print(f"\nTaxa de entregas com 1 dia de atraso: {percentual_atrasos_1_dia:.2f}%")

arquivo_clientes = (
    pasta_projeto
    / "dados_originais"
    / "olist_customers_dataset.csv"
)

clientes = pd.read_csv(arquivo_clientes)

print(clientes.columns.to_list())

print("\nValores ausentes por coluna:")
print(clientes["customer_id"].isna().sum())

print("\nValores duplicados por coluna:")
print(clientes["customer_id"].duplicated().sum())

pedidos_com_estado = pedidos_avaliaveis.merge(
    clientes[["customer_id", "customer_state"]],
    on = "customer_id",
    how = "left",
    validate = "many_to_one"
)

print("\nQuantidade de linhas após a ligação:")
print(len(pedidos_com_estado))

print("\nPedidos sem estado")
print(pedidos_com_estado["customer_state"].isna().sum())

print("\nExemplo dos pedidos com estado:")
print(
    pedidos_com_estado[
        ["order_id", "customer_state", "entregas_atrasadas"]
    ].head(10).to_string(index = False)
)

# print("\nColunas disponíveis em pedidos_com_estado:")
# print(pedidos_com_estado.columns.to_list())

atrasos_por_estado = (
    pedidos_com_estado
    .groupby("customer_state")["entregas_atrasadas"]
    .sum()
)

print("\nQuantidade de pedidos atrasados por estado:")
print(atrasos_por_estado.sort_values(ascending=False))

pedidos_por_estado = (
    pedidos_com_estado
    .groupby("customer_state")
    .size()
)

print("\nQuantidade de pedidos por estado:")
print(pedidos_por_estado.sort_values(ascending=False))

taxa_atraso_por_estado = (
    atrasos_por_estado
    / pedidos_por_estado * 100
).round(2)

print("\nA taxa de pedidos atrasados por estado é: (%)", taxa_atraso_por_estado.sort_values(ascending=False))

atrasados_com_estado = pedidos_com_estado[pedidos_com_estado["entregas_atrasadas"] == True].copy()

print(len(atrasados_com_estado))

print("\nColunas disponíveis em pedidos_com_estado:")
print(pedidos_com_estado.columns.to_list())

atrasados_com_estado["dias_atraso"] = (
    atrasados_com_estado["order_delivered_customer_date"].dt.normalize()
    - atrasados_com_estado["order_estimated_delivery_date"].dt.normalize()
).dt.days

print("\nDias de atraso por pedido:")
print(
    atrasados_com_estado[
        ["order_id", "customer_state", "dias_atraso"]
    ].head(10).to_string(index = False)
)

media_atraso_por_estado = (
    atrasados_com_estado.groupby("customer_state")["dias_atraso"].mean()
)
print("\nMédia dias de atraso por estado: (dias)")
print(media_atraso_por_estado.round(2).sort_values(ascending=False))

mediana_atraso_por_estado = (
    atrasados_com_estado.groupby("customer_state")["dias_atraso"].median()
)
print("\nMediana dias de atraso por estado: (dias)")
print(mediana_atraso_por_estado.sort_values(ascending=False))

atrasado_ap = atrasados_com_estado[
    atrasados_com_estado["customer_state"] == "AP"
].copy()

print(
    atrasado_ap[
    ["order_id", 
     "order_purchase_timestamp", 
     "order_delivered_customer_date", 
     "order_estimated_delivery_date", 
     "dias_atraso"]
    ].head(10).to_string(index = False)
)

pedidos_com_estado["order_purchase_timestamp"] = pd.to_datetime(
    pedidos_com_estado["order_purchase_timestamp"]
)

pedidos_com_estado["mes_compra"] = (
    pedidos_com_estado["order_purchase_timestamp"].dt.to_period("M")
)

print(
    pedidos_com_estado[
        ["order_purchase_timestamp", "mes_compra"]
    ].head(10).to_string(index = False)
)

# Conta todos os pedidos avaliáveis de cada estado e mês.

pedidos_por_estado_mes = (
    pedidos_com_estado
    .groupby(["customer_state", "mes_compra"])
    .size()
)

# Conta os atrasados nos mesmos grupos.

atrasos_por_estado_mes = (
    pedidos_com_estado
    .groupby(["customer_state", "mes_compra"])["entregas_atrasadas"]
    .sum()
)

# Calcula o percentual de atraso de cada estado e mês.

taxa_atraso_estado_mes = (
    atrasos_por_estado_mes / pedidos_por_estado_mes * 100
)

resumo_mensal = pd.DataFrame({
    "pedidos_avaliaveis" : pedidos_por_estado_mes,
    "pedidos_atrasados" : atrasos_por_estado_mes,
    "taxa_atraso_pct" : taxa_atraso_estado_mes
}).reset_index()

print("\nAtrasos por mês da compra - RJ, Al e SP:")
print(
    resumo_mensal[
        resumo_mensal["customer_state"].isin(["RJ", "AL", "SP"])
    ].round(2).to_string(index = False)
)

arquivo_resumo = (
    pasta_projeto
    / "dados_tratados"
    / "resumo_atrasos_estado_mes.csv"
)

resumo_mensal.to_csv(
    arquivo_resumo,
    index = False,
    encoding = "utf-8-sig"
)

print("\nResumo mensal exportado.")