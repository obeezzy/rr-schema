USE ###DATABASENAME###;

---

CREATE PROCEDURE ViewPurchaseTransactions (
    IN iFrom DATETIME,
    IN iTo DATETIME,
    IN iSuspended BOOLEAN,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT pt.id AS purchase_transaction_id,
            pt.vendor_name AS vendor_name,
            pt.vendor_id AS vendor_id,
            pt.discount AS discount,
            pt.suspended AS suspended,
            pt.note_id AS note_id,
            (SELECT SUM(purchase_payment.amount)
                FROM purchase_payment
                WHERE purchase_transaction_id = pt.id) AS total_amount,
            note.note AS note,
            pt.archived AS archived,
            pt.created AS created,
            pt.last_edited AS last_edited,
            pt.user_id AS user_id
        FROM purchase_transaction pt
        LEFT JOIN note ON pt.note_id = note.id
        WHERE pt.suspended = IFNULL(iSuspended, FALSE)
        AND pt.archived = IFNULL(iArchived, FALSE)
        AND pt.created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
						AND IFNULL(iTo, CURRENT_TIMESTAMP())
        ORDER BY created ASC;
END;

---

CREATE PROCEDURE AddPurchaseTransaction (
	IN iVendorName VARCHAR(100),
    IN iVendorId INTEGER,
    IN iDiscount DECIMAL(19,2),
    IN iSuspended BOOLEAN,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
    INSERT INTO purchase_transaction (vendor_name,
                                        vendor_id,
                                        discount,
                                        suspended,
                                        note_id,
                                        user_id)
        VALUES (NULLIF(iVendorName, ""),
                NULLIF(iVendorId, 0),
                iDiscount,
                IFNULL(iSuspended, FALSE),
                NULLIF(iNoteId, 0),
                iUserId);

    SELECT LAST_INSERT_ID() AS purchase_transaction_id;
END;

---

CREATE PROCEDURE AddPurchasePayment (
	IN iPurchaseTransactionId INTEGER,
    IN iAmount DECIMAL(19,2),
    IN iPaymentMethod VARCHAR(15),
    IN iCurrency VARCHAR(4),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO purchase_payment (purchase_transaction_id,
                                    amount,
                                    payment_method,
                                    currency,
                                    note_id,
                                    user_id)
        VALUES (iPurchaseTransactionId,
                iAmount,
                iPaymentMethod,
                iCurrency,
                NULLIF(iNoteId, 0),
                iUserId);

    SELECT LAST_INSERT_ID() AS purchase_payment_id;
END;

---

CREATE PROCEDURE AddPurchasedProduct (
	IN iPurchaseTransactionId INTEGER,
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
	INSERT INTO purchased_product (purchase_transaction_id,
                                    product_id,
                                    product_unit_id,
                                    unit_price,
                                    quantity,
                                    cost,
                                    discount,
                                    currency,
                                    user_id)
        VALUES (iPurchaseTransactionId,
                iProductId,
                iProductUnitId,
                iUnitPrice,
                iQuantity,
                iCost,
                iDiscount,
                iCurrency,
                iUserId);

    SELECT LAST_INSERT_ID() AS purchased_product_id;
END;

---

CREATE PROCEDURE IsPurchaseTransactionSuspended (
	IN iPurchaseTransactionId INTEGER
)
BEGIN
	SELECT suspended
        FROM purchase_transaction
        WHERE archived = FALSE
        AND id = iPurchaseTransactionId;
END;

---

CREATE PROCEDURE RevertPurchaseQuantityUpdate (
	IN iPurchaseTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE current_product_quantity
		INNER JOIN purchased_product ON current_product_quantity.product_id = purchased_product.product_id
		INNER JOIN purchase_transaction ON purchased_product.purchase_transaction_id = purchase_transaction.id
        SET current_product_quantity.quantity = current_product_quantity.quantity - purchased_product.quantity,
            current_product_quantity.user_id = iUserId
		WHERE purchase_transaction.id = iPurchaseTransactionId;
END;

---

CREATE PROCEDURE ViewPurchaseTransactionProducts (
	IN iPurchaseTransactionId INTEGER,
    IN iSuspended BOOLEAN,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT product_category.id AS product_category_id,
            product_category.category AS product_category,
            purchased_product.product_id AS product_id,
            product.product AS product,
		    purchased_product.unit_price AS unit_price,
            purchased_product.quantity AS quantity,
            purchased_product.product_unit_id AS product_unit_id,
		    product_unit.unit AS product_unit,
            purchased_product.cost AS cost,
            purchased_product.discount AS discount,
            purchased_product.currency AS currency,
            purchased_product.note_id AS note_id,
            note.note AS note,
            purchased_product.archived AS archived,
            purchased_product.created AS created,
            purchased_product.last_edited AS last_edited,
            purchased_product.user_id AS user_id,
            rr_user.user AS user
        FROM purchased_product
        INNER JOIN product ON purchased_product.product_id = product.id
        INNER JOIN product_category ON product_category.id = product.product_category_id
        INNER JOIN product_unit ON purchased_product.product_unit_id = product_unit.id
        INNER JOIN purchase_transaction ON purchase_transaction.id = purchased_product.purchase_transaction_id
		LEFT JOIN rr_user ON purchased_product.user_id = rr_user.id
        LEFT JOIN note ON purchase_transaction.note_id = note.id
        WHERE purchase_transaction_id = iPurchaseTransactionId
        AND purchase_transaction.suspended = IFNULL(iSuspended, FALSE)
        AND purchase_transaction.archived = IFNULL(iArchived, FALSE);
END;

---

CREATE PROCEDURE ViewPurchaseCart (
	IN iPurchaseTransactionId INTEGER,
    IN iPurchaseTransactionArchived BOOLEAN,
    IN iPurchasedProductArchived BOOLEAN
)
BEGIN
	SELECT purchase_transaction.id AS purchase_transaction_id,
            purchase_transaction.vendor_name AS vendor_name,
            purchase_transaction.vendor_id AS vendor_id,
            client.phone_number AS vendor_phone_number,
            purchase_transaction.suspended AS suspended,
            purchase_transaction.note_id AS note_id,
            note.note AS note,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            purchased_product.product_id AS product_id,
            product.product AS product,
            purchased_product.unit_price AS unit_price,
            purchased_product.quantity AS quantity,
            current_product_quantity.quantity AS available_quantity,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            product_unit.cost_price AS cost_price,
            product_unit.retail_price AS retail_price,
            purchased_product.cost AS cost,
            purchased_product.discount AS discount,
            purchased_product.currency AS currency,
            purchase_transaction.created AS created,
            purchase_transaction.last_edited AS last_edited,
            purchase_transaction.user_id AS user_id
        FROM purchased_product
        INNER JOIN purchase_transaction ON purchased_product.purchase_transaction_id = purchase_transaction.id
        INNER JOIN product ON purchased_product.product_id = product.id
        INNER JOIN product_unit ON purchased_product.product_id = product_unit.product_id
        INNER JOIN current_product_quantity ON purchased_product.product_id = current_product_quantity.product_id
        INNER JOIN product_category ON product.product_category_id = product_category.id
        LEFT JOIN vendor ON purchase_transaction.vendor_id = vendor.id
        LEFT JOIN client ON vendor.client_id = client.id
        LEFT JOIN note ON purchase_transaction.note_id = note.id
        WHERE purchase_transaction.id = iPurchaseTransactionId
        AND purchase_transaction.archived = IFNULL(iPurchaseTransactionArchived, FALSE)
        AND purchased_product.archived = IFNULL(iPurchasedProductArchived, FALSE);
END;

---

CREATE PROCEDURE ArchivePurchaseTransaction (
    IN iArchived BOOLEAN,
	IN iPurchaseTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE purchase_transaction
        SET archived = IFNULL(iArchived, FALSE),
            user_id = iUserId
        WHERE id = iPurchaseTransactionId;
END;

---

CREATE PROCEDURE UndoRevertPurchaseQuantityUpdate (
	IN iPurchaseTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE current_product_quantity
		INNER JOIN purchased_product ON current_product_quantity.product_id = purchased_product.product_id
		INNER JOIN purchase_transaction ON purchased_product.purchase_transaction_id = purchase_transaction.id
        SET current_product_quantity.quantity = current_product_quantity.quantity + purchased_product.quantity,
            current_product_quantity.user_id = iUserId
		WHERE purchase_transaction.id = iPurchaseTransactionId;
END;

---

CREATE PROCEDURE ViewPurchaseReport (
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT product_category.id AS product_category_id,
            product_category.category AS product_category,
            p.id AS product_id,
            p.product AS product,
            (SELECT IFNULL(SUM(quantity), 0)
                FROM purchased_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND purchased_product.product_id = p.id) AS quantity_bought,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
        (SELECT IFNULL(SUM(cost), 0)
            FROM purchased_product
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                            AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND purchased_product.product_id = p.id) AS total_expenditure
        FROM product p
        INNER JOIN product_category ON p.product_category_id = product_category.id
        INNER JOIN product_unit ON p.id = product_unit.product_id
        INNER JOIN current_product_quantity ON p.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON p.user_id = rr_user.id
        WHERE p.archived = FALSE
        AND product_unit.base_unit_equivalent = 1;
END;

---

CREATE PROCEDURE FilterPurchaseReport (
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
            product_category.category AS product_category,
            p.product AS product,
            (SELECT IFNULL(SUM(quantity), 0)
                FROM purchased_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND purchased_product.product_id = p.id) AS quantity_bought,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            (SELECT IFNULL(SUM(cost), 0)
                FROM purchased_product
                WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                AND IFNULL(iTo, CURRENT_TIMESTAMP())
                AND purchased_product.product_id = p.id) AS total_expenditure
        FROM product p
        INNER JOIN product_category ON p.product_category_id = product_category.id
        INNER JOIN product_unit ON p.id = product_unit.product_id
        INNER JOIN current_product_quantity ON p.id = current_product_quantity.product_id
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
                    WHEN (iSortOrder IS NULL
                        AND iSortColumn IS NULL)
                    OR (LOWER(iSortOrder) <> 'descending'
                        AND LOWER(iSortColumn) = 'product_category')
                    THEN LOWER(product_category.category) END) ASC,
        LOWER(p.product) ASC;
END;