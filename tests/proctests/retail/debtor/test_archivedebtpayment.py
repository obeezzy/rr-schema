#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class ArchiveDebtPayment(StoredProcedureTestCase):
    def test_archive_debt_payment(self):
        addedClient = add_client(self.db)
        addedDebtor = add_debtor(self.db,
                                    clientId=addedClient["client_id"])
        addedNote = add_note(self.db)
        addedDebtTransaction = add_debt_transaction(self.db,
                                                    debtorId=addedDebtor["debtor_id"])
        add_debt_payment(db=self.db,
                            debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                            noteId=addedNote["note_id"])
        add_debt_payment(db=self.db,
                            debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                            noteId=addedNote["note_id"])
        add_debt_payment(db=self.db,
                            debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                            noteId=addedNote["note_id"])

        archive_debt_payment(db=self.db,
                                debtPaymentId=1)

        fetchedDebtPayments = fetch_debt_payments(self.db)
        self.assertEqual(len(fetchedDebtPayments), 2, "Expected 2 debt payments to be returned.")

        debtPaymentArchived = len([debtPayment for debtPayment in fetchedDebtPayments \
                                if debtPayment["debt_payment_id"] == 1]) == 0
        self.assertEqual(debtPaymentArchived, True, "Debt payment not archived.")

def add_client(db):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "1234",
        "user_id": 1
    }

    db.execute("""INSERT INTO client (preferred_name,
                                        phone_number,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS client_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"]
        }
    result.update(client)
    return result

def add_note(db):
    note = {
        "note": "Note",
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"]
        }
    return result

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.call_procedure("AddDebtor", tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"]
        }
    result.update(debtor)
    return result

def add_debt_transaction(db, debtorId):
    debtTransaction = {
        "debtor_id": debtorId,
        "table_ref": "sale_transaction",
        "table_id": 20,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                table_ref,
                                                table_id,
                                                user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS debt_transaction_id""", tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"]
        }
    result.update(debtTransaction)
    return result

def add_debt_payment(db, debtTransactionId, noteId):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": 100,
        "amount_paid": 80,
        "balance": 20,
        "currency": "NGN",
        "due_date_time": str(datetime.now()),
        "note_id": noteId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_payment (debt_transaction_id,
                                            total_debt,
                                            amount_paid,
                                            balance,
                                            currency,
                                            due_date_time,
                                            note_id,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", tuple(debtPayment.values()))
    db.commit()

def archive_debt_payment(db, debtPaymentId):
    debtPayment = {
        "archived": True,
        "debt_payment_id": debtPaymentId,
        "user_id": 1
    }

    db.call_procedure("ArchiveDebtPayment",
                        tuple(debtPayment.values()))

def fetch_debt_payments(db, archived=False):
    db.execute("""SELECT id AS debt_payment_id,
                            debt_transaction_id,
                            total_debt,
                            amount_paid,
                            balance,
                            currency,
                            due_date_time,
                            note_id,
                            user_id
                FROM debt_payment
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "debt_payment_id": row["debt_payment_id"],
            "debt_transaction_id": row["debt_transaction_id"],
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
            "currency": row["currency"],
            "due_date_time": row["due_date_time"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
