#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class UpdateDebtPayment(StoredProcedureTestCase):
    def test_update_debt_payment(self):
        now = datetime.now()
        addedClient = add_client(self.db)
        addedDebtor = add_debtor(self.db,
                                    clientId=addedClient["client_id"])
        addedDebtTransaction = add_debt_transaction(self.db,
                                                    debtorId=addedDebtor["debtor_id"])
        addedNote = add_note(self.db)
        addedDebtPayment = add_debt_payment(self.db,
                                            debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                            dueDateTime=now,
                                            noteId=addedNote["note_id"])
        update_debt_payment(self.db,
                            debtPaymentId=addedDebtPayment["debt_payment_id"],
                            dueDateTime=now)
        updatedDebtPayment = fetch_debt_payment(self.db)

        self.assertEqual(addedDebtPayment["debt_payment_id"], updatedDebtPayment["debt_payment_id"], "Debt payment ID mismatch.")
        self.assertEqual(addedDebtPayment["debt_transaction_id"], updatedDebtPayment["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtPayment["total_debt"], updatedDebtPayment["total_debt"], "Total debt mismatch.")
        self.assertEqual(addedDebtPayment["amount_paid"], updatedDebtPayment["amount_paid"], "Amount paid mismatch.")
        self.assertEqual(addedDebtPayment["balance"], updatedDebtPayment["balance"], "Balance mismatch.")
        self.assertEqual(addedDebtPayment["currency"], updatedDebtPayment["currency"], "Currency mismatch.")
        self.assertEqual(addedDebtPayment["due_date_time"], updatedDebtPayment["due_date_time"], "Due date/time mismatch.")
        self.assertEqual(addedDebtPayment["note_id"], updatedDebtPayment["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtPayment["user_id"], updatedDebtPayment["user_id"], "User ID mismatch.")

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

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debtor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS debtor_id""", tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"]
        }
    result.update(debtor)
    return result

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debtor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS debtor_id""", tuple(debtor.values()))
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

def add_note(db):
    note = {
        "note": "Note",
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id,
                    note,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"]
        }
    return result

def add_debt_payment(db, debtTransactionId, dueDateTime, noteId):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": dueDateTime,
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS debt_payment_id,
                    debt_transaction_id,
                    total_debt,
                    amount_paid,
                    balance,
                    currency,
                    due_date_time,
                    note_id,
                    user_id""", tuple(debtPayment.values()))
    result = {}
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
    result.update(debtPayment)
    return result

def update_debt_payment(db, debtPaymentId, dueDateTime):
    debtPayment = {
        "debt_payment_id": debtPaymentId,
        "total_debt": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": dueDateTime,
        "user_id": 1
    }

    db.call_procedure("UpdateDebtPayment",
                        tuple(debtPayment.values()))

def fetch_debt_payment(db):
    db.execute("""SELECT id AS debt_payment_id,
                            debt_transaction_id,
                            total_debt,
                            amount_paid,
                            balance,
                            currency,
                            due_date_time,
                            note_id,
                            user_id
                FROM debt_payment""")
    result = {}
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
    return result

if __name__ == '__main__':
    unittest.main()
