#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddVendor(StoredProcedureTestCase):
    def test_add_vendor(self):
        addedVendor = add_vendor(self.db)
        fetchedVendor = fetch_vendor(self.db)

        self.assertEqual(addedVendor, fetchedVendor, "Vendor mismatch.")

def add_vendor(db):
    vendor = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddVendor",
                                    tuple(vendor.values()))
    vendor.update(DatabaseResult(sqlResult).fetch_one())
    return vendor

def fetch_vendor(db):
    vendorTable = db.schema.get_table("vendor")
    rowResult = vendorTable.select("id AS vendor_id",
                                    "client_id AS client_id",
                                    "note_id AS note_id",
                                    "user_id AS user_id") \
                                .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()