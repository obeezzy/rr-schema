CREATE OR REPLACE FUNCTION AddCreditor (
    IN iClientId BIGINT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO creditor (client_id,
                            note_id,
                            user_id)
    VALUES (iClientId,
            NULLIF(iNoteId, 0),
            iUserId)
    RETURNING id AS creditor_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddCreditPayment (
    IN iCreditTransactionId BIGINT,
    IN iTotalCredit NUMERIC(19,2),
    IN iAmountPaid NUMERIC(19,2),
    IN iBalance NUMERIC(19,2),
    IN iCurrency TEXT,
    IN iDueDateTime TIMESTAMP,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
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
                iUserId)
    RETURNING id AS credit_payment_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION AddCreditTransaction (
    IN iCreditorId BIGINT,
    IN iTableRef TEXT,
    IN iTableId BIGINT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS BIGINT
AS $$
    INSERT INTO credit_transaction (creditor_id,
                                    table_ref,
                                    table_id,
                                    note_id,
                                    user_id)
        VALUES (iCreditorId,
                iTableRef,
                iTableId,
                iNoteId,
                iUserId)
        RETURNING id AS credit_transaction_id;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION ArchiveCreditTransaction (
    IN iArchived BOOLEAN,
    IN iTableRef TEXT,
    IN iTableId BIGINT,
    IN iUserId BIGINT
) RETURNS void
AS $$
    UPDATE credit_transaction
        SET archived = iArchived,
            user_id = iUserId
    WHERE table_ref = iTableRef
        AND table_id = iTableId;
$$ LANGUAGE sql;
