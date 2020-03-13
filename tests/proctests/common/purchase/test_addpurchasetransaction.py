#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime
from decimal import Decimal

class AddPurchaseTransaction(StoredProcedureTestCase):
    def test_add_purchase_transaction(self):
        addedPurchaseTransaction = add_purchase_transaction(db=self.db,
                                                            vendorName="Lois Lane",
                                                            discount=20.40)
        fetchedPurchaseTransaction = fetch_purchase_transaction(self.db)

        self.assertEqual(addedPurchaseTransaction["vendor_name"],
                            fetchedPurchaseTransaction["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(addedPurchaseTransaction["vendor_id"],
                            fetchedPurchaseTransaction["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(addedPurchaseTransaction["discount"],
                            fetchedPurchaseTransaction["discount"],
                            "Discount mismatch.")
        self.assertEqual(addedPurchaseTransaction["suspended"],
                            fetchedPurchaseTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(addedPurchaseTransaction["note_id"],
                            fetchedPurchaseTransaction["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedPurchaseTransaction["user_id"],
                            fetchedPurchaseTransaction["user_id"],
                            "User ID mismatch.")

def add_purchase_transaction(db, vendorName, discount, suspended=False, noteId=None):
    purchaseTransaction = {
        "vendor_name": vendorName,
        "vendor_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddPurchaseTransaction",
                                    tuple(purchaseTransaction.values()))
    purchaseTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return purchaseTransaction

def fetch_purchase_transaction(db):
    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    rowResult = purchaseTransactionTable.select("id AS purchase_transaction_id",
                                                "vendor_id AS vendor_id",
                                                "vendor_name AS vendor_name",
                                                "discount AS discount",
                                                "suspended AS suspended",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()