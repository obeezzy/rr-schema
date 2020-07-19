#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddDebtTransaction(StoredProcedureTestCase):
    def test_add_debt_transaction(self):
        addedClient = add_client(self.db)
        addedDebtor = add_debtor(self.db, clientId=addedClient["client_id"])
        addedNote = add_note(self.db)
        addedDebtTransaction = add_debt_transaction(self.db, debtorId=addedDebtor["debtor_id"], noteId=addedNote["note_id"])
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        self.assertEqual(addedDebtTransaction["debt_transaction_id"], fetchedDebtTransaction["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtTransaction["debtor_id"], fetchedDebtTransaction["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedDebtTransaction["table_ref"], fetchedDebtTransaction["table_ref"], "Table ref mismatch.")
        self.assertEqual(addedDebtTransaction["table_id"], fetchedDebtTransaction["table_id"], "Table ID mismatch.")
        self.assertEqual(addedDebtTransaction["note_id"], fetchedDebtTransaction["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtTransaction["user_id"], fetchedDebtTransaction["user_id"], "User ID mismatch.")

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

    db.call_procedure("AddDebtor",
                        tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row[0]
        }
    result.update(debtor)
    return result

def add_debt_transaction(db, debtorId, noteId):
    debtTransaction = {
        "debtor_id": debtorId,
        "table_ref": "sale_transaction",
        "table_id": 20,
        "note_id": noteId,
        "user_id": 1
    }

    db.call_procedure("AddDebtTransaction",
                        tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row[0]
        }
    result.update(debtTransaction)
    return result

def fetch_debt_transaction(db):
    db.execute("""SELECT id AS debt_transaction_id,
                        debtor_id,
                        table_ref,
                        table_id,
                        note_id,
                        user_id
                FROM debt_transaction""")
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "table_ref": row["table_ref"],
            "table_id": row["table_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
