#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddNote(StoredProcedureTestCase):
    def test_add_note(self):
        addedNote = add_note(self.db)
        fetchedNote = fetch_note(self.db)

        self.assertEqual(addedNote, fetchedNote, "Fetched record mismatch.")

def add_note(db):
    note = {
        "note": "Note",
        "table_name": "expense_transaction",
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddNote", tuple(note.values()))
    note.update(DatabaseResult(sqlResult).fetch_one("note_id"))
    return note

def fetch_note(db):
    noteTable = db.schema.get_table("note")
    rowResult = noteTable.select("id AS note_id",
                                    "note AS note",
                                    "table_name AS table_name",
                                    "user_id") \
                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()