#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddDebtor(StoredProcedureTestCase):
    def test_add_debtor(self):
        addedClient = add_client(self.db)
        addedNote = add_note(self.db)
        addedDebtor = add_debtor(self.db, clientId=addedClient["client_id"], noteId=addedNote["note_id"])
        fetchedDebtor = fetch_debtor(self.db)

        self.assertEqual(addedDebtor["debtor_id"], fetchedDebtor["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedDebtor["client_id"], fetchedDebtor["client_id"], "Client ID mismatch.")
        self.assertEqual(addedDebtor["note_id"], fetchedDebtor["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtor["user_id"], fetchedDebtor["user_id"], "User ID mismatch.")

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
                RETURNING id AS note_id,
                    note,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"]
        }
    return result

def add_debtor(db, clientId, noteId):
    debtor = {
        "client_id": clientId,
        "note_id": noteId,
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

def fetch_debtor(db):
    db.execute("""SELECT id AS debtor_id,
                            client_id,
                            note_id,
                            user_id
                FROM debtor""")
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "client_id": row["client_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
