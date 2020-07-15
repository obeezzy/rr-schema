CREATE OR REPLACE FUNCTION AddCustomer (
    IN iClientId BIGINT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO customer (client_id,
                            note_id,
                            user_id)
        VALUES (iClientId,
                iNoteId,
                iUserId)
        RETURNING id AS customer_id;
$$ LANGUAGE sql;
