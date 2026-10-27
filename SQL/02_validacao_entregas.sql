USE portfolio_olist;

-- 1. Taxa geral de atraso.
-- A CTE seleciona os pedidos avaliáveis e classifica cada um.
-- 1 = atrasado; 0 = entregue no prazo.
WITH entregas_avaliaveis AS (
    SELECT
        order_id,
        CASE
            WHEN CAST(order_delivered_customer_date AS date)
                 > CAST(order_estimated_delivery_date AS date)
            THEN 1
            ELSE 0
        END AS entrega_atrasada
    FROM dbo.pedidos
    WHERE order_status = 'delivered'
        AND order_delivered_customer_date IS NOT NULL
        AND order_estimated_delivery_date IS NOT NULL
)
SELECT
    COUNT(*) AS pedidos_avaliaveis,
    SUM(entrega_atrasada) AS pedidos_atrasados,
    CAST(
        SUM(entrega_atrasada) * 100.0 / COUNT(*)
        AS decimal(10,2)
    ) AS taxa_atraso_pct
FROM entregas_avaliaveis;


-- 2. Taxa de atraso por estado.
-- A ligação com clientes acrescenta o estado de cada pedido.
WITH entregas_avaliaveis AS (
    SELECT
        p.order_id,
        c.customer_state AS estado,
        CASE
            WHEN CAST(p.order_delivered_customer_date AS date)
                 > CAST(p.order_estimated_delivery_date AS date)
            THEN 1
            ELSE 0
        END AS entrega_atrasada
    FROM dbo.pedidos AS p
    INNER JOIN dbo.clientes AS c
        ON p.customer_id = c.customer_id
    WHERE p.order_status = 'delivered'
        AND p.order_delivered_customer_date IS NOT NULL
        AND p.order_estimated_delivery_date IS NOT NULL
)
SELECT
    estado,
    COUNT(*) AS pedidos_avaliaveis,
    SUM(entrega_atrasada) AS pedidos_atrasados,
    CAST(
        SUM(entrega_atrasada) * 100.0 / COUNT(*)
        AS decimal(10,2)
    ) AS taxa_atraso_pct
FROM entregas_avaliaveis
GROUP BY estado
ORDER BY taxa_atraso_pct DESC;


-- 3. Duração média dos atrasos por estado.
-- Aqui selecionamos SOMENTE pedidos atrasados.
-- DATEDIFF calcula os dias entre previsão e entrega real.
WITH pedidos_atrasados AS (
    SELECT
        p.order_id,
        c.customer_state AS estado,
        DATEDIFF(
            DAY,
            CAST(p.order_estimated_delivery_date AS date),
            CAST(p.order_delivered_customer_date AS date)
        ) AS dias_atraso
    FROM dbo.pedidos AS p
    INNER JOIN dbo.clientes AS c
        ON p.customer_id = c.customer_id
    WHERE p.order_status = 'delivered'
        AND p.order_delivered_customer_date IS NOT NULL
        AND p.order_estimated_delivery_date IS NOT NULL
        AND CAST(p.order_delivered_customer_date AS date)
            > CAST(p.order_estimated_delivery_date AS date)
)
SELECT
    estado,
    COUNT(*) AS pedidos_atrasados,
    CAST(
        AVG(CAST(dias_atraso AS decimal(10,2)))
        AS decimal(10,2)
    ) AS media_dias_atraso
FROM pedidos_atrasados
GROUP BY estado
ORDER BY media_dias_atraso DESC;