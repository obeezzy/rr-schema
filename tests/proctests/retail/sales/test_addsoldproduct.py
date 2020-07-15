#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

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
        "unit_price": locale.currency(1038.39),
        "quantity": 183.25,
        "cost": locale.currency(1832.28),
        "discount": locale.currency(138.23),
        "currency": "NGN",
        "user_id": 1
    }

    db.call_procedure("AddSoldProduct",
                        tuple(soldProduct.values()))
    result = {}
    for row in db:
        result = {
            "sold_product_id": row[0]
        }
    result.update(soldProduct)
    return result

def fetch_sold_product(db):
    db.execute("""SELECT id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    product_unit_id,
                    unit_price,
                    quantity,
                    cost,
                    discount,
                    currency,
                    user_id
                FROM sold_product""")
    result = {}
    for row in db:
        result = {
            "sold_product_id": row["sold_product_id"],
            "sale_transaction_id": row["sale_transaction_id"],
            "product_id": row["product_id"],
            "product_unit_id": row["product_unit_id"],
            "unit_price": row["unit_price"].replace(",", ""),
            "quantity": row["quantity"],
            "cost": row["cost"].replace(",", ""),
            "discount": row["discount"].replace(",", ""),
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
