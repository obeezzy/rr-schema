#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddCurrentProductQuantity(StoredProcedureTestCase):
    def test_add_current_product_quantity(self):
        addedCurrentProductQuantity = add_current_product_quantity(db=self.db,
                                                                    productId=1,
                                                                    quantity=200.125)
        fetchedCurrentProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                        productId=addedCurrentProductQuantity["product_id"])

        self.assertEqual(fetchedCurrentProductQuantity["current_product_quantity_id"],
                            addedCurrentProductQuantity["current_product_quantity_id"],
                            "Current product quantity ID mismatch.")
        self.assertEqual(fetchedCurrentProductQuantity["product_id"],
                            addedCurrentProductQuantity["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedCurrentProductQuantity["quantity"],
                            addedCurrentProductQuantity["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedCurrentProductQuantity["user_id"],
                            addedCurrentProductQuantity["user_id"],
                            "User ID mismatch.")

def add_current_product_quantity(db, productId, quantity):
    currentProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }
    db.call_procedure("AddCurrentProductQuantity", 
                        tuple(currentProductQuantity.values()))
    result = {}
    for row in db:
        result = {
            "current_product_quantity_id": row[0]
        }
    result.update(currentProductQuantity)
    return result

def fetch_current_product_quantity(db, productId):
    db.execute("""SELECT id AS current_product_quantity_id,
                            product_id,
                            quantity,
                            user_id
                FROM current_product_quantity
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "current_product_quantity_id": row["current_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
