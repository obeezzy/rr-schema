#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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

    db.execute("""INSERT INTO purchase_transaction (vendor_id,
                                                    vendor_name,
                                                    suspended,
                                                    user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_id,
                    vendor_name,
                    suspended,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def is_purchase_transaction_suspended(db, purchaseTransactionId):
    db.call_procedure("IsPurchaseTransactionSuspended", (purchaseTransactionId,))
    result = False
    for row in db:
        result = row[0]
    return result

if __name__ == '__main__':
    unittest.main()
