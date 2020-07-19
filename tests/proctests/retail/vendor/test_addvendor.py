#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddVendor(StoredProcedureTestCase):
    def test_add_vendor(self):
        add_client(self.db)
        add_note(self.db)
        addedVendor = add_vendor(self.db)
        fetchedVendor = fetch_vendor(self.db)

        self.assertEqual(addedVendor["vendor_id"], fetchedVendor["vendor_id"], "Vendor ID mismatch.")
        self.assertEqual(addedVendor["client_id"], fetchedVendor["client_id"], "Client ID mismatch.")
        self.assertEqual(addedVendor["note_id"], fetchedVendor["note_id"], "Note ID mismatch.")
        self.assertEqual(addedVendor["user_id"], fetchedVendor["user_id"], "User ID mismatch.")

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

def add_vendor(db):
    vendor = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }


    db.call_procedure("AddVendor", tuple(vendor.values()))
    result = {}
    for row in db:
        result = {
            "vendor_id": row["vendor_id"]
        }
    result.update(vendor)
    return result
    
def fetch_vendor(db):
    db.execute("""SELECT id AS vendor_id,
                            client_id,
                            note_id,
                            user_id
                FROM vendor""")
    result = {}
    for row in db:
        result = {
            "vendor_id": row["vendor_id"],
            "client_id": row["client_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
