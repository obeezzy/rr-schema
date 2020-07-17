CREATE OR REPLACE FUNCTION ViewPurchaseTransactions (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IN iSuspended BOOLEAN DEFAULT FALSE,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(purchase_transaction_id BIGINT, vendor_name TEXT, vendor_id BIGINT,
                discount NUMERIC(19,2), suspended BOOLEAN, note_id BIGINT,
                total_amount NUMERIC(19,2), note TEXT, archived BOOLEAN,
                created TIMESTAMP, last_edited TIMESTAMP, user_id BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT pt.id AS purchase_transaction_id,
        pt.vendor_name AS vendor_name,
        pt.vendor_id AS vendor_id,
        pt.discount AS discount,
        pt.suspended AS suspended,
        pt.note_id AS note_id,
        (SELECT SUM(purchase_payment.amount)
            FROM purchase_payment
            WHERE purchase_payment.purchase_transaction_id = pt.id) AS total_amount,
        note.note AS note,
        pt.archived AS archived,
        pt.created AS created,
        pt.last_edited AS last_edited,
        pt.user_id AS user_id
    FROM purchase_transaction pt
    LEFT JOIN note ON pt.note_id = note.id
    WHERE pt.suspended = iSuspended
        AND pt.archived = iArchived
        AND pt.created BETWEEN iFrom AND iTo
    ORDER BY created ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddPurchaseTransaction (
    IN iVendorName TEXT,
    IN iVendorId BIGINT,
    IN iDiscount NUMERIC(19,2),
    IN iSuspended BOOLEAN,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO purchase_transaction (vendor_name,
                                        vendor_id,
                                        discount,
                                        suspended,
                                        note_id,
                                        user_id)
    VALUES (NULLIF(iVendorName, ''),
            NULLIF(iVendorId, 0),
            iDiscount,
            iSuspended,
            NULLIF(iNoteId, 0),
            iUserId)
    RETURNING id AS purchase_transaction_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddPurchasePayment (
    IN iPurchaseTransactionId BIGINT,
    IN iAmount NUMERIC(19,2),
    IN iPaymentMethod PAYMENT_METHOD,
    IN iCurrency TEXT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
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
                iUserId)
    RETURNING id AS purchase_payment_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddPurchasedProduct (
    IN iPurchaseTransactionId BIGINT,
    IN iProductId BIGINT,
    IN iProductUnitId BIGINT,
    IN iQuantity REAL,
    IN iUnitPrice NUMERIC(19,2),
    IN iCost NUMERIC(19,2),
    IN iDiscount NUMERIC(19,2),
    IN iCurrency TEXT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
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
                iUserId)
    RETURNING id AS purchased_product_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION IsPurchaseTransactionSuspended (
    IN iPurchaseTransactionId BIGINT
) RETURNS BOOLEAN 
AS $$
    SELECT suspended
        FROM purchase_transaction WHERE archived = FALSE
        AND id = iPurchaseTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION RevertPurchaseQuantityUpdate (
    IN iPurchaseTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE product_quantity AS cpq
        SET quantity = cpq.quantity - pp.quantity,
            user_id = iUserId
        FROM purchased_product pp, purchase_transaction pt
        WHERE cpq.product_id = pp.product_id
            AND pp.purchase_transaction_id = pt.id
            AND pt.id = iPurchaseTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ViewPurchaseTransactionProducts (
    IN iPurchaseTransactionId BIGINT,
    IN iSuspended BOOLEAN DEFAULT FALSE,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_category_id BIGINT, product_category TEXT, product_id BIGINT,
                product TEXT, quantity REAL, unit_price NUMERIC(19,2),
                product_unit_id BIGINT, product_unit TEXT, cost NUMERIC(19,2),
                discount NUMERIC(19,2), currency TEXT, note_id BIGINT,
                note TEXT, archived BOOLEAN, created TIMESTAMP,
                last_edited TIMESTAMP, user_id BIGINT, username TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT product_category.id AS product_category_id,
        product_category.category AS product_category,
        purchased_product.product_id AS product_id,
        product.product AS product,
        purchased_product.quantity AS quantity,
        purchased_product.unit_price AS unit_price,
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
        rr_user.username AS username
    FROM purchased_product
    INNER JOIN product ON purchased_product.product_id = product.id
    INNER JOIN product_category ON product_category.id = product.product_category_id
    INNER JOIN product_unit ON purchased_product.product_unit_id = product_unit.id
    INNER JOIN purchase_transaction ON purchase_transaction.id = purchased_product.purchase_transaction_id
    LEFT JOIN rr_user ON purchased_product.user_id = rr_user.id
    LEFT JOIN note ON purchase_transaction.note_id = note.id
    WHERE purchase_transaction_id = iPurchaseTransactionId
        AND purchase_transaction.suspended = iSuspended
        AND purchase_transaction.archived = iArchived;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewPurchaseCart (
    IN iPurchaseTransactionId BIGINT,
    IN iPurchaseTransactionArchived BOOLEAN,
    IN iPurchasedProductArchived BOOLEAN
) RETURNS TABLE(purchase_transaction_id BIGINT, vendor_name TEXT, vendor_id BIGINT,
                vendor_phone_number TEXT, suspended BOOLEAN, note_id BIGINT,
                note TEXT, product_category_id BIGINT, product_category TEXT,
                product_id BIGINT, product TEXT, unit_price NUMERIC(19,2),
                quantity REAL, available_quantity REAL, product_unit_id BIGINT,
                product_unit TEXT, cost_price NUMERIC(19,2), retail_price NUMERIC(19,2),
                cost NUMERIC(19,2), discount NUMERIC(19,2), currency TEXT,
                created TIMESTAMP, last_edited TIMESTAMP, user_id BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT purchase_transaction.id AS purchase_transaction_id,
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
            product_quantity.quantity AS available_quantity,
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
    INNER JOIN product_quantity ON purchased_product.product_id = product_quantity.product_id
    INNER JOIN product_category ON product.product_category_id = product_category.id
    LEFT JOIN vendor ON purchase_transaction.vendor_id = vendor.id
    LEFT JOIN client ON vendor.client_id = client.id
    LEFT JOIN note ON purchase_transaction.note_id = note.id
    WHERE purchase_transaction.id = iPurchaseTransactionId
        AND purchase_transaction.archived = iPurchaseTransactionArchived
        AND purchased_product.archived = iPurchasedProductArchived
    ORDER BY purchased_product.id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ArchivePurchaseTransaction (
    IN iArchived BOOLEAN,
    IN iPurchaseTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
	UPDATE purchase_transaction
        SET archived = iArchived,
            user_id = iUserId
        WHERE id = iPurchaseTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION UndoRevertPurchaseQuantityUpdate (
    IN iPurchaseTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE product_quantity AS cpq
        SET quantity = cpq.quantity + pp.quantity,
            user_id = iUserId
        FROM purchased_product pp, purchase_transaction pt
        WHERE cpq.product_id = pp.product_id
        AND pp.purchase_transaction_id = pt.id
        AND pt.id = iPurchaseTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ViewPurchaseReport (
    IN iFrom TIMESTAMP DEFAULT '1970-01-01 00:00:00',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_category_id BIGINT, product_category TEXT, product_id BIGINT,
                product TEXT, quantity_bought REAL, product_unit_id BIGINT,
                product_unit TEXT, total_expenditure NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT product_category.id AS product_category_id,
            product_category.category AS product_category,
            p.id AS product_id,
            p.product AS product,
            (SELECT COALESCE(SUM(quantity), 0)
                FROM purchased_product
                WHERE created BETWEEN iFrom AND iTo
            AND purchased_product.product_id = p.id) AS quantity_bought,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
        (SELECT COALESCE(SUM(cost), '0.00')
            FROM purchased_product
            WHERE created BETWEEN iFrom AND iTo
            AND purchased_product.product_id = p.id) AS total_expenditure
    FROM product p
    INNER JOIN product_category ON p.product_category_id = product_category.id
    INNER JOIN product_unit ON p.id = product_unit.product_id
    INNER JOIN product_quantity ON p.id = product_quantity.product_id
    LEFT JOIN rr_user ON p.user_id = rr_user.id
    WHERE p.archived = FALSE
        AND product_unit.base_unit_equivalent = 1
    ORDER BY p.id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterPurchaseReport (
    IN iFilterColumn TEXT,
    IN iFilterText TEXT,
    IN iSortColumn TEXT,
    IN iSortOrder TEXT,
    IN iFrom TIMESTAMP DEFAULT '1970-01-01 00:00:00',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
                product TEXT, quantity_bought REAL, product_unit_id BIGINT,
                product_unit TEXT, total_expenditure NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT p.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            p.product AS product,
            (SELECT SUM(quantity)
                FROM purchased_product
                WHERE created BETWEEN iFrom AND iTo
            AND purchased_product.product_id = p.id) AS quantity_bought,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            (SELECT SUM(cost)
                FROM purchased_product
                WHERE created BETWEEN iFrom AND iTo
                AND purchased_product.product_id = p.id) AS total_expenditure
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
                    WHEN (iSortOrder IS NULL
                        AND iSortColumn IS NULL)
                    OR (LOWER(iSortOrder) <> 'descending'
                        AND LOWER(iSortColumn) = 'product_category')
                    THEN LOWER(product_category.category) END) ASC,
        LOWER(p.product) ASC;
END
$$ LANGUAGE plpgsql;
