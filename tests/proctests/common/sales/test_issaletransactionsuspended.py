#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

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

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_id",
                                                "customer_name",
                                                "suspended",
                                                "user_id") \
                                    .values(tuple(saleTransaction.values())) \
                                    .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

def is_sale_transaction_suspended(db, saleTransactionId):
    sqlResult = db.call_procedure("IsSaleTransactionSuspended", (saleTransactionId,))
    return bool(DatabaseResult(sqlResult).fetch_one()["suspended"])

if __name__ == '__main__':
    unittest.main()