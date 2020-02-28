USE ###DATABASENAME###;

---

CREATE PROCEDURE AddDebtor (
	IN iClientId INTEGER,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO debtor (client_id,
						note_id,
						user_id)
		VALUES (iClientId,
                NULLIF(iNoteId, 0),
				iUserId);
	SELECT LAST_INSERT_ID() AS debtor_id;
END;

---

CREATE PROCEDURE AddDebtPayment (
	IN iDebtTransactionId INTEGER,
    IN iTotalAmount DECIMAL(19,2),
    IN iAmountPaid DECIMAL(19,2),
    IN iBalance DECIMAL(19,2),
    IN iCurrency VARCHAR(4),
    IN iDueDateTime DATETIME,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO debt_payment (debt_transaction_id,
								total_debt,
								amount_paid,
								balance,
								currency,
								due_date_time,
								note_id,
								user_id)
		VALUES (iDebtTransactionId,
				iTotalAmount,
				iAmountPaid,
				iBalance,
				iCurrency,
				iDueDateTime,
                NULLIF(iNoteId, 0),
				iUserId);
	SELECT LAST_INSERT_ID() AS debt_payment_id;
END;

---

CREATE PROCEDURE AddDebtTransaction (
	IN iDebtorId INTEGER,
    IN iTransactionTable VARCHAR(20),
    IN iTransactionId INTEGER,
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	INSERT INTO debt_transaction (debtor_id,
									transaction_table,
									transaction_id,
									note_id,
									user_id)
		VALUES (iDebtorId,
				iTransactionTable,
				iTransactionId,
                NULLIF(iNoteId, 0),
				iUserId);

	SELECT LAST_INSERT_ID() AS debt_transaction_id;
END;

---

CREATE PROCEDURE ArchiveDebtTransactionByTransactionTable (
	IN iArchived BOOLEAN,
	IN iTransactionTable VARCHAR(40),
    IN iTransactionId INTEGER,
	IN iUserId INTEGER
)
BEGIN
	UPDATE debt_transaction
		SET archived = IFNULL(iArchived, FALSE),
			last_edited = CURRENT_TIMESTAMP(),
			user_id = iUserId
		WHERE transaction_table = iTransactionTable
		AND transaction_id = iTransactionId;
END;

---

CREATE PROCEDURE TouchDebtTransaction (
	IN iDebtTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debt_transaction
		SET last_edited = CURRENT_TIMESTAMP(),
			user_id = iUserId
		WHERE id = iDebtTransactionId;
END;

---

CREATE PROCEDURE UpdateDebtPayment (
	IN iDebtPaymentId INTEGER,
    IN iTotalDebt DECIMAL(19,2),
    IN iAmountPaid DECIMAL(19,2),
    IN iBalance DECIMAL(19,2),
    IN iCurrency VARCHAR(4),
    IN iDueDateTime DATETIME,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debt_payment
		SET total_debt = iTotalDebt,
			amount_paid = iAmountPaid,
			balance = iBalance,
			due_date_time = iDueDateTime,
			currency = iCurrency,
			user_id = iUserId
        WHERE id = iDebtPaymentId;
END;

---

CREATE PROCEDURE ArchiveDebtTransactionById (
	IN iDebtTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debt_transaction
		SET archived = TRUE,
			user_id = iUserId
		WHERE id = iDebtTransactionId;
END;

---

CREATE PROCEDURE ArchiveDebtPayment (
	IN iDebtPaymentId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debt_payment
		SET archived = TRUE,
			user_id = iUserId
		WHERE id = iDebtPaymentId;
END;

---

CREATE PROCEDURE FilterDebtorsByName (
	IN iFilterColumn VARCHAR(100),
	IN iFilterText VARCHAR(100),
	IN iSortColumn VARCHAR(100),
	IN iSortOrder VARCHAR(15),
    IN iArchived BOOLEAN
)
BEGIN
	SELECT DISTINCT
		debtor_list.debtor_id AS debtor_id,
		debtor_list.preferred_name AS preferred_name,
		debtor_list.first_name AS first_name,
		debtor_list.last_name AS last_name,
		SUM(debtor_list.total_debt) AS total_debt
		FROM (SELECT
			dt.debtor_id AS debtor_id,
			client.preferred_name AS preferred_name,
			client.first_name AS first_name,
			client.last_name AS last_name,
			(SELECT balance AS balance
				FROM (SELECT
						debt_payment.balance AS balance,
						debt_payment.created AS created
						FROM debt_payment
						WHERE debt_payment.debt_transaction_id = dt.id
						ORDER BY debt_payment.created DESC
						LIMIT 1
					) debt_transactions_for_debtor
			) AS total_debt
			FROM debt_transaction dt
			INNER JOIN debtor ON debtor.id = dt.debtor_id
							  AND debtor.archived = IFNULL(iArchived, FALSE)
			INNER JOIN client ON client.id = debtor.client_id) AS debtor_list
			WHERE debtor_list.first_name LIKE (CASE
												WHEN LOWER(iFilterColumn) = 'first_name'
												THEN CONCAT('%', iFilterText, '%')
												ELSE '%'
												END)
			AND debtor_list.last_name LIKE (CASE
											WHEN LOWER(iFilterColumn) = 'last_name'
											THEN CONCAT('%', iFilterText, '%')
											ELSE '%'
											END)
			AND debtor_list.preferred_name LIKE (CASE
													WHEN LOWER(iFilterColumn) = 'preferred_name'
													THEN CONCAT('%', iFilterText, '%')
													ELSE '%'
													END)
			AND debtor_list.total_debt LIKE (CASE
												WHEN LOWER(iFilterColumn) = 'total_debt'
												THEN CONCAT('%', iFilterText, '%')
												ELSE '%'
												END)
			GROUP BY debtor_list.debtor_id
			ORDER BY (CASE
						WHEN (LOWER(iSortColumn) = 'first_name') AND (LOWER(iSortOrder) <> 'descending')
							THEN LOWER(debtor_list.first_name)
						END) ASC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'first_name') AND (LOWER(iSortOrder) = 'descending')
							THEN LOWER(debtor_list.first_name)
						END) DESC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'last_name') AND (LOWER(iSortOrder) <> 'descending')
							THEN LOWER(debtor_list.last_name)
						END) ASC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'last_name') AND (LOWER(iSortOrder) = 'descending')
							THEN LOWER(debtor_list.last_name)
						END) DESC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'total_debt') AND (LOWER(iSortOrder) <> 'descending')
							THEN CAST(SUM(debtor_list.total_debt) AS unsigned)
						END) ASC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'total_debt') AND (LOWER(iSortOrder) = 'descending')
							THEN CAST(SUM(debtor_list.total_debt) AS unsigned)
						END) DESC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'preferred_name') AND (LOWER(iSortOrder) <> 'descending')
							THEN LOWER(debtor_list.preferred_name)
						END) ASC,
					(CASE
						WHEN (LOWER(iSortColumn) = 'preferred_name') AND (LOWER(iSortOrder) = 'descending')
							THEN LOWER(debtor_list.preferred_name)
						END) DESC;
END;

---

CREATE PROCEDURE ArchiveDebtor (
	IN iDebtorId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debtor
		SET archived = TRUE,
			last_edited = CURRENT_TIMESTAMP(),
			user_id = iUserId
		WHERE id = iDebtorId;
END;

---

CREATE PROCEDURE ArchiveDebtTransactionByDebtorId (
	IN iDebtorId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debt_transaction
		SET archived = TRUE,
			user_id = iUserId
		WHERE id = iDebtorId;
END;

---

CREATE PROCEDURE FetchDebtTransaction (
	IN iDebtorId INTEGER
)
BEGIN
	SELECT id AS debt_transaction_id
		FROM debt_transaction
		WHERE debtor_id = iDebtorId;
END;

---

CREATE PROCEDURE UndoArchiveDebtor (
	IN iDebtorId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debtor
		SET archived = FALSE,
			last_edited = CURRENT_TIMESTAMP(),
			user_id = iUserId
		WHERE id = iDebtorId;
END;

---

CREATE PROCEDURE UndoArchiveDebtTransaction (
	IN iDebtTransactionId INTEGER,
    IN iUserId INTEGER
)
BEGIN
	UPDATE debt_transaction
		SET archived = 0,
			last_edited = CURRENT_TIMESTAMP(),
			user_id = iUserId
		WHERE id = iDebtTransactionId;
END;

---

CREATE PROCEDURE UndoArchiveDebtPayment (
    IN iDebtPaymentId INTEGER,
    IN iUserId INTEGER
)
BEGIN
    UPDATE debt_payment
		SET archived = FALSE,
			last_edited = CURRENT_TIMESTAMP(),
        	user_id = iUserId
		WHERE id = iDebtPaymentId;
END;

---

CREATE PROCEDURE ViewTotalBalanceForDebtor (
	IN iDebtorId INTEGER
)
BEGIN
	SELECT debtor.client_id,
			debtor.id AS debtor_id,
			client.preferred_name AS preferred_name,
			(SELECT SUM(debt_payment.balance)
				FROM debt_payment
				INNER JOIN debt_transaction ON debt_transaction.id = debt_payment.debt_transaction_id
				INNER JOIN debtor ON debt_transaction.debtor_id = debtor.id
				WHERE debt_payment.debt_transaction_id IN
					(SELECT debt_transaction.id
						FROM debt_transaction
						WHERE debt_transaction.debtor_id = debtor.id
						AND debt_transaction.archived = 0)
						AND debt_payment.archived = 0 ORDER BY debt_payment.last_edited DESC LIMIT 1) AS total_debt,
			note.note AS note,
			debtor.created,
			debtor.last_edited,
			debtor.user_id,
			rr_user.user
		FROM debtor
		INNER JOIN client ON client.id = debtor.client_id
		LEFT JOIN rr_user ON rr_user.id = debtor.user_id
		LEFT JOIN note ON debtor.note_id = note.id
		WHERE debtor.archived = FALSE
		AND debtor.id = iDebtorId;
END;

---

CREATE PROCEDURE FetchDebtor (
	IN iDebtorId INTEGER,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT debtor.id AS debtor_id,
			client.preferred_name AS preferred_name,
			client.phone_number,
			client.first_name,
			client.last_name,
			client.phone_number,
			note.note,
			debtor.archived,
       		debtor.user_id
        FROM debtor
        INNER JOIN client ON client.id = debtor.client_id
		LEFT JOIN note ON note.id = debtor.note_id
        WHERE debtor.id = iDebtorId
		AND debtor.archived = IFNULL(iArchived, FALSE);
END;

---

CREATE PROCEDURE ViewDebtTransactions (
	IN iDebtorId INTEGER,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT debt_transaction.id AS debt_transaction_id,
			debt_transaction.transaction_table AS related_transaction_table,
			debt_transaction.transaction_id AS related_transaction_id,
			debt_transaction.created AS debt_transaction_created,
			debt_payment.id AS debt_payment_id,
			debt_payment.total_amount,
			debt_payment.amount_paid,
			debt_payment.balance AS balance,
			debt_payment.currency,
			debt_payment.due_date_time,
			debt_transaction.note_id AS debt_transaction_note_id,
			debt_payment.note_id AS debt_payment_note_id,
			debt_transaction.archived,
			debt_payment.created AS debt_payment_created
		FROM debt_payment
		INNER JOIN debt_transaction ON debt_transaction.id = debt_payment.debt_transaction_id
		INNER JOIN debtor ON debtor.id = debt_transaction.debtor_id
		LEFT JOIN note ON note.id = debt_transaction.note_id
		WHERE debtor.id = iDebtorId
		AND debt_transaction.archived = IFNULL(iArchived, FALSE)
		ORDER BY debt_payment.last_edited ASC;
END;

---

CREATE PROCEDURE ViewDebtors (
	IN iArchived INTEGER
)
BEGIN
	SELECT
		dt.debtor_id AS debtor_id,
		client.preferred_name AS preferred_name,
		client.first_name AS first_name,
		client.last_name AS last_name,
		(SELECT SUM(balance) AS balance
			FROM (SELECT
					debt_payment.balance AS balance,
					debt_payment.created AS created
					FROM debt_payment
					WHERE debt_payment.debt_transaction_id = dt.id
					ORDER BY created DESC
					LIMIT 1
				) debt_transactions_for_debtor
		) AS total_debt
		FROM debt_transaction dt
		INNER JOIN debtor ON debtor.id = dt.debtor_id AND debtor.archived = IFNULL(iArchived, FALSE)
		INNER JOIN client ON client.id = debtor.client_id;
END;

---

CREATE PROCEDURE ViewDebtPayments (
	IN iDebtTransactionId INTEGER,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT debt_transaction_id,
		debt_payment.id AS debt_payment_id,
		debt_payment.total_amount,
		debt_payment.amount_paid,
		debt_payment.balance AS balance,
		debt_payment.currency,
		debt_payment.due_date_time,
		debt_payment.note_id,
		note.note,
		debt_transaction.archived,
		debt_payment.created,
		debt_payment.last_edited
    FROM debt_payment
    INNER JOIN debt_transaction ON debt_transaction.id = debt_payment.debt_transaction_id
    LEFT JOIN note ON note.id = debt_payment.note_id
    WHERE debt_transaction.id = iDebtTransactionId
	AND debt_transaction.archived = IFNULL(iArchived, FALSE)
    ORDER BY debt_payment.last_edited ASC;
END
