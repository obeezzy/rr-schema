#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddSoldProduct(StoredProcedureTestCase):
    def test_add_sold_product(self):
        addedSoldProduct = add_sold_product(self.db)
        fetchedSoldProduct = fetch_sold_product(self.db)

        self.assertEqual(addedSoldProduct["sold_product_id"],
                            fetchedSoldProduct["sold_product_id"],
                            "Sold product ID mismatch.")
        self.assertEqual(addedSoldProduct["sale_transaction_id"],
                            fetchedSoldProduct["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(addedSoldProduct["product_id"],
                            fetchedSoldProduct["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(addedSoldProduct["product_unit_id"],
                            fetchedSoldProduct["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(addedSoldProduct["unit_price"],
                            fetchedSoldProduct["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(addedSoldProduct["quantity"],
                            fetchedSoldProduct["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(addedSoldProduct["cost"],
                            fetchedSoldProduct["cost"],
                            "Cost mismatch.")
        self.assertEqual(addedSoldProduct["discount"],
                            fetchedSoldProduct["discount"],
                            "Discount mismatch.")
        self.assertEqual(addedSoldProduct["currency"],
                            fetchedSoldProduct["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedSoldProduct["user_id"],
                            fetchedSoldProduct["user_id"],
                            "User ID mismatch.")

def add_sold_product(db):
    soldProduct = {
        "sale_transaction_id": 1,
        "product_id": 1,
        "product_unit_id": 1,
        "unit_price": 1038.39,
        "quantity": 183.25,
        "cost": 1832.28,
        "discount": 138.23,
        "currency": "NGN",
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddSoldProduct",
                                    tuple(soldProduct.values()))
    soldProduct.update(DatabaseResult(sqlResult).fetch_one())
    return soldProduct

def fetch_sold_product(db):
    soldProductTable = db.schema.get_table("sold_product")
    rowResult = soldProductTable.select("id AS sold_product_id",
                                            "sale_transaction_id AS sale_transaction_id",
                                            "product_id AS product_id",
                                            "product_unit_id AS product_unit_id",
                                            "unit_price AS unit_price",
                                            "quantity AS quantity",
                                            "cost AS cost",
                                            "discount AS discount",
                                            "currency AS currency",
                                            "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()