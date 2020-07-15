#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class UpdateNote(StoredProcedureTestCase):
    def test_update_note(self):
        add_note(self.db)
        updatedNote = update_note(self.db)
        fetchedNote = fetch_note(self.db)

        self.assertEqual(updatedNote["note_id"], fetchedNote["note_id"], "Note ID mismatch.")

def add_note(db):
    note = {
        "note": "This is very very noteworthy",
        "table_name": "income_transaction",
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    table_name,
                                    user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS note_id""", tuple(note.values()))
    for row in db:
        result = {
            "note_id": row[0]
        }
    result.update(note)
    return result

def update_note(db):
    note = {
        "note_id": 1,
        "note": "New noteworthy note!",
        "table_name": "expense_transaction",
        "user_id": 1
    }

    db.call_procedure("UpdateNote", tuple(note.values()))
    return note

def fetch_note(db):
    db.execute("""SELECT id AS note_id,
                            note,
                            table_name,
                            user_id
                FROM note""")
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
