USE ###DATABASENAME###;

---

CREATE PROCEDURE ViewStockProductCategories (
    IN iSortOrder VARCHAR(20),
    IN iArchived BOOLEAN
)
BEGIN
    IF LOWER(iSortOrder) = "descending" THEN
        SELECT id AS product_category_id,
                category AS product_category
                FROM product_category
                WHERE archived = IFNULL(iArchived, FALSE)
                ORDER BY LOWER(category) DESC;
    ELSE
        SELECT id AS product_category_id,
                category AS product_category
                FROM product_category
                WHERE archived = iArchived
                ORDER BY LOWER(category) ASC;
    END IF;
END;

---

CREATE PROCEDURE ViewStockProducts (
    IN iProductCategoryId INTEGER,
    IN iSortOrder VARCHAR(20)
)
BEGIN
    SELECT product.id AS product_id,
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
        rr_user.user AS user
        FROM product
        INNER JOIN product_category ON product.product_category_id = product_category.id
        INNER JOIN product_unit ON product.id = product_unit.product_id
        INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON product.user_id = rr_user.id
        WHERE product.archived = FALSE AND product_unit.base_unit_equivalent = 1
        AND product_category.id = iProductCategoryId
        ORDER BY (CASE
                    WHEN LOWER(iSortOrder) = 'descending'
                    THEN LOWER(product.product) END) DESC,
                 (CASE
                  WHEN LOWER(iSortOrder) = 'ascending' OR iSortOrder IS NULL
                  THEN LOWER(product.product) END) ASC;
END;

---

CREATE PROCEDURE FilterStockProductCategories (
    IN iFilterText VARCHAR(200),
    IN iSortOrder VARCHAR(20)
)
BEGIN
    SELECT id AS product_category_id,
            category AS product_category
            FROM product_category
            WHERE product_category.category
            LIKE CONCAT('%', iFilterText, '%')
            ORDER BY (CASE WHEN LOWER(iSortOrder) = 'descending'
                        THEN LOWER(product_category.category) END) DESC,
                    (CASE WHEN LOWER(iSortOrder) <> 'descending' OR iSortOrder IS NULL
                        THEN LOWER(product_category.category) END) ASC;
END;

---

CREATE PROCEDURE FilterStockProductCategoriesByProduct (
    IN iFilterText VARCHAR(200),
    IN iSortOrder VARCHAR(20)
)
BEGIN
    SELECT id AS product_category_id,
            category AS product_category
            FROM product_category
            INNER JOIN (SELECT product_category_id FROM product
                        INNER JOIN product_category ON product.product_category_id = product_category.id
                        WHERE product.archived = FALSE
                        AND product.product LIKE CONCAT('%', iFilterText, '%')
                        ORDER BY (CASE WHEN LOWER(iSortOrder) = 'descending'
                                    THEN LOWER(product.product) END) DESC,
                                (CASE WHEN (iSortOrder IS NULL) OR (LOWER(iSortOrder) <> 'descending')
                                    THEN LOWER(product.product) END) ASC) pc
            ON pc.product_category_id = product_category.id;
END;

---

CREATE PROCEDURE FilterStockProducts (
    IN iFilterText VARCHAR(200),
    IN iSortOrder VARCHAR(20),
    IN iProductCategoryId INTEGER
)
BEGIN
    SELECT product.id AS product_id,
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
            rr_user.user AS user
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
END;

---

CREATE PROCEDURE FetchStockProductCount (
    IN iProductCategoryId INTEGER,
    IN iArchived BOOLEAN
)
BEGIN
    IF iProductCategoryId IS NULL OR iProductCategoryId < 1 THEN
        SELECT COUNT(product.id) AS product_count
            FROM product
            INNER JOIN product_category ON product.product_category_id = product_category.id
            LEFT JOIN rr_user ON product.user_id = rr_user.id
            WHERE product.archived = IFNULL(iArchived, FALSE);
    ELSE
        SELECT COUNT(product.id) AS product_count
            FROM product
            INNER JOIN product_category ON product.product_category_id = product_category.id
            LEFT JOIN rr_user ON product.user_id = rr_user.id
            WHERE product.archived = IFNULL(iArchived, FALSE)
            AND product_category.id = iProductCategoryId;
    END IF;
END;

---

CREATE PROCEDURE FilterStockProductCount (
    IN iFilterColumn VARCHAR(50),
    IN iFilterText VARCHAR(200),
    IN iArchived BOOLEAN
)
BEGIN
    SELECT COUNT(product.id) AS product_count
        FROM product
        INNER JOIN product_category ON product.product_category_id = product_category.id
        WHERE product.archived = IFNULL(iArchived, FALSE)
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
END;

---

CREATE PROCEDURE AddStockProductQuantity (
    IN iProductId INTEGER,
    IN iQuantity DOUBLE,
    IN iProductUnitId INTEGER,
    IN iReason VARCHAR(200),
    IN iUserId INTEGER
)
BEGIN
    INSERT INTO initial_product_quantity (product_id,
                                            quantity,
                                            product_unit_id,
                                            reason,
                                            user_id)
    SELECT iProductId,
                quantity,
                iProductUnitId,
                iReason,
                iUserId
        FROM current_product_quantity
        WHERE product_id = iProductId;

    UPDATE current_product_quantity 
        SET quantity = quantity + iQuantity,
            user_id = iUserId
		WHERE product_id = iProductId;
END;

---

CREATE PROCEDURE DeductStockProductQuantity (
    IN iProductId INTEGER,
    IN iQuantity DOUBLE,
    IN iProductUnitId INTEGER,
    IN iReason VARCHAR(200),
    IN iUserId INTEGER
)
BEGIN
	SET @availableQuantity := 0.0;
	SELECT quantity INTO @availableQuantity
        FROM current_product_quantity
        WHERE product_id = iProductId;

    IF @availableQuantity < iQuantity THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Available quantity is too low to make deduction.';
    END IF;

    UPDATE current_product_quantity
            SET quantity = @availableQuantity - iQuantity,
                user_id = iUserId
		WHERE product_id = iProductId;

    INSERT INTO initial_product_quantity (product_id,
                                            quantity,
                                            product_unit_id,
                                            reason,
                                            user_id)
		VALUES (iProductId,
                @availableQuantity,
                iProductUnitId,
                iReason,
                iUserId);

    SELECT LAST_INSERT_ID() AS initial_product_quantity_id;
END;

---

CREATE PROCEDURE FetchStockProduct (
    IN iProductId INTEGER
)
BEGIN
    SELECT product.id AS product_id,
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
            rr_user.user AS user
        FROM product
        INNER JOIN product_category ON product.product_category_id = product_category.id
        INNER JOIN product_unit ON product.id = product_unit.product_id
        INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON product.user_id = rr_user.id
        WHERE product.archived = FALSE AND product_unit.base_unit_equivalent = 1
        AND product.id = iProductId;
END;

---

CREATE PROCEDURE AddOrUpdateStockProductCategory (
    IN iCategory VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT IGNORE INTO product_category (category,
                                        short_form,
                                        note_id,
                                        archived,
                                        created,
                                        last_edited,
                                        user_id)
		VALUES (iCategory,
                iShortForm,
                NULLIF(iNoteId, 0),
                FALSE,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP(),
                iUserId);

	IF LAST_INSERT_ID() > 0 THEN
        UPDATE product_category SET archived = FALSE
            WHERE id = LAST_INSERT_ID();
		SELECT LAST_INSERT_ID() AS product_category_id;
	ELSE
		SELECT id
            FROM product_category
            WHERE category = iCategory;
    END IF;
END;

---

CREATE PROCEDURE AddStockProduct (
    IN iProductCategoryId INTEGER,
    IN iProduct VARCHAR(200),
    IN iShortForm VARCHAR(10),
    IN iDescription VARCHAR(200),
    IN iBarcode VARCHAR(50),
    IN iDivisible BOOLEAN,
    IN iImage BLOB,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
    SET @productAlreadyExists := NULL;
    SELECT id INTO @productAlreadyExists
            FROM product
            WHERE LOWER(product) = LOWER(iProduct)
            AND archived = FALSE;
    IF @productAlreadyExists IS NOT NULL THEN
        SIGNAL SQLSTATE '80001'
            SET MESSAGE_TEXT = 'Product already exists.';
    END IF;

	INSERT INTO product (product_category_id,
                        product,
                        short_form,
                        description,
                        barcode,
                        divisible,
                        image,
                        note_id,
                        archived,
                        created,
                        last_edited,
                        user_id)
		VALUES (iProductCategoryId,
                iProduct,
                iShortForm,
                iDescription,
                iBarcode,
                IFNULL(iDivisible, FALSE),
                iImage,
                NULLIF(iNoteId, 0),
                FALSE,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP(),
                iUserId);

	    IF LAST_INSERT_ID() > 0 THEN
		    SELECT LAST_INSERT_ID() AS product_id;
	    ELSE
		    SELECT id AS product_id
                FROM product
                WHERE product = iProduct;
        END IF;
END;

---

CREATE PROCEDURE AddStockProductUnit (
    IN iProductId INTEGER,
    IN iUnit VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iBaseUnitEquivalent INTEGER,
    IN iCostPrice DECIMAL(19,2),
    IN iRetailPrice DECIMAL(19,2),
    IN iPreferred BOOLEAN,
    IN iCurrency VARCHAR(4),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO product_unit (product_id,
                                unit,
                                short_form,
                                base_unit_equivalent,
                                cost_price,
                                retail_price,
                                preferred,
                                currency,
                                note_id,
                                archived,
                                created,
                                last_edited,
                                user_id)
		VALUES (iProductId,
                iUnit,
                iShortForm,
                iBaseUnitEquivalent,
                iCostPrice,
                iRetailPrice,
                IFNULL(iPreferred, FALSE),
                iCurrency,
                NULLIF(iNoteId, 0),
                FALSE,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP(),
                iUserId);

	IF LAST_INSERT_ID() > 0 THEN
		SELECT LAST_INSERT_ID() AS id;
	ELSE
		SELECT id
            FROM product_unit
            WHERE unit = iUnit;
    END IF;
END;

---

CREATE PROCEDURE AddInitialProductQuantity (
    IN iProductId INTEGER,
    IN iQuantity DOUBLE,
    IN iProductUnitId INTEGER,
    IN iReason VARCHAR(20),
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO initial_product_quantity (product_id,
                                            quantity,
                                            product_unit_id,
                                            reason,
                                            archived,
                                            created,
                                            last_edited,
                                            user_id)
		VALUES (iProductId,
                iQuantity,
                iProductUnitId,
                iReason,
                FALSE,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP(),
                iUserId);
END;

---

CREATE PROCEDURE AddCurrentProductQuantity (
    IN iProductId INTEGER,
    IN iQuantity DOUBLE,
    IN iProductUnitId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO current_product_quantity (product_id,
                                            quantity,
                                            product_unit_id,
                                            created,
                                            last_edited,
                                            user_id)
		VALUES (iProductId,
                iQuantity,
                iProductUnitId,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP(),
                iUserId);
END;

---

CREATE PROCEDURE FetchStockProductCategoryId (
    IN iProductId INTEGER
)
BEGIN
	SELECT (SELECT product_category_id
            FROM product
            WHERE product.id = iProductId) AS category_id;
END;

---

CREATE PROCEDURE UpdateStockProduct (
    IN iProductCategoryId INTEGER,
    IN iProductId INTEGER,
    IN iProduct VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iDescription VARCHAR(200),
    IN iBarcode VARCHAR(50),
    IN iDivisible BOOLEAN,
    IN iImageData BLOB,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE product
        SET product_category_id = iProductCategoryId,
            product = iProduct,
            short_form = iShortForm,
            description = iDescription,
		    barcode = iBarcode,
            divisible = iDivisible,
            image_data = iImageData,
            note_id = NULLIF(iNoteId, 0),
            archived = FALSE,
		    last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
		    WHERE product.id = iProductId;
END;

---

CREATE PROCEDURE UpdateStockProductUnit (
    IN iProductId INTEGER,
    IN iUnit VARCHAR(100),
    IN iShortForm VARCHAR(10),
    IN iBaseUnitEquivalent INTEGER,
    IN iCostPrice DECIMAL(19,2),
    IN iRetailPrice DECIMAL(19,2),
    IN iPreferred BOOLEAN,
    IN iCurrency VARCHAR(4),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
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
            archived = FALSE,
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
        WHERE product_id = iProductId;
END;

---

CREATE PROCEDURE ArchiveStockProduct (
    IN iProductId INTEGER,
    IN iUserId INTEGER
)
BEGIN
    UPDATE product
        SET archived = 1,
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
            WHERE id = iProductId;
        SET @productCategoryId = (SELECT category_id
                                    FROM product
                                    WHERE id = iProductId);
        SET @productExistsUnderCategory = (SELECT EXISTS(SELECT product_category_id
                                                        FROM product
                                                        WHERE archived = 0
                                                        AND product_category_id = @productCategoryId LIMIT 1)
                                        );
    IF @productExistsUnderCategory = FALSE THEN
        UPDATE category
            SET archived = 1,
                last_edited = CURRENT_TIMESTAMP(),
                user_id = iUserId
            WHERE id = @productCategoryId;
    END IF;
END;

---

CREATE PROCEDURE UndoArchiveStockItem (
    IN iProductId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE product
        SET archived = 0,
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
        WHERE id = iProductId;

    SET @productCategoryId := 0;
    SELECT product_category_id INTO @productCategoryId
        FROM product
        INNER JOIN product_category ON product_category.id = product.product_category_id
        WHERE product.id = iProductId;

    UPDATE product_category
        SET archived = 0,
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
        WHERE id = @productCategoryId;

	SELECT product.id AS product,
            product_category.id AS product_category_id,
            product_category.category,
            product.product,
            product.description,
            product.divisible,
            product.image_data,
            current_product_quantity.quantity,
            product_unit.id AS product_unit_id,
            product_unit.unit,
            product_unit.cost_price,
            product_unit.retail_price,
            product_unit.currency,
            product.created,
            product.last_edited,
            product.user_id,
            product.user_id AS user
        FROM product
		INNER JOIN product_category ON product.product_category_id = product_category.id
		INNER JOIN product_unit ON product.id = product_unit.product_id
		INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
		LEFT JOIN rr_user ON product.user_id = iUserId
		WHERE product.archived = 0
        AND product_unit.base_unit_equivalent = 1
		AND product.id = iProductId;

    SET @productCategoryId = (SELECT id
                        FROM product
                        WHERE archived = 0
                        LIMIT 1);
    IF @productCategoryId IS NOT NULL THEN
        UPDATE category
        SET archived = 0,
            last_edited = CURRENT_TIMESTAMP(),
            user_id = iUserId
            WHERE id = @productCategoryId;
    END IF;
END;

---

CREATE PROCEDURE ViewStockReport (
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT p.id AS product_id,
        category.id AS category_id,
        product_category.category,
        p.product,
        (SELECT IFNULL(quantity, 0)
            FROM initial_product_quantity
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                    AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND initial_product_quantity.product_id = p.id
            ORDER BY created ASC
            LIMIT 1) AS opening_stock_quantity,
        (SELECT IFNULL(SUM(quantity), 0)
            FROM sold_product
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                    AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND sold_product.product_id = p.id) AS quantity_sold,
        (SELECT IFNULL(SUM(quantity), 0)
            FROM purchased_product
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                    AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND purchased_product.product_id = p.id) AS quantity_bought,
            current_product_quantity.quantity AS quantity_in_stock,
            product_unit.id AS product_unit_id,
            product_unit.unit
        FROM product p
        INNER JOIN product_category ON p.product_category_id = product_category.id
        INNER JOIN product_unit ON product.id = product_unit.product_id
        INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON product.user_id = rr_user.id
        WHERE p.archived = FALSE AND product_unit.base_unit_equivalent = 1;
END;

---

CREATE PROCEDURE FilterStockReport (
    IN iFilterColumn VARCHAR(20),
    IN iFilterText VARCHAR(100),
    IN iSortColumn VARCHAR(20),
    IN iSortOrder VARCHAR(20),
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT p.id AS product_id,
        category.id AS category_id,
        product_category.category,
        p.product,
        (SELECT IFNULL(quantity, 0)
            FROM initial_product_quantity
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                    AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND initial_product_quantity.product_id = p.id
            ORDER BY created ASC
            LIMIT 1) AS opening_stock_quantity,
        (SELECT IFNULL(SUM(quantity), 0)
            FROM sold_product
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                    AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND sold_product.product_id = p.id) AS quantity_sold,
        (SELECT IFNULL(SUM(quantity), 0)
            FROM purchased_product
            WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                                    AND IFNULL(iTo, CURRENT_TIMESTAMP())
            AND purchased_product.product_id = p.id) AS quantity_bought,
            current_product_quantity.quantity AS quantity_in_stock,
            product_unit.id AS product_unit_id,
            product_unit.unit
        FROM product p
        INNER JOIN product_category ON p.product_category_id = product_category.id
        INNER JOIN product_unit ON product.id = product_unit.product_id
        INNER JOIN current_product_quantity ON product.id = current_product_quantity.product_id
        LEFT JOIN rr_user ON product.user_id = rr_user.id
        WHERE p.archived = FALSE AND product_unit.base_unit_equivalent = 1
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