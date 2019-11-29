USE ###DATABASENAME###;

---
DROP PROCEDURE IF EXISTS UpdateBusinessDetails;
---
CREATE PROCEDURE UpdateBusinessDetails(
    IN iName VARCHAR(100),
    IN iAddress VARCHAR(100),
    IN iBusinessFamily VARCHAR(10),
    IN iEstablishmentYear INTEGER,
    IN iPhoneNumber VARCHAR(20),
    IN iLogo BLOB,
    IN iExtraDetails VARCHAR(200)
)
BEGIN
    REPLACE INTO business_details (id, address, type, establishment_year, phone_number, logo, extra_details, created, last_edited)
        VALUES (1, iName, iAddress, iBusinessFamily, iEstablishmentYear, iPhoneNumber, iLogo, iExtraDetails, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
END;