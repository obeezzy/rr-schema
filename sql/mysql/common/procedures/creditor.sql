
USE ###DATABASENAME###;

---

CREATE PROCEDURE AddCreditor (
	IN iClientId INTEGER,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO creditor (client_id,
							note_id,
							user_id)
		VALUES (iClientId,
				NULLIF(iNoteId, 0),
				iUserId);
	SELECT LAST_INSERT_ID() AS creditor_id;
END;

---

CREATE PROCEDURE AddCreditPayment (
	IN iCreditTransactionId INTEGER,
    IN iTotalCredit DECIMAL(19,2),
    IN iAmountPaid DECIMAL(19,2),
    IN iBalance DECIMAL(19,2),
    IN iCurrency VARCHAR(4),
    IN iDueDateTime DATETIME,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO credit_payment (credit_transaction_id,
								total_credit,
								amount_paid,
								balance,
								currency,
								due_date_time,
								note_id,
								user_id)
		VALUES (iCreditTransactionId,
				iTotalCredit,
				iAmountPaid,
				iBalance,
				iCurrency,
				iDueDateTime,
				NULLIF(iNoteId, 0),
				iUserId);
	SELECT LAST_INSERT_ID() AS credit_payment_id;
END;

---

CREATE PROCEDURE AddCreditTransaction (
	IN iCreditorId INTEGER,
    IN iTransactionTable VARCHAR(20),
    IN iTransactionId INTEGER,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO credit_transaction (creditor_id,
									transaction_table,
									transaction_id,
									note_id,
									user_id)
		VALUES (iCreditorId,
				iTransactionTable,
				iTransactionId,
				iNoteId,
				iUserId);

	SELECT LAST_INSERT_ID() AS credit_transaction_id;
END;

---

CREATE PROCEDURE ArchiveCreditTransaction (
	IN iArchived BOOLEAN,
	IN iTransactionTable VARCHAR(40),
    IN iTransactionId INTEGER,
	IN iUserId INTEGER
)
BEGIN
	UPDATE credit_transaction
		SET archived = IFNULL(iArchived, FALSE),
			user_id = iUserId
		WHERE transaction_table = iTransactionTable
		AND transaction_id = iTransactionId;
END;