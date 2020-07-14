CREATE OR REPLACE FUNCTION AddNote (
    IN iNote VARCHAR(200),
    IN iTableName VARCHAR(20),
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO note (note,
                        table_name,
                        user_id)
    VALUES (iNote,
            iTableName,
            iUserId)
    RETURNING id AS note_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION UpdateNote (
    IN iNoteId BIGINT,
    IN iNote VARCHAR(200),
    IN iTableName VARCHAR(20),
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE note
        SET note = iNote,
            table_name = iTableName,
            user_id = iUserId
    WHERE id = iNoteId;
$$ LANGUAGE sql;
