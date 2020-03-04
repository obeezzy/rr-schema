USE ###DATABASENAME###;

---

CREATE PROCEDURE AddNote (
    IN iNote VARCHAR(200),
    IN iTableName VARCHAR(20),
    IN iUserId INTEGER
)
BEGIN
    INSERT INTO note (note,
                        table_name,
                        user_id)
        VALUES (iNote,
                iTableName,
                iUserId);
	SELECT LAST_INSERT_ID() AS note_id;
END;

---

CREATE PROCEDURE UpdateNote (
	IN iNoteId INTEGER,
    IN iNote VARCHAR(200),
    IN iTableName VARCHAR(20),
    IN iUserId INTEGER
)
BEGIN
    UPDATE note
        SET note = iNote,
            table_name = iTableName,
            user_id = iUserId
		WHERE id = iNoteId;
END;