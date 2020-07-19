CREATE OR REPLACE FUNCTION AddNote (
    IN iNote TEXT,
    IN iUserId BIGINT
) RETURNS TABLE(note_id BIGINT)
AS $$
BEGIN
    RETURN QUERY INSERT INTO note (note,
                        user_id)
    VALUES (iNote,
            iUserId)
    RETURNING id AS note_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION UpdateNote (
    IN iNoteId BIGINT,
    IN iNote TEXT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE note
        SET note = iNote,
            user_id = iUserId
    WHERE id = iNoteId;
$$ LANGUAGE sql;
