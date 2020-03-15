#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddPurchasedProduct(StoredProcedureTestCase):
    def test_add_purchased_product(self):
        addedPurchasedProduct = add_purchased_product(self.db)
        fetchedPurchasedProduct = fetch_purchased_product(self.db)

        self.assertEqual(addedPurchasedProduct["purchased_product_id"],
                            fetchedPurchasedProduct["purchased_product_id"],
                            "Purchased product ID mismatch.")
        self.assertEqual(addedPurchasedProduct["purchase_transaction_id"],
                            fetchedPurchasedProduct["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(addedPurchasedProduct["product_id"],
                            fetchedPurchasedProduct["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(addedPurchasedProduct["product_unit_id"],
                            fetchedPurchasedProduct["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(addedPurchasedProduct["unit_price"],
                            fetchedPurchasedProduct["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(addedPurchasedProduct["quantity"],
                            fetchedPurchasedProduct["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(addedPurchasedProduct["cost"],
                            fetchedPurchasedProduct["cost"],
                            "Cost mismatch.")
        self.assertEqual(addedPurchasedProduct["discount"],
                            fetchedPurchasedProduct["discount"],
                            "Discount mismatch.")
        self.assertEqual(addedPurchasedProduct["currency"],
                            fetchedPurchasedProduct["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedPurchasedProduct["user_id"],
                            fetchedPurchasedProduct["user_id"],
                            "User ID mismatch.")

def add_purchased_product(db):
    purchasedProduct = {
        "purchase_transaction_id": 1,
        "product_id": 1,
        "product_unit_id": 1,
        "unit_price": 1038.39,
        "quantity": 183.25,
        "cost": 1832.28,
        "discount": 138.23,
        "currency": "NGN",
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddPurchasedProduct",
                                    tuple(purchasedProduct.values()))
    purchasedProduct.update(DatabaseResult(sqlResult).fetch_one())
    return purchasedProduct

def fetch_purchased_product(db):
    purchasedProductTable = db.schema.get_table("purchased_product")
    rowResult = purchasedProductTable.select("id AS purchased_product_id",
                                            "purchase_transaction_id AS purchase_transaction_id",
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