USE ###DATABASENAME###;

---

CREATE PROCEDURE AddIncomeTransaction (
    IN iClientId INTEGER,
    IN iClientName VARCHAR(50),
    IN iPurpose VARCHAR(200),
    IN iAmount DECIMAL(19,2),
    IN iPaymentMethod VARCHAR(20),
    IN iCurrency VARCHAR(4),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
    )
BEGIN
    INSERT INTO income_transaction (client_name,
                                    client_id,
                                    purpose,
                                    amount,
                                    payment_method,
                                    currency,
                                    note_id,
                                    user_id)
        VALUES (iClientName,
                NULLIF(iClientId, 0),
                iPurpose,
                iAmount,
                iPaymentMethod,
                iCurrency,
                NULLIF(iNoteId, 0),
                iUserId);
	SELECT LAST_INSERT_ID() AS income_transaction_id;
END;

---

CREATE PROCEDURE ViewIncomeTransactions (
	IN iFrom DATETIME,
    IN iTo DATETIME,
    IN iArchived BOOLEAN
)
BEGIN
	SELECT id AS income_transaction_id,
            client_id AS client_id,
            name AS client_name,
            amount AS amount
        FROM income_transaction
		WHERE created BETWEEN iFrom
                        AND iTo
        AND archived = IFNULL(iArchived, FALSE);
END

---

CREATE PROCEDURE FilterIncomeReport (
    IN iFilterColumn VARCHAR(20),
    IN iFilterText VARCHAR(100),
    IN iSortColumn VARCHAR(20),
    IN iSortOrder VARCHAR(15),
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT id AS income_transaction_id,
            purpose AS purpose,
            amount AS amount
        FROM income_transaction
        WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                        AND IFNULL(iTo, CURRENT_TIMESTAMP())
        AND income_transaction.archived = FALSE
        AND purpose LIKE (CASE
                            WHEN LOWER(iFilterColumn) = 'purpose'
                            THEN CONCAT('%', iFilterText, '%')
                            ELSE '%'
                            END)
        ORDER BY (CASE
                    WHEN LOWER(iSortOrder) = 'descending'
                    AND LOWER(iSortColumn) = 'purpose'
                    THEN LOWER(income_transaction.purpose) END) DESC,
                 (CASE
                    WHEN (iSortOrder IS NULL
                        AND iSortColumn IS NULL)
                    OR (LOWER(iSortOrder) <> 'descending'
                        AND LOWER(iSortColumn) = 'purpose')
                    THEN LOWER(income_transaction.purpose) END) ASC,
        LOWER(income_transaction.purpose) ASC;
END;

---

CREATE PROCEDURE ViewIncomeReport (
    IN iFrom DATETIME,
    IN iTo DATETIME
)
BEGIN
    SELECT id AS income_transaction_id,
            purpose AS purpose,
            amount AS amount
        FROM income
        WHERE created BETWEEN IFNULL(iFrom, '1970-01-01 00:00:00')
                        AND IFNULL(iTo, CURRENT_TIMESTAMP())
        AND income.archived = FALSE;
END;