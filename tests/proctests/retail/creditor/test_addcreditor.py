#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddCreditor(StoredProcedureTestCase):
    def test_add_creditor(self):
        add_client(self.db)
        add_note(self.db)
        addedCreditor = add_creditor(self.db)
        fetchedCreditor = fetch_creditor(self.db)

        self.assertEqual(addedCreditor["creditor_id"], fetchedCreditor["creditor_id"], "Creditor ID mismatch.")
        self.assertEqual(addedCreditor["client_id"], fetchedCreditor["client_id"], "Client ID mismatch.")
        self.assertEqual(addedCreditor["note_id"], fetchedCreditor["note_id"], "Note ID mismatch.")
        self.assertEqual(addedCreditor["user_id"], fetchedCreditor["user_id"], "User ID mismatch.")

def add_client(db):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "1234",
        "archived": False,
        "user_id": 1
    }

    db.execute("""INSERT INTO client (preferred_name,
                                        phone_number,
                                        archived,
                                        user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS client_id,
                    preferred_name,
                    phone_number,
                    archived,
                    user_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "archived": row["archived"],
            "user_id": row["user_id"]
        }
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
            "note_id": row["note_id"],
            "note": row["note"],
            "user_id": row["user_id"]
        }
    return result

def add_creditor(db):
    creditor = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddCreditor",
                        tuple(creditor.values()))
    result = {}
    for row in db:
        result = {
            "creditor_id": row[0]
        }
    result.update(creditor)
    return result

def fetch_creditor(db):
    db.execute("""SELECT id as creditor_id,
                    client_id,
                    note_id,
                    user_id
                FROM creditor""")
    result = {}
    for row in db:
        result = {
            "creditor_id": row["creditor_id"],
            "client_id": row["client_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
