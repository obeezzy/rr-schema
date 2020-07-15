#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

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
        "quantity": 183.25,
        "unit_price": locale.currency(1038.39),
        "cost": locale.currency(1832.28),
        "discount": locale.currency(138.23),
        "currency": "NGN",
        "user_id": 1
    }

    db.call_procedure("AddPurchasedProduct",
                        tuple(purchasedProduct.values()))
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row[0]
        }
    result.update(purchasedProduct)
    return result

def fetch_purchased_product(db):
    db.execute("""SELECT id AS purchased_product_id,
                            purchase_transaction_id,
                            product_id,
                            product_unit_id,
                            quantity,
                            unit_price,
                            cost,
                            discount,
                            currency,
                            user_id
                FROM purchased_product""")
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row["purchased_product_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "product_id": row["product_id"],
            "product_unit_id": row["product_unit_id"],
            "quantity": row["quantity"],
            "unit_price": row["unit_price"].replace(",", ""),
            "cost": row["cost"].replace(",", ""),
            "discount": row["discount"].replace(",", ""),
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
