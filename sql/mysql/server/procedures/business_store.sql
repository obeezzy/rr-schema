DROP PROCEDURE IF EXISTS AddBusinessStore;
---
CREATE PROCEDURE AddBusinessStore (
    IN iBusinessAdminId INTEGER,
    IN iName VARCHAR(300),
    IN iRackId VARCHAR(100),
    IN iAddress VARCHAR(200),
    IN iBusinessFamily VARCHAR(50),
    IN iEstablishmentYear INTEGER,
    IN iPhoneNumber VARCHAR(100),
    IN iLogo BLOB
)
BEGIN
	SET @id := NULL;
	SELECT name INTO @id
        FROM business_store
        WHERE name = iName;

    IF @id IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A business store name must be unique.';
    END IF;

    INSERT INTO business_store (business_admin_id,
                                name,
                                rack_id,
                                address,
                                business_family,
                                establishment_year,
                                phone_number,
                                logo,
                                created,
                                last_edited)
        VALUES (iBusinessAdminId,
                iName,
                iRackId,
                iAddress,
                iBusinessFamily,
                iEstablishmentYear,
                iPhoneNumber,
                iLogo,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP());
    SELECT LAST_INSERT_ID() AS business_store_id;
END;

---

DROP PROCEDURE IF EXISTS ViewBusinessStores;
---
CREATE PROCEDURE ViewBusinessStores (
    IN iBusinessAdminId INTEGER
)
BEGIN
    SELECT id AS business_store_id,
            business_admin_id,
            name,
            rack_id,
            address,
            location,
            business_family,
            establishment_year,
            phone_number,
            logo,
            created,
            last_edited
    FROM business_store
    WHERE business_admin_id = iBusinessAdminId;
END;

---

DROP PROCEDURE IF EXISTS ActivateBusinessStore;
---
CREATE PROCEDURE ActivateBusinessStore (
    IN iBusinessStoreId INTEGER,
    IN iActive BOOLEAN
)
BEGIN
    UPDATE business_store
        SET active = iActive
        WHERE id = iBusinessStoreId;
END;

---

DROP PROCEDURE IF EXISTS LinkBusinessStore;
---
CREATE PROCEDURE LinkBusinessStore (
    IN iBusinessStoreId INTEGER
)
BEGIN
    UPDATE business_store
        SET linked = TRUE
        WHERE id = iBusinessStoreId;
END;