USE ###DATABASENAME###;

---

CREATE PROCEDURE AddVendor (
	IN iClientId INTEGER,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO vendor (client_id,
						note_id,
						user_id)
		VALUES (iClientId,
				NULLIF(iNoteId, 0),
				iUserId);
	SELECT LAST_INSERT_ID() AS vendor_id;
END;