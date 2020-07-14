#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddVendor(StoredProcedureTestCase):
    def test_add_vendor(self):
        addedVendor = add_vendor(self.db)
        fetchedVendor = fetch_vendor(self.db)

        self.assertEqual(addedVendor["vendor_id"], fetchedVendor["vendor_id"], "Vendor ID mismatch.")
        self.assertEqual(addedVendor["client_id"], fetchedVendor["client_id"], "Client ID mismatch.")
        self.assertEqual(addedVendor["note_id"], fetchedVendor["note_id"], "Note ID mismatch.")
        self.assertEqual(addedVendor["user_id"], fetchedVendor["user_id"], "User ID mismatch.")

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
