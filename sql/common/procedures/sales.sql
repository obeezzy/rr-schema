CREATE OR REPLACE FUNCTION AddSoldProduct (
    IN iSaleTransactionId BIGINT,
    IN iProductId BIGINT,
    IN iProductUnitId BIGINT,
    IN iUnitPrice NUMERIC(19,2),
    IN iQuantity REAL,
    IN iCost NUMERIC(19,2),
    IN iDiscount NUMERIC(19,2),
    IN iCurrency VARCHAR(4),
    IN iUserId BIGINT
) RETURNS TABLE(sold_product_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO sold_product (sale_transaction_id,
                                            product_id,
                                            product_unit_id,
                                            unit_price,
                                            quantity,
                                            cost,
                                            discount,
                                            currency,
                                            user_id)
    VALUES (iSaleTransactionId,
                iProductId,
                iProductUnitId,
                iUnitPrice,
                iQuantity,
                iCost,
                iDiscount,
                iCurrency,
                iUserId)
    RETURNING id AS sale_transaction_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddSalePayment (
    IN iSaleTransactionId BIGINT,
    IN iAmount NUMERIC(19,2),
    IN iPaymentMethod PAYMENT_METHOD,
    IN iCurrency VARCHAR(4),
    IN iUserId BIGINT,
    IN iNoteId BIGINT
) RETURNS TABLE(sale_payment_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO sale_payment (sale_transaction_id,
                                amount,
                                payment_method,
                                currency,
                                note_id,
                                user_id)
    VALUES (iSaleTransactionId,
            iAmount,
            iPaymentMethod,
            iCurrency,
            NULLIF(iNoteId, 0),
            iUserId)
    RETURNING id AS sale_payment_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddSaleTransaction (
    IN iCustomerName TEXT,
    IN iCustomerId BIGINT,
    IN iDiscount NUMERIC(19,2),
    IN iSuspended BOOLEAN,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO sale_transaction (customer_name,
                                    customer_id,
                                    discount,
                                    suspended,
                                    note_id,
                                    user_id)
    VALUES (NULLIF(iCustomerName, ''),
                NULLIF(iCustomerId, 0),
                iDiscount,
                iSuspended,
                NULLIF(iNoteId, 0),
                iUserId)
    RETURNING id AS sale_transaction_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ViewSaleTransactions (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IN iSuspended BOOLEAN DEFAULT FALSE,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(sale_transaction_id BIGINT, customer_name TEXT, customer_id BIGINT,
                discount NUMERIC(19,2), suspended BOOLEAN, note_id BIGINT,
                total_amount NUMERIC(19,2), note TEXT, archived BOOLEAN,
                created TIMESTAMP, last_edited TIMESTAMP, user_id BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT st.id AS sale_transaction_id,
            st.customer_name AS customer_name,
            st.customer_id AS customer_id,
            st.discount AS discount,
            st.suspended AS suspended,
            st.note_id AS note_id,
            (SELECT SUM(sale_payment.amount)
                FROM sale_payment
                WHERE sale_payment.sale_transaction_id = st.id) AS total_amount,
            note.note AS note,
            st.archived AS archived,
            st.created AS created,
            st.last_edited AS last_edited,
            st.user_id AS user_id
    FROM sale_transaction st
    LEFT JOIN note ON st.note_id = note.id
    WHERE st.suspended = iSuspended
        AND st.archived = iArchived
        AND st.created BETWEEN iFrom AND iTo
    ORDER BY created ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION IsSaleTransactionSuspended (
    IN iSaleTransactionId BIGINT
) RETURNS BOOLEAN
AS $$
    SELECT suspended
    FROM sale_transaction
    WHERE archived = FALSE
        AND id = iSaleTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveSaleTransaction (
    IN iArchived BOOLEAN,
    IN iSaleTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
BEGIN
    UPDATE sale_transaction
        SET archived = iArchived,
            user_id = iUserId
        WHERE id = iSaleTransactionId;
    UPDATE sold_product
        SET archived = iArchived,
            user_id = iUserId
        WHERE sale_transaction_id = iSaleTransactionId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewSaleCart (
    IN iSaleTransactionId BIGINT,
    IN iSaleTransactionArchived BOOLEAN,
    IN iSoldProductArchived BOOLEAN
) RETURNS TABLE(sale_transaction_id BIGINT, customer_name TEXT, customer_id BIGINT,
                customer_phone_number TEXT, total_cost NUMERIC(19,2), suspended BOOLEAN,
                note_id BIGINT, created TIMESTAMP, last_edited TIMESTAMP, user_id BIGINT,
                product_category_id BIGINT, product_category TEXT, product_id BIGINT,
                product TEXT, product_unit_id BIGINT, product_unit TEXT,
                unit_price NUMERIC(19,2), quantity REAL, available_quantity REAL,
                cost_price NUMERIC(19,2), retail_price NUMERIC(19,2),
                cost NUMERIC(19,2), discount NUMERIC(19,2), currency VARCHAR(4),
                note TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT sale_transaction.id AS sale_transaction_id,
            sale_transaction.customer_name AS customer_name,
            sale_transaction.customer_id AS customer_id,
		    client.phone_number AS customer_phone_number,
                (SELECT SUM(sold_product.cost)
                FROM sold_product
                WHERE sold_product.sale_transaction_id = iSaleTransactionId) AS total_cost,
        sale_transaction.suspended AS suspended,
        sale_transaction.note_id AS note_id,
        sale_transaction.created AS created,
        sale_transaction.last_edited AS last_edited,
        sale_transaction.user_id AS user_id,
        product_category.id AS product_category_id,
        product_category.category AS product_category,
        sold_product.product_id AS product_id,
        product.product AS product,
        product_unit.id AS product_unit_id,
        product_unit.unit AS product_unit,
        sold_product.unit_price AS unit_price,
        sold_product.quantity AS quantity,
        product_quantity.quantity AS available_quantity,
        product_unit.cost_price AS cost_price,
        product_unit.retail_price AS retail_price,
        sold_product.cost as cost,
        sold_product.discount AS discount,
        sold_product.currency AS currency,
        note.note AS note
    FROM sold_product
    INNER JOIN sale_transaction ON sold_product.sale_transaction_id = sale_transaction.id
    INNER JOIN product ON sold_product.product_id = product.id
    INNER JOIN product_unit ON sold_product.product_id = product_unit.product_id
    INNER JOIN product_quantity ON sold_product.product_id = product_quantity.product_id
    INNER JOIN product_category ON product.product_category_id = product_category.id
    LEFT JOIN customer ON sale_transaction.customer_id = customer.id
    LEFT JOIN client ON customer.client_id = client.id
    LEFT JOIN note ON sold_product.note_id = note.id
    WHERE sale_transaction.id = iSaleTransactionId
        AND sale_transaction.archived = iSaleTransactionArchived
        AND sold_product.archived = iSoldProductArchived
    ORDER BY sold_product.product_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewSoldProducts (
    IN iSaleTransactionId BIGINT,
    IN iSuspended BOOLEAN DEFAULT FALSE,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_category_id BIGINT, product_category TEXT, product_id BIGINT,
                product TEXT, unit_price NUMERIC(19,2), quantity REAL,
                product_unit_id BIGINT, product_unit TEXT, cost NUMERIC(19,2),
                discount NUMERIC(19,2), currency VARCHAR(4), note_id BIGINT,
                note TEXT, archived BOOLEAN, created TIMESTAMP,
                last_edited TIMESTAMP, user_id BIGINT, username TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT product_category.id AS product_category_id,
            product_category.category AS product_category,
            sold_product.product_id AS product_id,
            product.product AS product,
		    sold_product.unit_price AS unit_price,
            sold_product.quantity AS quantity,
            product_unit.id AS product_unit_id,
		    product_unit.unit AS product_unit,
            sold_product.cost AS cost,
            sold_product.discount AS discount,
            sold_product.currency AS currency,
            sold_product.note_id AS note_id,
            note.note AS note,
            sold_product.archived AS archived,
            sold_product.created AS created,
            sold_product.last_edited AS last_edited,
            sold_product.user_id AS user_id,
            rr_user.username AS username
        FROM sold_product
        INNER JOIN product ON sold_product.product_id = product.id
        INNER JOIN product_category ON product_category.id = product.product_category_id
        INNER JOIN product_unit ON sold_product.product_id = product_unit.product_id
                                AND product_unit.preferred = TRUE
        INNER JOIN sale_transaction ON sale_transaction.id = sold_product.sale_transaction_id
        LEFT JOIN rr_user ON sold_product.user_id = rr_user.id
        LEFT JOIN note ON sold_product.note_id = note.id
        WHERE sale_transaction_id = iSaleTransactionId
            AND sale_transaction.suspended = iSuspended
            AND sale_transaction.archived = iArchived
        ORDER BY sold_product.created;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION RevertSaleQuantityUpdate (
    IN iSaleTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE product_quantity AS cpq
    SET quantity = cpq.quantity + sp.quantity,
        user_id = iUserId
    FROM sold_product sp, sale_transaction st
    WHERE cpq.product_id = sp.product_id
        AND sp.sale_transaction_id = st.id
        AND st.id = iSaleTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION FetchTotalRevenue (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(created DATE, total_revenue NUMERIC(19,2))
AS $$
BEGIN
	RETURN QUERY SELECT DATE(sale_transaction.created) AS created,
            SUM(sale_payment.amount) AS total_revenue
        FROM sale_transaction
        INNER JOIN sale_payment ON sale_payment.sale_transaction_id = sale_transaction.id
        WHERE sale_transaction.suspended = FALSE
            AND sale_transaction.archived = FALSE
            AND DATE(sale_transaction.created)
            BETWEEN DATE(iFrom)
                AND DATE(iTo)
        GROUP BY DATE(sale_transaction.created);
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchMostSoldProducts (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IN iLimit BIGINT DEFAULT 5
) RETURNS TABLE(product_category_id BIGINT, product_category TEXT, product_id BIGINT,
                product TEXT, product_unit_id BIGINT, product_unit TEXT,
                total_revenue NUMERIC(19,2), total_quantity REAL)
AS $$
BEGIN
    RETURN QUERY SELECT product_category.id AS product_category_id,
            product_category.category AS product_category,
            sold_product.product_id AS product_id,
            product.product AS product,
            sold_product.product_unit_id AS product_unit_id,
            product_unit.unit AS product_unit,
		    SUM(sold_product.cost - sold_product.discount) AS total_revenue,
            SUM(sold_product.quantity) AS total_quantity
    FROM sold_product
    INNER JOIN product ON product.id = sold_product.product_id
    INNER JOIN product_category ON product_category.id = product.product_category_id
    INNER JOIN product_unit ON product_unit.id = sold_product.product_unit_id
    WHERE sold_product.created BETWEEN iFrom AND iTo
    GROUP BY sold_product.product_id, sold_product.product_unit_id, product_category.id, product.product, product_unit.unit
    ORDER BY SUM(sold_product.quantity) DESC
    LIMIT iLimit;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewSaleReport (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
        product TEXT, quantity_sold REAL, product_unit_id BIGINT,
        product_unit TEXT, total_revenue NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT p.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            p.product AS product,
            (SELECT COALESCE(SUM(quantity), 0)
                FROM sold_product
                WHERE created BETWEEN iFrom AND iTo
                AND sold_product.product_id = p.id) AS quantity_sold,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            (SELECT COALESCE(SUM(cost), '0.00')
                FROM sold_product
                WHERE created BETWEEN iFrom AND iTo
                AND sold_product.product_id = p.id) AS total_revenue
    FROM product p
    INNER JOIN product_category ON p.product_category_id = product_category.id
    INNER JOIN product_unit ON p.id = product_unit.product_id
    INNER JOIN product_quantity ON p.id = product_quantity.product_id
    LEFT JOIN rr_user ON p.user_id = rr_user.id
    WHERE p.archived = FALSE
        AND product_unit.base_unit_equivalent = 1;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterSaleReport (
    IN iFilterColumn TEXT,
    IN iFilterText TEXT,
    IN iSortColumn TEXT,
    IN iSortOrder TEXT,
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
                product TEXT, quantity_sold REAL, product_unit_id BIGINT,
                product_unit TEXT, total_revenue NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT p.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            p.product AS product,
            (SELECT COALESCE(SUM(quantity), 0)
                FROM sold_product
                WHERE created BETWEEN iFrom AND iTo
                AND sold_product.product_id = p.id) AS quantity_sold,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            (SELECT COALESCE(SUM(cost), '0.00')
                FROM sold_product
                WHERE created BETWEEN iFrom AND iTo
                AND sold_product.product_id = p.id) AS total_revenue
    FROM product p
    INNER JOIN product_category ON p.product_category_id = product_category.id
    INNER JOIN product_unit ON p.id = product_unit.product_id
    INNER JOIN product_quantity ON p.id = product_quantity.product_id
    LEFT JOIN rr_user ON p.user_id = rr_user.id
    WHERE p.archived = FALSE
        AND product_unit.base_unit_equivalent = 1
        AND product_category.category LIKE (CASE
                                            WHEN LOWER(iFilterColumn) = 'product_category'
                                            THEN CONCAT('%', iFilterText, '%')
                                            ELSE '%'
                                            END)
        AND p.product LIKE (CASE
                            WHEN LOWER(iFilterColumn) = 'product'
                            THEN CONCAT('%', iFilterText, '%')
                            ELSE '%'
                            END)
    ORDER BY (CASE
                WHEN LOWER(iSortOrder) = 'descending'
                AND LOWER(iSortColumn) = 'product_category'
                THEN LOWER(product_category.category) END) DESC,
             (CASE
                WHEN (iSortOrder IS NULL AND iSortColumn IS NULL)
                OR (LOWER(iSortOrder) <> 'descending'
                    AND LOWER(iSortColumn) = 'product_category')
                THEN LOWER(product_category.category) END) ASC,
    LOWER(p.product) ASC;
END
$$ LANGUAGE plpgsql;
