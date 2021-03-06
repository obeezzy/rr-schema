CREATE OR REPLACE FUNCTION AddIncomeTransaction (
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
                iUserId)
    RETURNING id AS income_transaction_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ViewIncomeTransactions (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(income_transaction_id BIGINT, client_id BIGINT, client_name TEXT,
                purpose TEXT, amount NUMERIC(19,2), currency VARCHAR(4))
AS $$
BEGIN
    RETURN QUERY SELECT income_transaction.id AS income_transaction_id,
            income_transaction.client_id AS client_id,
            income_transaction.client_name AS client_name,
            income_transaction.purpose AS purpose,
            income_transaction.amount AS amount,
            income_transaction.currency AS currency
    FROM income_transaction
    WHERE created BETWEEN iFrom AND iTo
        AND archived = iArchived;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterIncomeReport (
    IN iFilterColumn TEXT,
    IN iFilterText TEXT,
    IN iSortColumn TEXT,
    IN iSortOrder TEXT,
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(income_transaction_id BIGINT, purpose TEXT, amount NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT income_transaction.id AS income_transaction_id,
            income_transaction.purpose AS purpose,
            income_transaction.amount AS amount
    FROM income_transaction
    WHERE created BETWEEN iFrom AND iTo
        AND income_transaction.archived = FALSE
        AND income_transaction.purpose
            LIKE (CASE
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
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewIncomeReport (
    IN iFrom TIMESTAMP DEFAULT CURRENT_TIMESTAMP - INTERVAL '1 day',
    IN iTo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) RETURNS TABLE(income_transaction_id BIGINT, purpose TEXT, amount NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT income_transaction.id AS income_transaction_id,
            income_transaction.purpose AS purpose,
            income_transaction.amount AS amount
    FROM income_transaction
    WHERE created BETWEEN iFrom AND iTo
        AND income_transaction.archived = FALSE;
END
$$ LANGUAGE plpgsql;
