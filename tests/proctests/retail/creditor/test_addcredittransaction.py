#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddCreditTransaction(StoredProcedureTestCase):
    def test_add_credit_transaction(self):
        addedClient = add_client(self.db)
        addedCreditor = add_creditor(self.db, clientId=addedClient["client_id"])
        addedNote = add_note(self.db)
        addedCreditTransaction = add_credit_transaction(self.db, addedCreditor["creditor_id"], addedNote["note_id"])
        fetchedCreditTransaction = fetch_credit_transaction(self.db)

        self.assertEqual(addedCreditTransaction["credit_transaction_id"],
                            fetchedCreditTransaction["credit_transaction_id"],
                            "Credit transaction ID mismatch.")
        self.assertEqual(addedCreditTransaction["table_ref"],
                            fetchedCreditTransaction["table_ref"],
                            "Table ref mismatch.")
        self.assertEqual(addedCreditTransaction["table_id"],
                            fetchedCreditTransaction["table_id"],
                            "Table ID mismatch.")
        self.assertEqual(addedCreditTransaction["note_id"],
                            fetchedCreditTransaction["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedCreditTransaction["user_id"],
                            fetchedCreditTransaction["user_id"],
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

def add_credit_transaction(db, creditorId, noteId):
    creditTransaction = {
        "creditor_id": creditorId,
        "table_ref": "sale_transaction",
        "table_id": 20,
        "note_id": noteId,
        "user_id": 1
    }

    db.call_procedure("AddCreditTransaction",
                        tuple(creditTransaction.values()))
    result = {}
    for row in db:
        result = {
            "credit_transaction_id": row[0]
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

def fetch_credit_transaction(db):
    db.execute("""SELECT id AS credit_transaction_id,
                            creditor_id,
                            table_ref,
                            table_id,
                            note_id,
                            user_id
                FROM credit_transaction""")
    result = {}
    for row in db:
        result = {
            "credit_transaction_id": row["credit_transaction_id"],
            "creditor_id": row["creditor_id"],
            "table_ref": row["table_ref"],
            "table_id": row["table_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
