CREATE PROCEDURE AddBusinessAdmin (
    IN iEmailAddress VARCHAR(100),
    IN iFirstName VARCHAR(100),
    IN iLastName VARCHAR(100),
    IN iPhoto BLOB,
    IN iPhoneNumber VARCHAR(100)
)
BEGIN
    INSERT INTO business_admin (email_address, first_name, last_name, phone_number, photo, created, last_edited)
        VALUES (iEmailAddress, iFirstName, iLastName, iPhoneNumber, iPhoto, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
    SELECT LAST_INSERT_ID() AS business_admin_id;
END;

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
	SELECT name INTO @id FROM business_store WHERE name = iName;

    IF @id IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A business store name must be unique.';
    END IF;

    INSERT INTO business_store (business_admin_id, name, rack_id, address, business_family, establishment_year, phone_number, logo, created, last_edited)
        VALUES (iBusinessAdminId, iName, iRackId, iAddress, iBusinessFamily, iEstablishmentYear, iPhoneNumber, iLogo, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
    SELECT LAST_INSERT_ID() AS business_store_id;
END;

---

CREATE PROCEDURE GetBusinessAdminDetails (
    IN iEmailAddress VARCHAR(100)
)
BEGIN
    SELECT id AS business_admin_id, email_address, first_name, last_name, phone_number, photo, created, last_edited
    FROM business_admin WHERE email_address = iEmailAddress;
END;

---

CREATE PROCEDURE GetBusinessStores (
    IN iBusinessAdminId INTEGER
)
BEGIN
    SELECT id AS business_store_id, business_admin_id, name, rack_id, address, location, family, establishment_year, phone_number, logo, created, last_edited
    FROM business_store WHERE business_admin_id = iBusinessAdminId;
END;

---

CREATE PROCEDURE ActivateBusinessAdmin (
    IN iBusinessAdminId INTEGER,
    IN iActive BOOLEAN
)
BEGIN
    UPDATE business_admin SET active = iActive WHERE id = iBusinessAdminId;
END;

---

CREATE PROCEDURE ActivateBusinessStore (
    IN iBusinessStoreId INTEGER,
    IN iActive BOOLEAN
)
BEGIN
    UPDATE business_store SET active = iActive WHERE id = iBusinessStoreId;
END;

---

CREATE PROCEDURE LinkBusinessAdmin (
    IN iBusinessAdminId INTEGER
)
BEGIN
    UPDATE business_admin SET linked = TRUE WHERE id = iBusinessAdminId;
END;

---

CREATE PROCEDURE LinkBusinessStore (
    IN iBusinessSToreId INTEGER
)
BEGIN
    UPDATE business_store SET linked = TRUE WHERE id = iBusinessStoreId;
END;