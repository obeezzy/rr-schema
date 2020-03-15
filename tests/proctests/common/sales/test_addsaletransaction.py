#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddSaleTransaction(StoredProcedureTestCase):
    def test_add_sale_transaction(self):
        addedSaleTransaction = add_sale_transaction(db=self.db,
                                                            customerName="Lois Lane",
                                                            discount=20.40)
        fetchedSaleTransaction = fetch_sale_transaction(self.db)

        self.assertEqual(addedSaleTransaction["customer_name"],
                            fetchedSaleTransaction["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(addedSaleTransaction["customer_id"],
                            fetchedSaleTransaction["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(addedSaleTransaction["discount"],
                            fetchedSaleTransaction["discount"],
                            "Discount mismatch.")
        self.assertEqual(addedSaleTransaction["suspended"],
                            fetchedSaleTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(addedSaleTransaction["note_id"],
                            fetchedSaleTransaction["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedSaleTransaction["user_id"],
                            fetchedSaleTransaction["user_id"],
                            "User ID mismatch.")

def add_sale_transaction(db, customerName, discount, suspended=False, noteId=None):
    saleTransaction = {
        "customer_name": customerName,
        "customer_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddSaleTransaction",
                                    tuple(saleTransaction.values()))
    saleTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return saleTransaction

def fetch_sale_transaction(db):
    saleTransactionTable = db.schema.get_table("sale_transaction")
    rowResult = saleTransactionTable.select("id AS sale_transaction_id",
                                                "customer_id AS customer_id",
                                                "customer_name AS customer_name",
                                                "discount AS discount",
                                                "suspended AS suspended",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()