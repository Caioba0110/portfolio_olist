from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent.parent

arquivo_itens = (
    pasta_projeto
    / "dados_originais"
    / "olist_order_items_dataset.csv"
)

itens = pd.read_csv(arquivo_itens)

print("\nDimensões da tabela de itens:")
print(itens.shape)

print("\nColunas disponíveis:")
print(itens.columns.tolist())

print("\nPrimeiros cinco itens:")
print(itens.head(5).to_string(index = False))

print("\nValores ausentes nos campos essenciais:")
print(
    itens[
        ["order_id", "order_item_id", "price", "freight_value"]
    ].isna().sum()
)

print("\nCombinações de pedido e item repetidas:")
print(
    itens.duplicated(
        subset = ["order_id", "order_item_id"]
    ).sum()
)

print("\nPedidos distintos na tabelas de itens:")
print(itens["order_id"].nunique())

valores_por_pedido = (
    itens.groupby("order_id")[["price", "freight_value"]]
    .sum()
    .reset_index()
)

print("\nValores por pedido:")
print(valores_por_pedido.head().to_string(index = False))

print("\nQuantidade de linhas do resumo:")
print(len(valores_por_pedido))

arquivo_pedidos = (
    pasta_projeto
    / "dados_originais"
    / "olist_orders_dataset.csv"
)

pedidos = pd.read_csv(arquivo_pedidos)

pedidos_com_valores = pedidos.merge(
    valores_por_pedido,
    on = "order_id",
    how = "left",
    validate = "one_to_one",
    indicator = True
)

print("\nResultado da ligação:")
print(pedidos_com_valores["_merge"].value_counts())

pedidos_sem_itens = pedidos_com_valores[
    pedidos_com_valores["_merge"] == "left_only"
].copy()

print("\nStatus dos pedidos sem itens:")
print(pedidos_sem_itens["order_status"].value_counts())

vendas_entregues = pedidos_com_valores[
    pedidos_com_valores["order_status"] == "delivered"
].copy()

total_produtos = vendas_entregues["price"].sum()
total_frete = vendas_entregues["freight_value"].sum()
total_pedidos_entregues = len(vendas_entregues)

ticket_medio_produtos = total_produtos / total_pedidos_entregues

print("\nPedidos entregues:", total_pedidos_entregues)
print(f"Valor dos produtos: R$ {total_produtos:.2f}")
print(f"Valor do frete: R$ {total_frete:.2f}")
print(f"Ticket médio sem frete: R$ {ticket_medio_produtos:.2f}")

arquivo_clientes = (
    pasta_projeto
    / "dados_originais"
    / "olist_customers_dataset.csv"
)

clientes = pd.read_csv(arquivo_clientes)

vendas_por_cliente = vendas_entregues.merge(
    clientes[["customer_id", "customer_state"]],
    on = "customer_id",
    how = "left",
    validate = "many_to_one"
)

print("\nPedidos após a ligação:")
print(len(vendas_por_cliente))

print("\nPedidos sem estado:")
print(vendas_por_cliente["customer_state"].isna().sum())

valor_vendido_por_estado = (
    vendas_por_cliente
    .groupby("customer_state")["price"]
    .sum()
    .sort_values(ascending = False)
)

print("\nValor dos produtos por estado - sem frete (R$):")
print(valor_vendido_por_estado.round(2))

print(f"\nValor total dos estados: R$ {valor_vendido_por_estado.sum():.2f}")

participacao_por_estado = (
    valor_vendido_por_estado / total_produtos * 100
)

print("\nParticipação no valor do produtos de cada estado (%):")
print(participacao_por_estado.round(2))

resumo_vendas_estado = pd.DataFrame({
    "valor_produtos": valor_vendido_por_estado,
    "participacao_pct": participacao_por_estado
}).reset_index()

arquivo_resumo_vendas = (
    pasta_projeto
    / "dados_tratados"
    / "resumo_vendas_estado.csv"
)

resumo_vendas_estado.to_csv(
    arquivo_resumo_vendas,
    index = False,
    encoding = "utf-8-sig"
)

print("\nResumo de vendas por estado exportado.")