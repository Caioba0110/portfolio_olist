USE portfolio_olist;

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    UPDATE i
    SET
        i.price = CONVERT(decimal(18, 2), origem.price),
        i.freight_value = CONVERT(decimal(18, 2), origem.freight_value)
    FROM dbo.itens AS i
    INNER JOIN dbo.itens_importacao AS origem
        ON i.order_id = origem.order_id
        AND i.order_item_id = origem.order_item_id;

    -- Conferência dos valores dos pedidos entregues
    DECLARE @total_produtos decimal(18, 2);
    DECLARE @total_frete decimal(18, 2);

    SELECT
        @total_produtos = SUM(i.price),
        @total_frete = SUM(i.freight_value)
    FROM dbo.itens AS i
    INNER JOIN dbo.pedidos AS p
        ON i.order_id = p.order_id
    WHERE p.order_status = 'delivered';

    IF @total_produtos IS NULL
        OR @total_frete IS NULL
        OR @total_produtos <> 13221498.11
        OR @total_frete <> 2198275.64
    BEGIN
        THROW 50001, 'Os totais não correspondem à validação. Correção desfeita.', 1;
    END;

    COMMIT TRANSACTION;

    SELECT
        @total_produtos AS valor_produtos,
        @total_frete AS valor_frete;

    PRINT 'Correção salva com sucesso.';
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;