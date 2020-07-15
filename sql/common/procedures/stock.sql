CREATE OR REPLACE FUNCTION ViewStockProductCategories (
    IN iSortOrder VARCHAR(15),
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_category_id BIGINT, product_category VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT id AS product_category_id,
            category AS product_category
            FROM product_category
            WHERE archived = iArchived
            ORDER BY LOWER(category) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewStockProducts (
    IN iProductCategoryId BIGINT,
    IN iSortOrder VARCHAR(15)
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category VARCHAR(100),
                product VARCHAR(100), description VARCHAR(200), divisible BOOLEAN,
                image BYTEA, quantity DOUBLE PRECISION, product_unit_id BIGINT,
                product_unit VARCHAR(100), cost_price MONEY, retail_price MONEY,
                currency VARCHAR(4), created TIMESTAMP, last_edited TIMESTAMP,
                user_id BIGINT, username VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT product.id AS product_id,
        product_category.id AS product_category_id,
        product_category.category AS product_category,
        product.product AS product,
        product.description AS description,
        product.divisible AS divisible,
        product.image AS image,
        current_product_quantity.quantity AS quantity,
        product_unit.id AS product_unit_id,
        product_unit.unit AS product_unit,
        product_unit.cost_price AS cost_price,
        product_unit.retail_price AS retail_price,
        product_unit.currency AS currency,
        product.created AS created,
        product.last_edited AS last_edited,
        product.user_id AS user_id,
        rr_user.username AS username
    FROM product
    INNER JOIN product_category ON product.product_category_id = product_category.id
    INNER JOIN product_unit ON product.id = product_unit.product_id
    INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
    LEFT JOIN rr_user ON product.user_id = rr_user.id
    WHERE product.archived = FALSE
        AND product_unit.base_unit_equivalent = 1
        AND product_category.id = iProductCategoryId
    ORDER BY (CASE
                WHEN LOWER(iSortOrder) = 'descending'
                THEN LOWER(product.product) END) DESC,
             (CASE
              WHEN LOWER(iSortOrder) = 'ascending' OR iSortOrder IS NULL
              THEN LOWER(product.product) END) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterStockProductCategories (
    IN iFilterText VARCHAR(200),
    IN iSortOrder VARCHAR(20)
) RETURNS TABLE(product_category_id BIGINT, product_category VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT id AS product_category_id,
            category AS product_category
            FROM product_category
            WHERE product_category.category
            LIKE CONCAT('%', iFilterText, '%')
            ORDER BY (CASE WHEN LOWER(iSortOrder) = 'descending'
                        THEN LOWER(product_category.category) END) DESC,
                    (CASE WHEN LOWER(iSortOrder) <> 'descending' OR iSortOrder IS NULL
                        THEN LOWER(product_category.category) END) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterStockProductCategoriesByProduct (
    IN iFilterText VARCHAR(200),
    IN iSortOrder VARCHAR(20)
) RETURNS TABLE(product_category_id BIGINT, product_category VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT id AS product_category_id,
            category AS product_category
    FROM product_category
    INNER JOIN (SELECT product.product_category_id FROM product
                    INNER JOIN product_category ON product.product_category_id = product_category.id
                    WHERE product.archived = FALSE
                        AND product.product LIKE CONCAT('%', iFilterText, '%')
                    ORDER BY (CASE WHEN LOWER(iSortOrder) = 'descending'
                                THEN LOWER(product.product) END) DESC,
                            (CASE WHEN (iSortOrder IS NULL) OR (LOWER(iSortOrder) <> 'descending')
                                THEN LOWER(product.product) END) ASC) pc
        ON pc.product_category_id = product_category.id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterStockProducts (
    IN iFilterText VARCHAR(200),
    IN iSortOrder VARCHAR(20),
    IN iProductCategoryId BIGINT
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category VARCHAR(100),
                product VARCHAR(100), description VARCHAR(200), divisible BOOLEAN,
                image BYTEA, quantity DOUBLE PRECISION, product_unit_id BIGINT,
                product_unit VARCHAR(100), cost_price MONEY, retail_price MONEY,
                currency VARCHAR(4), created TIMESTAMP, last_edited TIMESTAMP,
                user_id BIGINT, username VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT product.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            product.product AS product,
            product.description AS description,
            product.divisible AS divisible,
            product.image AS image,
            current_product_quantity.quantity AS quantity,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            product_unit.cost_price AS cost_price,
            product_unit.retail_price AS retail_price,
            product_unit.currency AS currency,
            product.created AS created,
            product.last_edited AS last_edited,
            product.user_id AS user_id,
            rr_user.username AS username
    FROM product
    INNER JOIN product_category ON product.product_category_id = product_category.id
    INNER JOIN product_unit ON product.id = product_unit.product_id
    INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
    LEFT JOIN rr_user ON product.user_id = rr_user.id
    WHERE product.archived = FALSE AND product_unit.base_unit_equivalent = 1
    AND product_category.id = iProductCategoryId
    AND product.product LIKE CONCAT('%', iFilterText, '%')
    ORDER BY (CASE WHEN LOWER(iSortOrder) = 'descending'
                THEN LOWER(product.product) END) DESC,
             (CASE WHEN (iSortOrder IS NULL)
                OR (LOWER(iSortOrder) <> 'descending')
                THEN LOWER(product.product) END) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchStockProductCount (
    IN iProductCategoryId BIGINT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_count BIGINT)
AS $$
BEGIN
    IF iProductCategoryId IS NULL OR iProductCategoryId < 1 THEN
        RETURN QUERY SELECT COUNT(product.id) AS product_count
            FROM product
            INNER JOIN product_category ON product.product_category_id = product_category.id
            LEFT JOIN rr_user ON product.user_id = rr_user.id
            WHERE product.archived = iArchived;
    ELSE
        RETURN QUERY SELECT COUNT(product.id) AS product_count
            FROM product
            INNER JOIN product_category ON product.product_category_id = product_category.id
            LEFT JOIN rr_user ON product.user_id = rr_user.id
            WHERE product.archived = iArchived
            AND product_category.id = iProductCategoryId;
    END IF;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterStockProductCount (
    IN iFilterColumn VARCHAR(50),
    IN iFilterText VARCHAR(200),
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_count BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT COUNT(product.id) AS product_count
    FROM product
    INNER JOIN product_category ON product.product_category_id = product_category.id
    WHERE product.archived = iArchived
        AND product_category.category LIKE (CASE
                                            WHEN LOWER(iFilterColumn) = 'product_category'
                                            THEN CONCAT('%', iFilterText, '%')
                                            ELSE '%'
                                            END)
        AND product.product LIKE (CASE
                                    WHEN LOWER(iFilterColumn) = 'product'
                                    THEN CONCAT('%', iFilterText, '%')
                                    ELSE '%'
                                    END);
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddStockProductQuantity (
    IN iProductId BIGINT,
    IN iQuantity DOUBLE PRECISION,
    IN iReason VARCHAR(200),
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO initial_product_quantity (product_id,
                                            quantity,
                                            reason,
                                            user_id)
    SELECT iProductId,
                quantity,
                iReason,
                iUserId
        FROM current_product_quantity
        WHERE product_id = iProductId;

    UPDATE current_product_quantity 
        SET quantity = quantity + iQuantity,
            user_id = iUserId
		WHERE product_id = iProductId
    RETURNING id AS current_product_quantity_id;
$$LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION DeductStockProductQuantity (
    IN iProductId BIGINT,
    IN iQuantity DOUBLE PRECISION,
    IN iReason VARCHAR(200),
    IN iUserId BIGINT
) RETURNS TABLE(initial_product_quantity_id BIGINT)
AS $$
DECLARE availableQuantity DOUBLE PRECISION := 0.0;
BEGIN
    SELECT quantity INTO availableQuantity FROM current_product_quantity
    WHERE product_id = iProductId;

    IF availableQuantity < iQuantity THEN
        RAISE EXCEPTION 'Available quantity is too low to make deduction.';
    END IF;

    UPDATE current_product_quantity
        SET quantity = availableQuantity - iQuantity,
            user_id = iUserId
    WHERE product_id = iProductId;

    RETURN QUERY INSERT INTO initial_product_quantity (product_id,
                                                        quantity,
                                                        reason,
                                                        user_id)
        VALUES (iProductId,
                availableQuantity,
                iReason,
                iUserId)
    RETURNING id AS current_product_quantity;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchStockProduct (
    IN iProductId BIGINT
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category VARCHAR(100),
                product VARCHAR(100), description VARCHAR(200), divisible BOOLEAN,
                image BYTEA, quantity DOUBLE PRECISION, product_unit_id BIGINT,
                product_unit VARCHAR(100), cost_price MONEY, retail_price MONEY,
                currency VARCHAR(4), created TIMESTAMP, last_edited TIMESTAMP,
                user_id BIGINT, username VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT product.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            product.product AS product,
            product.description AS description,
            product.divisible AS divisible,
            product.image AS image,
            current_product_quantity.quantity AS quantity,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit,
            product_unit.cost_price AS cost_price,
            product_unit.retail_price AS retail_price,
            product_unit.currency AS currency,
            product.created AS created,
            product.last_edited AS last_edited,
            product.user_id AS user_id,
            rr_user.username AS username
    FROM product
    INNER JOIN product_category ON product.product_category_id = product_category.id
    INNER JOIN product_unit ON product.id = product_unit.product_id
    INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
    LEFT JOIN rr_user ON product.user_id = rr_user.id
    WHERE product.archived = FALSE AND product_unit.base_unit_equivalent = 1
        AND product.id = iProductId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddOrUpdateStockProductCategory (
    IN iCategory VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO product_category (category,
                                        short_form,
                                        note_id,
                                        user_id)
    VALUES (iCategory,
                iShortForm,
                NULLIF(iNoteId, 0),
                iUserId)
    ON CONFLICT(category) DO UPDATE
        SET category = iCategory
    RETURNING id AS product_category_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddStockProduct (
    IN iProductCategoryId BIGINT,
    IN iProduct VARCHAR(200),
    IN iShortForm VARCHAR(10),
    IN iDescription VARCHAR(200),
    IN iBarcode VARCHAR(50),
    IN iDivisible BOOLEAN,
    IN iImage BYTEA,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS TABLE(product_id BIGINT)
AS $$
DECLARE productAlreadyExists BOOLEAN := FALSE;
BEGIN
    SELECT EXISTS(SELECT id FROM product
        WHERE LOWER(product) = LOWER(iProduct)
            AND archived = FALSE) INTO productAlreadyExists;
    IF productAlreadyExists = TRUE THEN
        RAISE EXCEPTION 'Product already exists.';
    END IF;

    INSERT INTO product (product_category_id,
                            product,
                            short_form,
                            description,
                            barcode,
                            divisible,
                            image,
                            note_id,
                            user_id)
        VALUES (iProductCategoryId,
                iProduct,
                iShortForm,
                iDescription,
                iBarcode,
                iDivisible,
                iImage,
                NULLIF(iNoteId, 0),
                iUserId);

    RETURN QUERY SELECT MAX(id) AS product_id FROM product;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddStockProductUnit (
    IN iProductId BIGINT,
    IN iUnit VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iBaseUnitEquivalent BIGINT,
    IN iCostPrice MONEY,
    IN iRetailPrice MONEY,
    IN iPreferred BOOLEAN,
    IN iCurrency VARCHAR(4),
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO product_unit (product_id,
                                unit,
                                short_form,
                                base_unit_equivalent,
                                cost_price,
                                retail_price,
                                preferred,
                                currency,
                                note_id,
                                user_id)
    VALUES (iProductId,
                iUnit,
                iShortForm,
                iBaseUnitEquivalent,
                iCostPrice,
                iRetailPrice,
                iPreferred,
                iCurrency,
                NULLIF(iNoteId, 0),
                iUserId)
    RETURNING id AS product_unit_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddInitialProductQuantity (
    IN iProductId BIGINT,
    IN iQuantity DOUBLE PRECISION,
    IN iReason VARCHAR(50),
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO initial_product_quantity (product_id,
                                            quantity,
                                            reason,
                                            user_id)
    VALUES (iProductId,
                iQuantity,
                iReason,
                iUserId)
    RETURNING id AS initial_product_quantity_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddCurrentProductQuantity (
    IN iProductId BIGINT,
    IN iQuantity DOUBLE PRECISION,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO current_product_quantity (product_id,
                                            quantity,
                                            user_id)
    VALUES (iProductId,
                iQuantity,
                iUserId)
    RETURNING id AS current_product_quantity_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION FetchStockProductCategoryId (
    IN iProductId BIGINT
) RETURNS BIGINT
AS $$
    SELECT product.product_category_id AS product_category_id
    FROM product
    WHERE product.id = iProductId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION UpdateStockProduct (
    IN iProductCategoryId BIGINT,
    IN iProductId BIGINT,
    IN iProduct VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iDescription VARCHAR(200),
    IN iBarcode VARCHAR(50),
    IN iDivisible BOOLEAN,
    IN iImage BYTEA,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE product
        SET product_category_id = iProductCategoryId,
            product = iProduct,
            short_form = iShortForm,
            description = iDescription,
            barcode = iBarcode,
            divisible = iDivisible,
            image = iImage,
            note_id = NULLIF(iNoteId, 0),
            user_id = iUserId
    WHERE product.id = iProductId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION UpdateStockProductUnit (
    IN iProductId BIGINT,
    IN iUnit VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iBaseUnitEquivalent BIGINT,
    IN iCostPrice MONEY,
    IN iRetailPrice MONEY,
    IN iPreferred BOOLEAN,
    IN iCurrency VARCHAR(4),
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE product_unit
        SET unit = iUnit,
            short_form = iShortForm,
            base_unit_equivalent = iBaseUnitEquivalent,
            cost_price = iCostPrice,
            retail_price = iRetailPrice,
            preferred = iPreferred,
            currency = iCurrency,
            note_id = iNoteId,
            user_id = iUserId
    WHERE product_id = iProductId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveStockProduct (
    IN iArchived BOOLEAN,
    IN iProductId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
DECLARE productCategoryId BIGINT := 0;
BEGIN
    UPDATE product
        SET archived = iArchived,
            user_id = iUserId
    WHERE id = iProductId;

    SELECT product_category_id
        INTO productCategoryId
    FROM product
    WHERE id = iProductId;

    UPDATE product_category
        SET archived = NOT EXISTS(SELECT archived
                                    FROM product
                                    WHERE product_category_id = productCategoryId
                                        AND archived = FALSE
                                    LIMIT 1),
            user_id = iUserId
    WHERE id = productCategoryId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewStockReport (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category VARCHAR(100),
                product VARCHAR(100), opening_stock_quantity DOUBLE PRECISION, quantity_sold DOUBLE PRECISION,
                quantity_bought DOUBLE PRECISION, quantity_in_stock DOUBLE PRECISION, product_unit_id BIGINT,
                product_unit VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT p.id AS product_id,
        product_category.id AS product_category_id,
        product_category.category AS product_category,
        p.product AS product,
        (SELECT COALESCE(quantity, 0)
            FROM initial_product_quantity
            WHERE created BETWEEN iFrom AND iTo
            AND initial_product_quantity.product_id = p.id
            ORDER BY created ASC
            LIMIT 1) AS opening_stock_quantity,
        (SELECT COALESCE(SUM(quantity), 0)
            FROM sold_product
            WHERE created BETWEEN iFrom AND iTo
            AND sold_product.product_id = p.id) AS quantity_sold,
        (SELECT COALESCE(SUM(quantity), 0)
            FROM purchased_product
            WHERE created BETWEEN iFrom AND iTo
            AND purchased_product.product_id = p.id) AS quantity_bought,
            current_product_quantity.quantity AS quantity_in_stock,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit
    FROM product p
    INNER JOIN product_category ON p.product_category_id = product_category.id
    INNER JOIN product_unit ON p.id = product_unit.product_id
    INNER JOIN current_product_quantity ON p.id = current_product_quantity.product_id
    LEFT JOIN rr_user ON p.user_id = rr_user.id
    WHERE p.archived = FALSE AND product_unit.base_unit_equivalent = 1;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterStockReport (
    IN iFilterColumn VARCHAR(100),
    IN iFilterText VARCHAR(100),
    IN iSortColumn VARCHAR(100),
    IN iSortOrder VARCHAR(15),
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category VARCHAR(100),
                product VARCHAR(100), opening_stock_quantity DOUBLE PRECISION, quantity_sold DOUBLE PRECISION,
                quantity_bought DOUBLE PRECISION, quantity_in_stock DOUBLE PRECISION, product_unit_id BIGINT,
                product_unit VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT p.id AS product_id,
        product_category.id AS product_category_id,
        product_category.category AS product_category,
        p.product AS product,
        (SELECT COALESCE(quantity, 0)
            FROM initial_product_quantity
            WHERE created BETWEEN iFrom AND iTo
            AND initial_product_quantity.product_id = p.id
            ORDER BY created ASC
            LIMIT 1) AS opening_stock_quantity,
        (SELECT COALESCE(SUM(quantity), 0)
            FROM sold_product
            WHERE created BETWEEN iFrom AND iTo
            AND sold_product.product_id = p.id) AS quantity_sold,
        (SELECT COALESCE(SUM(quantity), 0)
            FROM purchased_product
            WHERE created BETWEEN iFrom AND iTo
            AND purchased_product.product_id = p.id) AS quantity_bought,
            current_product_quantity.quantity AS quantity_in_stock,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit
    FROM product p
    INNER JOIN product_category ON p.product_category_id = product_category.id
    INNER JOIN product_unit ON p.id = product_unit.product_id
    INNER JOIN current_product_quantity ON p.id = current_product_quantity.product_id
    LEFT JOIN rr_user ON p.user_id = rr_user.id
    WHERE p.archived = FALSE AND product_unit.base_unit_equivalent = 1
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
