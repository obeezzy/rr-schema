CREATE OR REPLACE FUNCTION AddBusinessAdmin (
    IN iEmailAddress VARCHAR(100),
    IN iFirstName VARCHAR(100),
    IN iLastName VARCHAR(100),
    IN iPhoto BYTEA,
    IN iPhoneNumber VARCHAR(100)
) RETURNS TABLE(business_admin_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO business_admin (email_address,
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
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP)
    RETURNING id AS business_admin_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchBusinessAdmin (
    IN iEmailAddress VARCHAR(100)
) RETURNS TABLE(email_address VARCHAR(100))
AS $$
BEGIN
    RETURN QUERY SELECT ba.id AS business_admin_id,
            ba.email_address AS email_address,
            ba.first_name AS first_name,
            ba.last_name AS last_name,
            ba.phone_number AS phone_number,
            ba.photo AS photo,
            ba.created AS created,
            ba.last_edited AS last_edited
    FROM business_admin ba
    WHERE ba.email_address = iEmailAddress;
END
$$ LANGUAGE plpgsql

---

CREATE PROCEDURE ActivateBusinessAdmin (
    IN iBusinessAdminId BIGINT,
    IN iActive BOOLEAN
) RETURNS void
AS $$
BEGIN
    UPDATE business_admin
        SET active = iActive
    WHERE id = iBusinessAdminId;
END
LANGUAGE plpgsql;

---

CREATE PROCEDURE LinkBusinessAdmin (
    IN iBusinessAdminId BIGINT
) RETURNS void
AS $$
BEGIN
    UPDATE business_admin
        SET linked = TRUE
    WHERE id = iBusinessAdminId;
END
LANGUAGE plpgsql;
