#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

class AddPurchaseTransaction(StoredProcedureTestCase):
    def test_add_purchase_transaction(self):
        addedPurchaseTransaction = add_purchase_transaction(db=self.db,
                                                            vendorName="Lois Lane",
                                                            discount=locale.currency(20.40))
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

    db.call_procedure("AddPurchaseTransaction",
                        tuple(purchaseTransaction.values()))
    for row in db:
        result = {
            "purchase_transaction_id": row[0]
        }
    result.update(purchaseTransaction)
    return result

def fetch_purchase_transaction(db):
    db.execute("""SELECT id AS purchase_transaction_id,
                            vendor_id,
                            vendor_name,
                            discount,
                            suspended,
                            note_id,
                            user_id
                FROM purchase_transaction""")
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
