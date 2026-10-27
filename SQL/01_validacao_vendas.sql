USE portfolio_olist;

-- 1. Indicadores gerais dos pedidos entregues.
SELECT
    COUNT(DISTINCT p.order_id) AS pedidos_entregues,
    SUM(i.price) AS valor_produtos,
    SUM(i.freight_value) AS valor_frete,
    CAST(
        SUM(i.price)
        / NULLIF(COUNT(DISTINCT p.order_id), 0)
        AS decimal(18, 2)
    ) AS ticket_medio_sem_frete
FROM dbo.pedidos AS p
INNER JOIN dbo.itens AS i
    ON p.order_id = i.order_id
WHERE p.order_status = 'delivered';


-- 2. Quantidade de pedidos e valor dos produtos por estado.
SELECT
    c.customer_state AS estado,
    COUNT(DISTINCT p.order_id) AS pedidos_entregues,
    SUM(i.price) AS valor_produtos
FROM dbo.pedidos AS p
INNER JOIN dbo.itens AS i
    ON p.order_id = i.order_id
INNER JOIN dbo.clientes AS c
    ON p.customer_id = c.customer_id
WHERE p.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY valor_produtos DESC;