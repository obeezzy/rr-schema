#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddSaleTransaction(StoredProcedureTestCase):
    def test_add_sale_transaction(self):
        addedSaleTransaction = add_sale_transaction(db=self.db,
                                                    customerName="Lois Lane",
                                                    discount=Decimal("20.40"))
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

    db.call_procedure("AddSaleTransaction",
                        tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row[0]
        }
    result.update(saleTransaction)
    return result

def fetch_sale_transaction(db):
    db.execute("""SELECT id AS sale_transaction_id,
                            customer_id,
                            customer_name,
                            discount,
                            suspended,
                            note_id,
                            user_id
                FROM sale_transaction""")
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
