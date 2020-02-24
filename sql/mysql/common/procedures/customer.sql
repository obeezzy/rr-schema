USE ###DATABASENAME###;

---

CREATE PROCEDURE AddCustomer (
	IN iClientId INTEGER,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO customer (client_id,
							note_id,
							user_id)
		VALUES (iClientId,
				iNoteId,
				iUserId);
	SELECT LAST_INSERT_ID() AS customer_id;
END;