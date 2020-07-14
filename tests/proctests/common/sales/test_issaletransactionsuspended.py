#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class IsSaleTransactionSuspended(StoredProcedureTestCase):
    def test_is_sale_transaction_suspended_when_true(self):
        addedSaleTransaction = add_sale_transaction(db=self.db,
                                                        customerName="Tony Stark",
                                                        suspended=True)
        suspended = is_sale_transaction_suspended(db=self.db, 
                                                    saleTransactionId=addedSaleTransaction["sale_transaction_id"])
        self.assertEqual(suspended, True, "Not suspended.")

    def test_is_sale_transaction_suspended_when_false(self):
        addedSaleTransaction = add_sale_transaction(self.db,
                                                        customerName="Tony Stark",
                                                        suspended=False)
        suspended = is_sale_transaction_suspended(db=self.db, 
                                                    saleTransactionId=addedSaleTransaction["sale_transaction_id"])
        self.assertEqual(suspended, False, "Suspended.")

def add_sale_transaction(db, customerName, suspended=False):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_id,
                                                customer_name,
                                                suspended,
                                                user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_id,
                    customer_name,
                    suspended,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def is_sale_transaction_suspended(db, saleTransactionId):
    db.call_procedure("IsSaleTransactionSuspended", [saleTransactionId])
    result = False
    for row in db:
        result = row[0]
    return result

if __name__ == '__main__':
    unittest.main()
