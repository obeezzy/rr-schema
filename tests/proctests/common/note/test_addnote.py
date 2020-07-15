#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddNote(StoredProcedureTestCase):
    def test_add_note(self):
        addedNote = add_note(self.db)
        fetchedNote = fetch_note(self.db)

        self.assertEqual(addedNote["note_id"], fetchedNote["note_id"], "Note ID mismatch.")
        self.assertEqual(addedNote["note"], fetchedNote["note"], "Note mismatch.")
        self.assertEqual(addedNote["table_name"], fetchedNote["table_name"], "Table name mismatch.")
        self.assertEqual(addedNote["user_id"], fetchedNote["user_id"], "User ID mismatch.")

def add_note(db):
    note = {
        "note": "Note",
        "table_name": "expense_transaction",
        "user_id": 1
    }

    db.call_procedure("AddNote", tuple(note.values()))
    for row in db:
        result = {
            "note_id": row[0]
        }
    result.update(note)
    return result

def fetch_note(db):
    db.execute("""SELECT id AS note_id,
                            note,
                            table_name,
                            user_id
                FROM note""")
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "note": row["note"],
            "table_name": row["table_name"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
