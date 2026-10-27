USE portfolio_olist;
GO

-- Cria a tabela de clientes caso ela ainda não exista.
IF OBJECT_ID('dbo.clientes', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.clientes (
        customer_id nvarchar(50) NOT NULL,
        customer_unique_id nvarchar(50) NOT NULL,
        customer_zip_code_prefix nvarchar(5) NOT NULL,
        customer_city nvarchar(100) NOT NULL,
        customer_state nvarchar(2) NOT NULL
    );
END;
GO

-- Cria a tabela de pedidos caso ela ainda não exista.
IF OBJECT_ID('dbo.pedidos', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.pedidos (
        order_id nvarchar(50) NOT NULL,
        customer_id nvarchar(50) NOT NULL,
        order_status nvarchar(50) NOT NULL,
        order_purchase_timestamp datetime2 NOT NULL,
        order_approved_at datetime2 NULL,
        order_delivered_carrier_date datetime2 NULL,
        order_delivered_customer_date datetime2 NULL,
        order_estimated_delivery_date datetime2 NOT NULL
    );
END;
GO

-- Cria a tabela de pedidos caso ela ainda não exista.
IF OBJECT_ID('dbo.pedidos', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.pedidos (
        order_id nvarchar(50) NOT NULL,
        customer_id nvarchar(50) NOT NULL,
        order_status nvarchar(50) NOT NULL,
        order_purchase_timestamp datetime2 NOT NULL,
        order_approved_at datetime2 NULL,
        order_delivered_carrier_date datetime2 NULL,
        order_delivered_customer_date datetime2 NULL,
        order_estimated_delivery_date datetime2 NOT NULL,

        CONSTRAINT PK_pedidos PRIMARY KEY (order_id)
    );
END;
GO