#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class FetchDebtor(StoredProcedureTestCase):
    def test_fetch_debtor(self):
        addedClient = add_client(self.db)
        addedNote = add_note(self.db)
        addedDebtor = add_debtor(db=self.db, client=addedClient, note=addedNote)
        fetchedDebtor = fetch_debtor(self.db)

        self.assertEqual(addedDebtor["debtor_id"], fetchedDebtor["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedClient["first_name"], fetchedDebtor["first_name"], "First name mismatch.")
        self.assertEqual(addedClient["last_name"], fetchedDebtor["last_name"], "Last name mismatch.")
        self.assertEqual(addedClient["preferred_name"], fetchedDebtor["preferred_name"], "Preferred name mismatch.")
        self.assertEqual(addedClient["phone_number"], fetchedDebtor["phone_number"], "Phone number mismatch.")
        self.assertEqual(addedNote["note"], fetchedDebtor["note"], "Note mismatch.")
        self.assertEqual(addedClient["user_id"], fetchedDebtor["user_id"], "User ID mismatch.")


def add_client(db):
    client = {
        "first_name": "Miles",
        "last_name": "Morales",
        "preferred_name": "Spider-Man",
        "phone_number": "1234788083",
        "user_id": 1
    }

    db.execute("""INSERT INTO client (first_name,
                                        last_name,
                                        preferred_name,
                                        phone_number,
                                        user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS client_id,
                            first_name,
                            last_name,
                            preferred_name,
                            phone_number,
                            user_id""", tuple(client.values()))
    db.commit()
    result = {} 
    for row in db:
        result = {
            "client_id": row["client_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "user_id": row["user_id"]
        }
    return result

def add_debtor(db, client, note):
    debtor = {
        "client_id": client["client_id"],
        "note_id": 1,
        "user_id": 1
    }
    db.execute("""INSERT INTO debtor (client_id,
                                        note_id,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS debtor_id,
                    client_id,
                    note_id,
                    user_id""", tuple(debtor.values()))
    db.commit()
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "client_id": row["client_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def add_note(db):
    note = {
        "note": "His middle name is Gonzalo.",
        "user_id": 1
    }
    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id,
                    note,
                    user_id""", tuple(note.values()))
    db.commit()
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "note": row["note"],
            "user_id": row["user_id"]
        }
    return result

def fetch_debtor(db, archived=False):
    debtor = {
        "debtor_id": 1,
        "archived": archived
    }

    db.call_procedure("FetchDebtor",
                        tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "note": row["note"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
