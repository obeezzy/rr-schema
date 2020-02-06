DROP PROCEDURE IF EXISTS AddBusinessAdmin;
---
CREATE PROCEDURE AddBusinessAdmin (
    IN iEmailAddress VARCHAR(100),
    IN iFirstName VARCHAR(100),
    IN iLastName VARCHAR(100),
    IN iPhoto BLOB,
    IN iPhoneNumber VARCHAR(100)
)
BEGIN
    INSERT INTO business_admin (email_address,
                                first_name,
                                last_name,
                                phone_number,
                                photo,
                                created,
                                last_edited)
        VALUES (iEmailAddress,
                iFirstName,
                iLastName,
                iPhoneNumber,
                iPhoto,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP());
    SELECT LAST_INSERT_ID() AS business_admin_id;
END;

---

DROP PROCEDURE IF EXISTS FetchBusinessAdmin;
---
CREATE PROCEDURE FetchBusinessAdmin (
    IN iEmailAddress VARCHAR(100)
)
BEGIN
    SELECT id AS business_admin_id, email_address, first_name, last_name, phone_number, photo, created, last_edited
    FROM business_admin WHERE email_address = iEmailAddress;
END;

---

DROP PROCEDURE IF EXISTS ActivateBusinessAdmin;
---
CREATE PROCEDURE ActivateBusinessAdmin (
    IN iBusinessAdminId INTEGER,
    IN iActive BOOLEAN
)
BEGIN
    UPDATE business_admin SET active = iActive WHERE id = iBusinessAdminId;
END;

---

DROP PROCEDURE IF EXISTS LinkBusinessAdmin;
---
CREATE PROCEDURE LinkBusinessAdmin (
    IN iBusinessAdminId INTEGER
)
BEGIN
    UPDATE business_admin SET linked = TRUE WHERE id = iBusinessAdminId;
END;