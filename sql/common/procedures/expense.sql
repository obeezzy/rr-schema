CREATE OR REPLACE FUNCTION AddExpenseTransaction (
    IN iClientId BIGINT,
    IN iClientName TEXT,
    IN iPurpose TEXT,
    IN iAmount NUMERIC(19,2),
    IN iPaymentMethod PAYMENT_METHOD,
    IN iCurrency TEXT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO expense_transaction (client_name,
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
                iUserId)
    RETURNING id AS expense_transaction_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ViewExpenseTransactions (
    IN iFrom TIMESTAMP DEFAULT '1970-01-01 00:00:00',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(expense_transaction_id BIGINT, client_id BIGINT, client_name TEXT,
                amount NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT id AS expense_transaction_id,
        expense_transaction.client_id AS client_id,
        expense_transaction.client_name AS client_name,
        expense_transaction.amount AS amount
    FROM expense_transaction
    WHERE created BETWEEN iFrom AND iTo
        AND archived = iArchived;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterExpenseReport (
    IN iFilterColumn TEXT,
    IN iFilterText TEXT,
    IN iSortColumn TEXT,
    IN iSortOrder TEXT,
    IN iFrom TIMESTAMP DEFAULT '1970-01-01 00:00:00',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP) RETURNS TABLE(expense_transaction_id BIGINT, purpose TEXT, amount NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT expense_transaction.id AS expense_transaction_id,
        expense_transaction.purpose AS purpose,
        expense_transaction.amount AS amount
    FROM expense_transaction
    WHERE created BETWEEN iFrom AND iTo
        AND expense_transaction.archived = FALSE
        AND expense_transaction.purpose LIKE (CASE
                            WHEN LOWER(iFilterColumn) = 'purpose'
                            THEN CONCAT('%', iFilterText, '%')
                            ELSE '%'
                            END)
    ORDER BY (CASE
                WHEN LOWER(iSortOrder) = 'descending'
                AND LOWER(iSortColumn) = 'purpose'
                THEN LOWER(expense_transaction.purpose) END) DESC,
             (CASE
                WHEN (iSortOrder IS NULL
                AND iSortColumn IS NULL)
                OR (LOWER(iSortOrder) <> 'descending'
                AND LOWER(iSortColumn) = 'purpose')
                THEN LOWER(expense_transaction.purpose) END) ASC,
    LOWER(expense_transaction.purpose) ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewExpenseReport (
    IN iFrom TIMESTAMP DEFAULT '1970-01-01 00:00:00',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(expense_transaction_id BIGINT, purpose TEXT, amount NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT id AS expense_transaction_id,
            expense_transaction.purpose AS purpose,
            expense_transaction.amount AS amount
    FROM expense_transaction
    WHERE created BETWEEN iFrom AND iTo
        AND expense_transaction.archived = FALSE;
END
$$ LANGUAGE plpgsql;
