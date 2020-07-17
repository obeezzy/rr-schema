CREATE OR REPLACE FUNCTION AddDebtor (
    IN iClientId BIGINT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO debtor (client_id,
                        note_id,
                        user_id)
    VALUES (iClientId,
            NULLIF(iNoteId, 0),
            iUserId)
    RETURNING id AS debtor_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddDebtPayment (
    IN iDebtTransactionId BIGINT,
    IN iTotalDebt NUMERIC(19,2),
    IN iAmountPaid NUMERIC(19,2),
    IN iBalance NUMERIC(19,2),
    IN iCurrency TEXT,
    IN iDueDateTime TIMESTAMP,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO debt_payment (debt_transaction_id,
                                total_debt,
                                amount_paid,
                                balance,
                                currency,
                                due_date_time,
                                note_id,
                                user_id)
        VALUES (iDebtTransactionId,
                iTotalDebt,
                iAmountPaid,
                iBalance,
                iCurrency,
                iDueDateTime,
                NULLIF(iNoteId, 0),
                iUserId)
        RETURNING id AS debt_payment_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddDebtTransaction (
    IN iDebtorId BIGINT,
    IN iTransactionTable TEXT,
    IN iTransactionId BIGINT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO debt_transaction (debtor_id,
                                    transaction_table,
                                    transaction_id,
                                    note_id,
                                    user_id)
        VALUES (iDebtorId,
                iTransactionTable,
                iTransactionId,
                NULLIF(iNoteId, 0),
                iUserId)
        RETURNING id AS debt_transaction_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveDebtTransactionByTransactionTable (
    IN iArchived BOOLEAN,
    IN iTransactionTable TEXT,
    IN iTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE debt_transaction
        SET archived = iArchived,
            last_edited = CURRENT_TIMESTAMP,
            user_id = iUserId
        WHERE transaction_table = iTransactionTable
            AND transaction_id = iTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION TouchDebtTransaction (
    IN iDebtTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE debt_transaction
        SET last_edited = CURRENT_TIMESTAMP,
            user_id = iUserId
        WHERE id = iDebtTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION UpdateDebtPayment (
    IN iDebtPaymentId BIGINT,
    IN iTotalDebt NUMERIC(19,2),
    IN iAmountPaid NUMERIC(19,2),
    IN iBalance NUMERIC(19,2),
    IN iCurrency TEXT,
    IN iDueDateTime TIMESTAMP,
    IN iUserId BIGINT
) RETURNS void 
AS $$
    UPDATE debt_payment
        SET total_debt = iTotalDebt,
            amount_paid = iAmountPaid,
			balance = iBalance,
			due_date_time = iDueDateTime,
			currency = iCurrency,
			user_id = iUserId
        WHERE id = iDebtPaymentId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveDebtTransactionById (
    IN iArchived BOOLEAN,
    IN iDebtTransactionId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE debt_transaction
        SET archived = iArchived,
            user_id = iUserId
        WHERE id = iDebtTransactionId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveDebtPayment (
    IN iArchived BOOLEAN,
    IN iDebtPaymentId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
BEGIN
    UPDATE debt_payment
        SET archived = iArchived,
            user_id = iUserId
    WHERE id = iDebtPaymentId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FilterDebtorsByName (
    IN iFilterColumn TEXT,
    IN iFilterText TEXT,
    IN iSortColumn TEXT,
    IN iSortOrder TEXT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(debtor_id BIGINT,
                preferred_name TEXT,
                first_name TEXT,
                last_name TEXT,
                total_balance NUMERIC(19,2),
                balance NUMERIC(19,2))
AS $$
BEGIN
    RETURN QUERY SELECT id AS debtor_id,
        '' AS preferred_name,
        '' AS first_name,
        '' AS last_name,
        0 AS total_balance,
        0 AS balance
    FROM debtor;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ArchiveDebtor (
    IN iArchived BOOLEAN,
    IN iDebtorId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE debtor
        SET archived = iArchived,
            user_id = iUserId
    WHERE id = iDebtorId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveDebtTransactionByDebtorId (
    IN iDebtorId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE debt_transaction
        SET archived = TRUE,
            user_id = iUserId
    WHERE id = iDebtorId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION FetchDebtTransaction (
    IN iDebtorId BIGINT
) RETURNS SETOF record
AS $$
    SELECT id AS debt_transaction_id
        FROM debt_transaction
    WHERE debtor_id = iDebtorId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION FetchDebtor (
    IN iDebtorId BIGINT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(debtor_id BIGINT, first_name TEXT, last_name TEXT, preferred_name TEXT, phone_number TEXT, note TEXT, user_id BIGINT)
AS $$
BEGIN
    RETURN QUERY SELECT debtor.id AS debtor_id,
            client.first_name AS first_name,
            client.last_name AS last_name,
            client.preferred_name AS preferred_name,
            client.phone_number AS phone_number,
            note.note AS note,
            debtor.user_id AS user_id
    FROM debtor
    INNER JOIN client ON client.id = debtor.client_id
    LEFT JOIN note ON note.id = debtor.note_id
    WHERE debtor.id = iDebtorId
        AND debtor.archived = iArchived;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewDebtTransactions (
    IN iDebtorId BIGINT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(debt_transaction_id BIGINT, debtor_id BIGINT, related_transaction_table TEXT, related_transaction_id BIGINT,
                debt_transaction_created TIMESTAMP, debt_payment_id BIGINT, total_debt NUMERIC(19,2),
                amount_paid NUMERIC(19,2), balance NUMERIC(19,2), currency TEXT,
                due_date_time TIMESTAMP, debt_transaction_note_id BIGINT, debt_payment_note_id BIGINT,
                archived BOOLEAN, debt_payment_created TIMESTAMP)
AS $$
BEGIN
    RETURN QUERY SELECT debt_transaction.id AS debt_transaction_id,
            debtor.id AS debtor_id,
            debt_transaction.transaction_table AS related_transaction_table,
            debt_transaction.transaction_id AS related_transaction_id,
            debt_transaction.created AS debt_transaction_created,
            debt_payment.id AS debt_payment_id,
            debt_payment.total_debt AS total_debt,
            debt_payment.amount_paid AS amount_paid,
            debt_payment.balance AS balance,
            debt_payment.currency AS currency,
            debt_payment.due_date_time AS due_date_time,
            debt_transaction.note_id AS debt_transaction_note_id,
            debt_payment.note_id AS debt_payment_note_id,
            debt_transaction.archived AS archived,
            debt_payment.created AS debt_payment_created
    FROM debt_payment
    INNER JOIN debt_transaction ON debt_transaction.id = debt_payment.debt_transaction_id
    INNER JOIN debtor ON debtor.id = debt_transaction.debtor_id
    LEFT JOIN note ON note.id = debt_transaction.note_id
    WHERE debtor.id = iDebtorId
        AND debt_transaction.archived = iArchived
    ORDER BY debt_payment.last_edited ASC;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewDebtors (
    IN iArchived BIGINT
) RETURNS TABLE(debtor_id BIGINT, preferred_name TEXT, first_name TEXT, last_name TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT DISTINCT
        debtor_list.debtor_id AS debtor_id,
        debtor_list.preferred_name AS preferred_name,
        debtor_list.first_name AS first_name,
        debtor_list.last_name AS last_name,
        SUM(debtor_list.balance) AS total_balance
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
                ) AS balance
    FROM debt_transaction dt
    INNER JOIN debtor ON debtor.id = dt.debtor_id
        AND debtor.archived = IFNULL(iArchived, FALSE)
    INNER JOIN client ON client.id = debtor.client_id) AS debtor_list
    GROUP BY debtor_list.debtor_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewDebtPayments (
    IN iDebtTransactionId BIGINT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(debt_transaction_id BIGINT, debt_payment_id BIGINT, total_debt NUMERIC(19,2),
                amount_paid NUMERIC(19,2), balance NUMERIC(19,2), currency TEXT,
                due_date_time TIMESTAMP, note_id BIGINT, note TEXT,
                archived BOOLEAN, created TIMESTAMP, last_edited TIMESTAMP)
AS $$
BEGIN
    RETURN QUERY SELECT debt_payment.debt_transaction_id AS debt_transaction_id,
            debt_payment.id AS debt_payment_id,
            debt_payment.total_debt AS total_debt,
            debt_payment.amount_paid AS amount_paid,
            debt_payment.balance AS balance,
            debt_payment.currency AS currency,
            debt_payment.due_date_time AS due_date_time,
            debt_payment.note_id AS note_id,
            note.note AS note,
            debt_transaction.archived AS debt_transaction_archived,
            debt_payment.created AS created,
            debt_payment.last_edited AS last_edited
    FROM debt_payment
    INNER JOIN debt_transaction ON debt_transaction.id = debt_payment.debt_transaction_id
    LEFT JOIN note ON note.id = debt_payment.note_id
    WHERE debt_transaction.id = iDebtTransactionId
	AND debt_transaction.archived = iArchived
    ORDER BY debt_payment.last_edited ASC;
END
$$ LANGUAGE plpgsql;
