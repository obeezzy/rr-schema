USE ###DATABASENAME###;

---

CREATE PROCEDURE AddSoldProduct (
	IN iSaleTransactionId INTEGER,
    IN iProductId INTEGER,
    IN iProductUnitId INTEGER,
    IN iUnitPrice DECIMAL(19,2),
    IN iQuantity DOUBLE,
    IN iCost DECIMAL(19,2),
    IN iDiscount DECIMAL(19,2),
    IN iCurrency VARCHAR(4),
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO sold_product (sale_transaction_id,
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
                iUserId);
    SELECT LAST_INSERT_ID() AS sold_product_id;
END;

---

CREATE PROCEDURE AddSalePayment (
	IN iSaleTransactionId INTEGER,
    IN iAmount DECIMAL(19,2),
    IN iPaymentMethod VARCHAR(15),
    IN iCurrency VARCHAR(4),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
    INSERT INTO sale_payment (sale_transaction_id,
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
                iUserId);

    SELECT LAST_INSERT_ID() AS sale_payment_id;
END;

---

CREATE PROCEDURE AddSaleTransaction (
	IN iCustomerName VARCHAR(100),
    IN iCustomerId INTEGER,
    IN iDiscount DECIMAL(19,2),
    IN iSuspended BOOLEAN,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
    )
BEGIN
    INSERT INTO sale_transaction (customer_name,
                                    customer_id,
                                    discount,
                                    suspended,
                                    note_id,
                                    user_id)
        VALUES (NULLIF(iCustomerName, ""),
                NULLIF(iCustomerId, 0),
                IFNULL(iDiscount, 0),
                IFNULL(iSuspended, FALSE),
                NULLIF(iNoteId, 0),
                iUserId);

    SELECT LAST_INSERT_ID() AS sale_transaction_id;
END;

---

CREATE PROCEDURE ViewSaleTransactions (
    IN iFrom DATETIME,
    IN iTo DATETIME,
	IN iSuspended BOOLEAN,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT st.id AS sale_transaction_id,
            st.customer_name AS customer_name,
            st.customer_id AS customer_id,
            st.discount AS discount,
            st.suspended AS suspended,
            st.note_id AS note_id,
            (SELECT SUM(sale_payment.amount)
                FROM sale_payment
                WHERE sale_transaction_id = st.id) AS total_amount,
            note.note AS note,
            st.archived AS archived,
            st.created AS created,
            st.last_edited AS last_edited,
            st.user_id AS user_id
        FROM sale_transaction st
        LEFT JOIN note ON st.note_id = note.id
        WHERE st.suspended = IFNULL(iSuspended, FALSE)
        AND st.archived = IFNULL(iArchived, FALSE)
        AND st.created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
						AND IFNULL(iTo, CURRENT_TIMESTAMP())
        ORDER BY created ASC;
END;

---

CREATE PROCEDURE IsSaleTransactionSuspended (
	IN iTransactionId INTEGER
)
BEGIN
	SELECT suspended
        FROM sale_transaction
        WHERE archived = 0
        AND id = iTransactionId;
END;

---

CREATE PROCEDURE ArchiveSaleTransaction (
    IN iArchived BOOLEAN,
	IN iSaleTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE sale_transaction
        SET archived = IFNULL(iArchived, FALSE),
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
        WHERE id = iSaleTransactionId;
    UPDATE sold_product
        SET archived = IFNULL(iArchived, FALSE),
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
        WHERE sale_transaction_id = iSaleTransactionId;
END;

---

CREATE PROCEDURE ViewSaleCart (
	IN iTransactionId INTEGER,
    IN iSaleTransactionArchived BOOLEAN,
    IN iSoldProductArchived BOOLEAN
)
BEGIN
	SELECT sale_transaction.id AS transaction_id,
            sale_transaction.name AS customer_name,
            sale_transaction.client_id AS client_id,
		    client.phone_number AS customer_phone_number,
		    (SELECT SUM(cost)
                FROM sold_product
                WHERE sale_transaction_id = iTransactionId) AS total_cost,
                sale_transaction.suspended,
                sale_transaction.note_id,
                sale_transaction.created,
                sale_transaction.last_edited,
                sale_transaction.user_id,
                product_category.id AS product_category_id,
                product_category.category,
                sold_product.product_id,
                product.product,
                sold_product.unit_price AS unit_price,
                sold_product.quantity,
                current_product_quantity.quantity AS available_quantity,
                product_unit.id AS unit_id,
                product_unit.unit,
                product_unit.cost_price AS cost_price,
                product_unit.retail_price AS retail_price,
                sold_product.cost,
                sold_product.discount,
                sold_product.currency,
                note.note
            FROM (sold_product
                INNER JOIN sale_transaction ON sold_product.sale_transaction_id = sale_transaction.id
                INNER JOIN product ON sold_product.product_id = product.id
                INNER JOIN product_unit ON sold_product.product_id = product_unit.product_id
                INNER JOIN current_product_quantity ON sold_product.product_id = current_product_quantity.product_id)
            INNER JOIN product_category ON product.product_category_id = product_category.id
            LEFT JOIN client ON sale_transaction.client_id = client.id
            LEFT JOIN note ON sold_product.note_id = note.id
            WHERE sale_transaction.id = iTransactionId
            AND sale_transaction.archived = iSaleTransactionArchived
            AND sold_product.archived = iSoldProductArchived;
END;

---

CREATE PROCEDURE ViewSoldProducts (
	IN iTransactionId INTEGER,
    IN iSuspended BOOLEAN,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT product_category.id AS product_category_id,
            product_category.category,
            sold_product.product_id,
            sold_product.product,
		    sold_product.unit_price,
            sold_product.quantity,
            sold_product.unit_id,
		    product_unit.unit,
            sold_product.cost,
            sold_product.discount,
            sold_product.currency,
            sold_product.note_id,
            note.note,
            sold_product.archived,
            sold_product.created,
            sold_product.last_edited,
            sold_product.user_id,
            rr_user.user
        FROM sold_product
        INNER JOIN product ON sold_product.product_id = product.id
        INNER JOIN product_category ON product_category.id = product.product_category_id
        INNER JOIN product_unit ON sold_product.unit_id = product_unit.id
        INNER JOIN sale_transaction ON sale_transaction.id = sold_product.sale_transaction_id
		LEFT JOIN rr_user ON sold_product.user_id = rr_user.id
        LEFT JOIN note ON sale_transaction.note_id = note.id
        WHERE sale_transaction_id = iTransactionId
        AND sale_transaction.suspended = IFNULL(iSuspended, FALSE)
        AND sale_transaction.archived = IFNULL(iArchived, FALSE);
END;

---

CREATE PROCEDURE RevertSaleQuantityUpdate (
	IN iTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE current_product_quantity
		INNER JOIN sold_product ON current_product_quantity.product_id = sold_product.product_id
		INNER JOIN sale_transaction ON sold_product.sale_transaction_id = sale_transaction.id
        SET current_product_quantity.quantity = current_product_quantity.quantity + sold_product.quantity,
            current_product_quantity.last_edited = CURRENT_TIMESTAMP(),
            current_product_quantity.user_id = iUserId
		WHERE sale_transaction.id = iTransactionId;
END;

---

CREATE PROCEDURE FetchTotalRevenue (
	IN iFrom DATE,
    IN iTo DATE
)
BEGIN
	SELECT DATE(sale_transaction.created) AS created,
        SUM(sale_payment.amount) AS amount_paid
        FROM sale_transaction
		INNER JOIN sale_payment ON sale_payment.sale_transaction_id = sale_transaction.id
		WHERE sale_transaction.suspended = 0
        AND sale_transaction.archived = 0
		AND DATE(sale_transaction.created) BETWEEN DATE(iFrom)
                                            AND DATE(iTo)
		GROUP BY DATE(sale_transaction.created);
END;

---

CREATE PROCEDURE FetchMostSoldProducts (
	IN iFrom DATETIME,
    IN iTo DATETIME,
    IN iLimit INTEGER
)
BEGIN
	SELECT product_category.id AS product_category_id,
            product_category.category,
            sold_product.product_id,
            product.product,
		    SUM(sold_product.cost - sold_product.discount) AS total_revenue,
            SUM(sold_product.quantity) AS total_quantity
		FROM sold_product
		INNER JOIN product ON product.id = sold_product.product_id
		INNER JOIN product_category ON product_category.id = product.product_category_id
		WHERE sold_product.created BETWEEN iFrom
                                    AND iTo
		GROUP BY sold_product.product_id
		ORDER BY SUM(sold_product.quantity) DESC
		LIMIT iLimit;
END;

---

CREATE PROCEDURE ViewSaleReport (
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT p.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category,
            p.product,
            (SELECT IFNULL(SUM(quantity), 0)
                FROM sold_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
                AND sold_product.product_id = p.product_id) AS quantity_sold,
            product_unit.id AS product_unit_id, product_unit.unit,
            (SELECT IFNULL(SUM(cost), 0)
                FROM sold_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
                AND sold_product.product_id = p.id) AS total_amount
        FROM product p
        INNER JOIN product_category ON p.product_category_id = product_category.id
        INNER JOIN product_unit ON p.id = product_unit.product_id
        INNER JOIN current_product_quantity ON p.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON p.user_id = rr_user.id
        WHERE p.archived = 0
        AND product_unit.base_unit_equivalent = 1;
END;

---

CREATE PROCEDURE FilterSaleReport (
    IN iFilterColumn VARCHAR(20),
    IN iFilterText VARCHAR(100),
    IN iSortColumn VARCHAR(20),
    IN iSortOrder VARCHAR(15),
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT p.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category,
            p.product,
            (SELECT IFNULL(SUM(quantity), 0)
                FROM sold_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
                AND sold_product.product_id = p.product_id) AS quantity_sold,
            product_unit.id AS product_unit_id, product_unit.unit,
            (SELECT IFNULL(SUM(cost), 0)
                FROM sold_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
                AND sold_product.product_id = p.id) AS total_amount
        FROM product p
        INNER JOIN product_category ON p.product_category_id = product_category.id
        INNER JOIN product_unit ON p.id = product_unit.product_id
        INNER JOIN current_product_quantity ON p.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON p.user_id = rr_user.id
        WHERE p.archived = 0
        AND product_unit.base_unit_equivalent = 1
        AND product_category.category LIKE (CASE
                                            WHEN LOWER(iFilterColumn) = 'category'
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
                    AND LOWER(iSortColumn) = 'category'
                    THEN LOWER(product_category.category) END) DESC,
                 (CASE
                    WHEN (iSortOrder IS NULL AND iSortColumn IS NULL)
                    OR (LOWER(iSortOrder) <> 'descending'
                        AND LOWER(iSortColumn) = 'category')
                    THEN LOWER(product_category.category) END) ASC,
        LOWER(p.product) ASC;
END;