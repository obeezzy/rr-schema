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
    IN iTotalDebt MONEY,
    IN iAmountPaid MONEY,
    IN iBalance MONEY,
    IN iCurrency VARCHAR(4),
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
    IN iTransactionTable VARCHAR(20),
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
    IN iTransactionTable VARCHAR(40),
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
    IN iTotalDebt MONEY,
    IN iAmountPaid MONEY,
    IN iBalance MONEY,
    IN iCurrency VARCHAR(4),
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
    IN iFilterColumn VARCHAR(100),
    IN iFilterText VARCHAR(100),
    IN iSortColumn VARCHAR(100),
    IN iSortOrder VARCHAR(15),
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(debtor_id BIGINT, preferred_name VARCHAR(100), first_name VARCHAR(100), last_name VARCHAR(100), total_balance MONEY, balance MONEY)
AS $$
BEGIN
    RETURN QUERY SELECT id AS debtor_id FROM debtor;
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
) RETURNS TABLE(debtor_id BIGINT, first_name VARCHAR(100), last_name VARCHAR(100), preferred_name VARCHAR(100), phone_number VARCHAR(100), note VARCHAR(100), user_id BIGINT)
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
) RETURNS TABLE(debt_transaction_id BIGINT, debtor_id BIGINT, related_transaction_table VARCHAR(100), related_transaction_id BIGINT,
                debt_transaction_created TIMESTAMP, debt_payment_id BIGINT, total_debt MONEY,
                amount_paid MONEY, balance MONEY, currency VARCHAR(4),
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
) RETURNS TABLE(debtor_id BIGINT, preferred_name VARCHAR(100), first_name VARCHAR(100), last_name VARCHAR(100))
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
) RETURNS TABLE(debt_transaction_id BIGINT, debt_payment_id BIGINT, total_debt MONEY,
                amount_paid MONEY, balance MONEY, currency VARCHAR(4),
                due_date_time TIMESTAMP, note_id BIGINT, note VARCHAR(200),
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
