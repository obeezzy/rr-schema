CREATE OR REPLACE FUNCTION ViewProductCategories (
    IN iSortOrder TEXT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_category_id BIGINT, product_category TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT product_category.id AS product_category_id,
            product_category.category AS product_category
            FROM product_category
            WHERE product_category.archived = iArchived
            ORDER BY LOWER(product_category.category) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewProducts (
    IN iProductCategoryId BIGINT,
    IN iSortOrder TEXT DEFAULT 'ascending'
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
                product TEXT, description TEXT, divisible BOOLEAN,
                image BYTEA, quantity REAL, product_unit_id BIGINT,
                product_unit TEXT, cost_price NUMERIC(19,2), retail_price NUMERIC(19,2),
                currency VARCHAR(4), created TIMESTAMP, last_edited TIMESTAMP,
                user_id BIGINT, username TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT product.id AS product_id,
        product_category.id AS product_category_id,
        product_category.category AS product_category,
        product.product AS product,
        product.description AS description,
        product.divisible AS divisible,
        product.image AS image,
        product_quantity.quantity AS quantity,
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
    INNER JOIN product_quantity ON product.id = product_quantity.product_id
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

CREATE OR REPLACE FUNCTION FilterProductCategories (
    IN iFilterText TEXT,
    IN iSortOrder TEXT DEFAULT 'ascending'
) RETURNS TABLE(product_category_id BIGINT, product_category TEXT)
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

CREATE OR REPLACE FUNCTION FilterProducts (
    IN iFilterText TEXT,
    IN iProductCategoryId BIGINT,
    IN iSortOrder TEXT DEFAULT 'ascending'
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
                product TEXT, description TEXT, divisible BOOLEAN,
                image BYTEA, quantity REAL, product_unit_id BIGINT,
                product_unit TEXT, cost_price NUMERIC(19,2), retail_price NUMERIC(19,2),
                currency VARCHAR(4), created TIMESTAMP, last_edited TIMESTAMP,
                user_id BIGINT, username TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT product.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            product.product AS product,
            product.description AS description,
            product.divisible AS divisible,
            product.image AS image,
            product_quantity.quantity AS quantity,
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
    INNER JOIN product_quantity ON product.id = product_quantity.product_id
    LEFT JOIN rr_user ON product.user_id = rr_user.id
    WHERE product.archived = FALSE AND product_unit.base_unit_equivalent = 1
    AND product_category.id = product_category_id
    AND product.product LIKE CONCAT('%', iFilterText, '%')
    ORDER BY (CASE WHEN LOWER(iSortOrder) = 'descending'
                THEN LOWER(product.product) END) DESC,
             (CASE WHEN (iSortOrder IS NULL)
                OR (LOWER(iSortOrder) <> 'descending')
                THEN LOWER(product.product) END) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchProductCount (
    IN iProductCategory BIGINT DEFAULT NULL,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_count BIGINT)
AS $$
BEGIN
    IF iProductCategory IS NULL THEN
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
            AND product_category.id = iProductCategory;
    END IF;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterProductCount (
    IN iFilterText TEXT,
    IN iFilterColumn TEXT DEFAULT 'product',
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(product_count BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT COUNT(product.id) AS product_count
    FROM product
    INNER JOIN product_category ON product.product_category_id = product_category.id
    WHERE product.archived = archived
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

CREATE OR REPLACE FUNCTION AddProductQuantity (
    IN iProductId BIGINT,
    IN iQuantity REAL,
    IN iReason TEXT,
    IN iUserId BIGINT
) RETURNS TABLE(product_quantity_id BIGINT)
AS $$
BEGIN
    INSERT INTO product_quantity_snapshot (product_id,
                                            quantity,
                                            reason,
                                            last_edited,
                                            user_id)
    SELECT pq.product_id,
            pq.quantity,
            iReason,
            CURRENT_TIMESTAMP,
            iUserId
    FROM product_quantity pq
    WHERE pq.product_id = iProductId;

    UPDATE product_quantity 
        SET quantity = quantity + iQuantity,
            last_edited = CURRENT_TIMESTAMP,
            user_id = iUserId
		WHERE product_id = iProductId;

    RETURN QUERY SELECT MAX(id) AS product_quantity_id FROM product_quantity;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION DeductProductQuantity (
    IN iProductId BIGINT,
    IN iQuantity REAL,
    IN iReason TEXT,
    IN iUserId BIGINT
) RETURNS TABLE(new_quantity REAL)
AS $$
DECLARE vAvailableQuantity REAL := 0.0;
BEGIN
    SELECT product_quantity.quantity INTO vAvailableQuantity
    FROM product_quantity
    WHERE product_quantity.product_id = iProductId;

    IF vAvailableQuantity < iQuantity THEN
        RAISE EXCEPTION 'Available quantity is too low to make deduction.';
    END IF;

    INSERT INTO product_quantity_snapshot (product_id,
                                            quantity,
                                            reason,
                                            last_edited,
                                            user_id)
    VALUES (iProductId,
            vAvailableQuantity,
            iReason,
            CURRENT_TIMESTAMP,
            iUserId);

    RETURN QUERY UPDATE product_quantity
        SET quantity = vAvailableQuantity - iQuantity,
            user_id = iUserId
    WHERE product_quantity.product_id = iProductId
    RETURNING quantity AS new_quantity;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchProduct (
    IN iProductId BIGINT
) RETURNS TABLE(product_id BIGINT,
                product_category_id BIGINT,
                product_category TEXT,
                product TEXT,
                description TEXT,
                divisible BOOLEAN,
                image BYTEA,
                quantity REAL,
                product_unit_id BIGINT,
                product_unit TEXT,
                cost_price NUMERIC(19,2),
                retail_price NUMERIC(19,2),
                currency VARCHAR(4),
                created TIMESTAMP,
                last_edited TIMESTAMP,
                user_id BIGINT,
                username TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT product.id AS product_id,
            product_category.id AS product_category_id,
            product_category.category AS product_category,
            product.product AS product,
            product.description AS description,
            product.divisible AS divisible,
            product.image AS image,
            product_quantity.quantity AS quantity,
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
    INNER JOIN product_quantity ON product.id = product_quantity.product_id
    LEFT JOIN rr_user ON product.user_id = rr_user.id
    WHERE product.archived = FALSE AND product_unit.base_unit_equivalent = 1
        AND product.id = iProductId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddOrUpdateProductCategory (
    IN iCategory TEXT,
    IN iUserId BIGINT,
    IN iShortForm TEXT DEFAULT NULL,
    IN iNoteId BIGINT DEFAULT NULL
) RETURNS TABLE(product_category_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO product_category (category,
                                    short_form,
                                    note_id,
                                    last_edited,
                                    user_id)
    VALUES (iCategory,
                iShortForm,
                NULLIF(iNoteId, 0),
                CURRENT_TIMESTAMP,
                iUserId)
    ON CONFLICT(category) DO UPDATE
        SET category = iCategory,
            last_edited = CURRENT_TIMESTAMP
    RETURNING id AS product_category_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddProduct (
    IN iProductCategoryId BIGINT,
    IN iProduct TEXT,
    IN iShortForm TEXT,
    IN iDescription TEXT,
    IN iBarcode TEXT,
    IN iDivisible BOOLEAN,
    IN iImage BYTEA,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS TABLE(product_id BIGINT)
AS $$
DECLARE vProductAlreadyExists BOOLEAN := FALSE;
BEGIN
    SELECT EXISTS(SELECT id FROM product
        WHERE LOWER(product.product) = LOWER(product.product)
            AND product.archived = FALSE) INTO vProductAlreadyExists;
    IF vProductAlreadyExists = TRUE THEN
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
                            last_edited,
                            user_id)
        VALUES (iProductCategoryId,
                iProduct,
                iShortForm,
                iDescription,
                iBarcode,
                iDivisible,
                iImage,
                NULLIF(iNoteId, 0),
                CURRENT_TIMESTAMP,
                iUserId);

    RETURN QUERY SELECT MAX(id) AS product_id FROM product;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddProductUnit (
    IN iProductId BIGINT,
    IN iUnit TEXT,
    IN iShortForm TEXT,
    IN iBaseUnitEquivalent BIGINT,
    IN iCostPrice NUMERIC(19,2),
    IN iRetailPrice NUMERIC(19,2),
    IN iPreferred BOOLEAN,
    IN iCurrency VARCHAR(4),
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS TABLE(product_unit_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO product_unit (product_id,
                                unit,
                                short_form,
                                base_unit_equivalent,
                                cost_price,
                                retail_price,
                                preferred,
                                currency,
                                note_id,
                                last_edited,
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
                CURRENT_TIMESTAMP,
                iUserId)
    RETURNING id AS product_unit_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchProductCategoryId (
    IN iProductId BIGINT
) RETURNS TABLE(product_category_id BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT product.product_category_id AS product_category_id
    FROM product
    WHERE product.id = iProductId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION UpdateProduct (
    IN iProductCategoryId BIGINT,
    IN iProductId BIGINT,
    IN iProduct TEXT,
    IN iShortForm TEXT,
    IN iDescription TEXT,
    IN iBarcode TEXT,
    IN iDivisible BOOLEAN,
    IN iImage BYTEA,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
BEGIN
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
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION UpdateProductUnit (
    IN iProductId BIGINT,
    IN iUnit TEXT,
    IN iShortForm TEXT,
    IN iBaseUnitEquivalent BIGINT,
    IN iCostPrice NUMERIC(19,2),
    IN iRetailPrice NUMERIC(19,2),
    IN iPreferred BOOLEAN,
    IN iCurrency VARCHAR(4),
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
BEGIN
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
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ArchiveProduct (
    IN iArchived BOOLEAN,
    IN iProductId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
DECLARE vProductCategoryId BIGINT := 0;
BEGIN
    UPDATE product
        SET archived = iArchived,
            user_id = iUserId
    WHERE id = iProductId;

    SELECT product.product_category_id
        INTO vProductCategoryId
    FROM product
    WHERE product.id = iProductId;

    UPDATE product_category
        SET archived = NOT EXISTS(SELECT product.archived
                                    FROM product
                                    WHERE product.product_category_id = vProductCategoryId
                                        AND product.archived = FALSE
                                    LIMIT 1),
            user_id = iUserId
    WHERE product_category.id = vProductCategoryId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewStockReport (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
                product TEXT, opening_stock_quantity REAL, quantity_sold REAL,
                quantity_bought REAL, quantity_in_stock REAL, product_unit_id BIGINT,
                product_unit TEXT)
AS $$
BEGIN
    RETURN QUERY WITH opening_stock_query AS (
        SELECT pqs1.product_id, pqs1.quantity
        FROM product_quantity_snapshot pqs1
        WHERE NOT EXISTS(
            SELECT pqs2.product_id, pqs2.quantity 
            FROM product_quantity_snapshot pqs2
            WHERE pqs2.id = pqs1.id AND pqs2.created > pqs1.created
        )
    ), sold_product_query AS (
        SELECT sp.product_id, SUM(sp.quantity) AS total_quantity
        FROM sold_product sp
        INNER JOIN product ON product.id = sp.product_id
        WHERE sp.created BETWEEN iFrom AND iTo 
        GROUP BY sp.product_id
    ), purchased_product_query AS (
        SELECT pp.product_id, SUM(pp.quantity) AS total_quantity
        FROM purchased_product pp
        INNER JOIN product ON product.id = pp.product_id
        WHERE pp.created BETWEEN iFrom AND iTo
        GROUP BY pp.product_id
    )
    SELECT p.id AS product_id,
        pc.id AS product_category_id,
        pc.category AS product_category,
        p.product AS product,
        osq.quantity AS opening_stock_quantity,
        CASE WHEN spq.total_quantity IS NULL
            THEN 0
            ELSE spq.total_quantity
            END AS quantity_sold,
        CASE WHEN ppq.total_quantity IS NULL
            THEN 0
            ELSE ppq.total_quantity
            END AS quantity_bought,
        pq.quantity AS quantity_in_stock,
        pu.id AS product_unit_id,
        pu.unit AS product_unit
    FROM product p
    INNER JOIN product_category pc ON p.product_category_id = pc.id
    INNER JOIN product_unit pu ON p.id = pu.product_id
    INNER JOIN product_quantity pq ON p.id = pq.product_id
    INNER JOIN opening_stock_query osq ON p.id = osq.product_id
    LEFT JOIN sold_product_query spq ON p.id = spq.product_id
    LEFT JOIN purchased_product_query ppq ON p.id = ppq.product_id
    LEFT JOIN rr_user ON p.user_id = rr_user.id
    WHERE p.archived = FALSE AND pu.base_unit_equivalent = 1;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterStockReport (
    IN iFilterText TEXT,
    IN iFilterColumn TEXT DEFAULT 'product',
    IN iSortColumn TEXT DEFAULT 'product',
    IN iSortOrder TEXT DEFAULT 'ascending',
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(product_id BIGINT, product_category_id BIGINT, product_category TEXT,
                product TEXT, opening_stock_quantity REAL, quantity_sold REAL,
                quantity_bought REAL, quantity_in_stock REAL, product_unit_id BIGINT,
                product_unit TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT p.id AS product_id,
        product_category.id AS product_category_id,
        product_category.category AS product_category,
        p.product AS product,
        (SELECT COALESCE(product_quantity_snapshot.quantity, 0)
            FROM product_quantity_snapshot
            WHERE created BETWEEN iFrom AND iTo
            AND product_quantity_snapshot.product_id = p.id
            ORDER BY created ASC
            LIMIT 1) AS opening_stock_quantity,
        (SELECT COALESCE(SUM(sold_product.quantity), 0)
            FROM sold_product
            WHERE created BETWEEN iFrom AND iTo
            AND sold_product.product_id = p.id) AS quantity_sold,
        (SELECT COALESCE(SUM(purchased_product.quantity), 0)
            FROM purchased_product
            WHERE created BETWEEN iFrom AND iTo
            AND purchased_product.product_id = p.id) AS quantity_bought,
            product_quantity.quantity AS quantity_in_stock,
            product_unit.id AS product_unit_id,
            product_unit.unit AS product_unit
    FROM product p
    INNER JOIN product_category ON p.product_category_id = product_category.id
    INNER JOIN product_unit ON p.id = product_unit.product_id
    INNER JOIN product_quantity ON p.id = product_quantity.product_id
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
