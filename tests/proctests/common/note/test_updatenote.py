#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class UpdateNote(StoredProcedureTestCase):
    def test_update_note(self):
        add_note(self.db)
        updatedNote = update_note(self.db)
        fetchedNote = fetch_note(self.db)

        self.assertEqual(updatedNote, fetchedNote, "Note mismatch.")

def add_note(db):
    note = {
        "note": "This is very very noteworthy",
        "table_name": "income_transaction",
        "user_id": 1
    }

    noteTable = db.schema.get_table("note")
    result = noteTable.insert("note",
                                "table_name",
                                "user_id") \
                        .values(list(note.values())) \
                        .execute()
    note.update(DatabaseResult(result).fetch_one("note_id"))
    return note

def update_note(db):
    note = {
        "note_id": 1,
        "note": "New noteworthy note!",
        "table_name": "expense_transaction",
        "user_id": 1
    }

    db.call_procedure("UpdateNote",
                        tuple(note.values()))

    return note

def fetch_note(db):
    noteTable = db.schema.get_table("note")
    rowResult = noteTable.select("id AS note_id",
                                    "note AS note",
                                    "table_name AS table_name",
                                    "user_id AS user_id") \
                            .execute()

    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()