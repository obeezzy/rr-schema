#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class AddCreditPayment(StoredProcedureTestCase):
    def test_add_credit_payment(self):
        addedClient = add_client(self.db)
        addedCreditor = add_creditor(self.db, clientId=addedClient["client_id"])
        addedCreditTransaction = add_credit_transaction(self.db, creditorId=addedCreditor["creditor_id"])
        addedNote = add_note(self.db)
        addedCreditPayment = add_credit_payment(self.db, creditTransactionId=addedCreditTransaction["credit_transaction_id"], noteId=addedNote["note_id"])
        fetchedCreditPayment = fetch_credit_payment(self.db)

        self.assertEqual(addedCreditPayment["credit_payment_id"],
                            fetchedCreditPayment["credit_payment_id"],
                            "Credit payment ID mismatch.")
        self.assertEqual(addedCreditPayment["credit_transaction_id"],
                            fetchedCreditPayment["credit_transaction_id"],
                            "Credit transaction ID mismatch.")
        self.assertEqual(addedCreditPayment["total_credit"],
                            fetchedCreditPayment["total_credit"],
                            "Total credit mismatch.")
        self.assertEqual(addedCreditPayment["amount_paid"],
                            fetchedCreditPayment["amount_paid"],
                            "Amount paid mismatch.")
        self.assertEqual(addedCreditPayment["balance"],
                            fetchedCreditPayment["balance"],
                            "Balance mismatch.")
        self.assertEqual(addedCreditPayment["currency"],
                            fetchedCreditPayment["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedCreditPayment["due_date_time"],
                            fetchedCreditPayment["due_date_time"],
                            "Due date/time mismatch.")
        self.assertEqual(addedCreditPayment["note_id"],
                            fetchedCreditPayment["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedCreditPayment["user_id"],
                            fetchedCreditPayment["user_id"],
                            "User ID mismatch.")
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

def add_creditor(db, clientId):
    creditor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO creditor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS creditor_id""", tuple(creditor.values()))
    result = {}
    for row in db:
        result = {
            "creditor_id": row["creditor_id"]
        }
    result.update(creditor)
    return result

def add_credit_transaction(db, creditorId):
    creditTransaction = {
        "creditor_id": creditorId,
        "table_ref": "sale_transaction",
        "table_id": 20,
        "user_id": 1
    }

    db.execute("""INSERT INTO credit_transaction (creditor_id,
                                                    table_ref,
                                                    table_id,
                                                    user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS credit_transaction_id""", tuple(creditTransaction.values()))
    result = {}
    for row in db:
        result = {
            "credit_transaction_id": row["credit_transaction_id"]
        }
    result.update(creditTransaction)
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

def add_credit_payment(db, creditTransactionId, noteId):
    creditPayment = {
        "credit_transaction_id": creditTransactionId,
        "total_credit": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": datetime.now(),
        "note_id": noteId,
        "user_id": 1
    }

    db.call_procedure("AddCreditPayment", tuple(creditPayment.values()))
    result = {}
    for row in db:
        result = {
            "credit_payment_id": row[0]
        }
    result.update(creditPayment)
    return result

def fetch_credit_payment(db):
    db.execute("""SELECT id AS credit_payment_id,
                            credit_transaction_id,
                            total_credit,
                            amount_paid,
                            balance,
                            currency,
                            due_date_time,
                            note_id,
                            user_id
                FROM credit_payment""")
    result = {}
    for row in db:
        result = {
            "credit_payment_id": row["credit_payment_id"],
            "credit_transaction_id": row["credit_transaction_id"],
            "total_credit": row["total_credit"],
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
