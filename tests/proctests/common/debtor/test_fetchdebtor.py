#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class FetchDebtor(StoredProcedureTestCase):
    def test_fetch_debtor(self):
        addedClient = add_client(self.db)
        addedNote = add_note(self.db)
        addedDebtor = add_debtor(db=self.db, client=addedClient, note=addedNote)
        fetchedDebtor = fetch_debtor(self.db)

        self.assertEqual(addedDebtor["debtor_id"], fetchedDebtor["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedDebtor["first_name"], fetchedDebtor["first_name"], "First name mismatch.")
        self.assertEqual(addedDebtor["last_name"], fetchedDebtor["last_name"], "Last name mismatch.")
        self.assertEqual(addedDebtor["preferred_name"], fetchedDebtor["preferred_name"], "Preferred name mismatch.")
        self.assertEqual(addedDebtor["phone_number"], fetchedDebtor["phone_number"], "Phone number mismatch.")
        self.assertEqual(addedDebtor["note"], fetchedDebtor["note"], "Note mismatch.")
        self.assertEqual(addedDebtor["user_id"], fetchedDebtor["user_id"], "User ID mismatch.")


def add_client(db):
    client = {
        "first_name": "Miles",
        "last_name": "Morales",
        "preferred_name": "Spider-Man",
        "phone_number": "1234788083",
        "user_id": 1
    }

    clientTable = db.schema.get_table("client")
    result = clientTable.insert("first_name",
                                "last_name",
                                "preferred_name",
                                "phone_number",
                                "user_id") \
                        .values(tuple(client.values())) \
                        .execute()
    client.update(DatabaseResult(result).fetch_one("client_id"))
    return client

def add_debtor(db, client, note):
    debtor = {
        "client_id": client["client_id"],
        "note_id": note["note_id"],
        "user_id": 1
    }
    debtorTable = db.schema.get_table("debtor")
    result = debtorTable.insert("client_id",
                                "note_id",
                                "user_id") \
                            .values(tuple(debtor.values())) \
                            .execute()
    del client["client_id"]
    debtor.update(client)
    debtor.update(DatabaseResult(result).fetch_one("debtor_id"))
    debtor["note"] = note["note"]
    return debtor

def add_note(db):
    note = {
        "note": "His middle name is Gonzalo.",
        "user_id": 1
    }
    noteTable = db.schema.get_table("note")
    result = noteTable.insert("note",
                                "user_id") \
                            .values(tuple(note.values())) \
                            .execute()
    note.update(DatabaseResult(result).fetch_one("note_id"))
    return note

def fetch_debtor(db, archived=False):
    debtor = {
        "debtor_id": 1,
        "archived": archived
    }

    sqlResult = db.call_procedure("FetchDebtor",
                                    tuple(debtor.values()))
    debtor.update(DatabaseResult(sqlResult).fetch_one())
    return debtor

if __name__ == '__main__':
    unittest.main()