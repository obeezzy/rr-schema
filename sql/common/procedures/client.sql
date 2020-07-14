CREATE OR REPLACE FUNCTION FilterClients (
    IN iFilterColumn VARCHAR(100),
    IN iFilterText VARCHAR(100),
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(client_id BIGINT, preferred_name VARCHAR(100), phone_number VARCHAR(100))
AS $$
BEGIN
    IF LOWER(iFilterColumn) = 'preferred_name' THEN
        RETURN QUERY SELECT id AS client_id,
                client.preferred_name,
                client.phone_number
        FROM client
        WHERE client.archived = iArchived
            AND client.preferred_name
            LIKE CONCAT('%', iFilterText, '%');
    ELSEIF LOWER(iFilterColumn) = 'phone_number' THEN
        RETURN QUERY SELECT id AS client_id,
                client.preferred_name,
                client.phone_number
        FROM client
        WHERE client.archived = iArchived
            AND client.phone_number
            LIKE CONCAT('%', iFilterText, '%');
    ELSE
        RETURN QUERY SELECT id AS client_id,
                client.preferred_name,
                client.phone_number
        FROM client
        WHERE client.archived = iArchived;
    END IF;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewClients (
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(client_id BIGINT, preferred_name VARCHAR(200), phone_number VARCHAR(100))
AS $$
    SELECT id AS client_id,
        preferred_name AS preferred_name,
        phone_number AS phone_number
    FROM client
    WHERE client.archived = iArchived;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddClient (
    IN iFirstName VARCHAR(100),
    IN iLastName VARCHAR(100),
    IN iPreferredName VARCHAR(100),
    IN iPhoneNumber VARCHAR(20),
    IN iAddress VARCHAR(100),
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO client (first_name,
                        last_name,
                        preferred_name,
                        phone_number,
                        address,
                        note_id,
                        archived,
                        created,
                        last_edited,
                        user_id)
    VALUES (iFirstName,
                iLastName,
                iPreferredName,
                iPhoneNumber,
                iAddress,
                NULLIF(iNoteId, 0),
                FALSE,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                iUserId)
    ON CONFLICT (phone_number) DO NOTHING
    RETURNING id AS client_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddClientLite (
    IN iPreferredName VARCHAR(100),
    IN iPhoneNumber VARCHAR(20),
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO client (preferred_name,
                        phone_number,
                        archived,
                        created,
                        last_edited,
                        user_id)
        SELECT *
            FROM (SELECT iPreferredName,
                            iPhoneNumber,
                            FALSE,
                            CURRENT_TIMESTAMP AS created,
                            CURRENT_TIMESTAMP AS last_edited,
                            iUserId) AS tmp
            WHERE NOT EXISTS (
                SELECT phone_number
                    FROM client
                    WHERE phone_number = iPhoneNumber
            ) LIMIT 1;

    SELECT id AS client_id
        FROM client
        WHERE phone_number = iPhoneNumber;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveClient (
    IN iClientId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE client
        SET archived = TRUE,
            last_edited = CURRENT_TIMESTAMP,
            user_id = iUserId
        WHERE id = iClientId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION UpdateClient (
    IN iClientId BIGINT,
    IN iFirstName VARCHAR(100),
    IN iLastName VARCHAR(100),
    IN iPreferredName VARCHAR(100),
    IN iPhoneNumber VARCHAR(20),
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE client
        SET first_name = iFirstName,
            last_name = iLastName,
            preferred_name = iPreferredName,
            phone_number = iPhoneNumber,
            last_edited = CURRENT_TIMESTAMP,
            user_id = iUserId
    WHERE id = iClientId;
$$ LANGUAGE sql;
