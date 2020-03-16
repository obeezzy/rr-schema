#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class IsPurchaseTransactionSuspended(StoredProcedureTestCase):
    def test_is_purchase_transaction_suspended_when_true(self):
        addedPurchaseTransaction = add_purchase_transaction(db=self.db,
                                                            vendorName="Tony Stark",
                                                            suspended=True)
        suspended = is_purchase_transaction_suspended(db=self.db, 
                                                        purchaseTransactionId=addedPurchaseTransaction["purchase_transaction_id"])
        self.assertEqual(suspended, True, "Not suspended.")

    def test_is_purchase_transaction_suspended_when_false(self):
        addedPurchaseTransaction = add_purchase_transaction(self.db,
                                                            vendorName="Tony Stark",
                                                            suspended=False)
        suspended = is_purchase_transaction_suspended(db=self.db, 
                                                        purchaseTransactionId=addedPurchaseTransaction["purchase_transaction_id"])
        self.assertEqual(suspended, False, "Suspended.")

def add_purchase_transaction(db, vendorName, suspended=False):
    purchaseTransaction = {
        "vendor_id": None,
        "vendor_name": vendorName,
        "suspended": suspended,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_id",
                                                "vendor_name",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

def is_purchase_transaction_suspended(db, purchaseTransactionId):
    sqlResult = db.call_procedure("IsPurchaseTransactionSuspended", (purchaseTransactionId,))
    return bool(DatabaseResult(sqlResult).fetch_one()["suspended"])

if __name__ == '__main__':
    unittest.main()