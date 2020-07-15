CREATE OR REPLACE FUNCTION AddVendor (
    IN iClientId BIGINT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS TABLE(vendor_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO vendor (client_id,
                        note_id,
                        user_id)
    VALUES (iClientId,
            NULLIF(iNoteId, 0),
            iUserId)
    RETURNING id AS vendor_id;
END
$$ LANGUAGE plpgsql;
