#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddInitialProductQuantity(StoredProcedureTestCase):
    def test_add_initial_product_quantity(self):
        addedInitialProductQuantity = add_initial_product_quantity(db=self.db,
                                                                    productId=1,
                                                                    quantity=200.125,
                                                                    reason="sale_transaction")
        fetchedInitialProductQuantity = fetch_initial_product_quantity(db=self.db,
                                                                        productId=addedInitialProductQuantity["product_id"])

        self.assertEqual(fetchedInitialProductQuantity["initial_product_quantity_id"],
                            addedInitialProductQuantity["initial_product_quantity_id"],
                            "Initial product quantity ID mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["product_id"],
                            addedInitialProductQuantity["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["quantity"],
                            addedInitialProductQuantity["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["reason"],
                            addedInitialProductQuantity["reason"],
                            "Reason mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["user_id"],
                            addedInitialProductQuantity["user_id"],
                            "User ID mismatch.")

def add_initial_product_quantity(db, productId, quantity, reason):
    initialProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "reason": "sale_transaction",
        "user_id": 1
    }
    db.call_procedure("AddInitialProductQuantity", 
                        tuple(initialProductQuantity.values()))
    result = {}
    for row in db:
        result = {
            "initial_product_quantity_id": row[0]
        }
    result.update(initialProductQuantity)
    return result

def fetch_initial_product_quantity(db, productId):
    db.execute("""SELECT id AS initial_product_quantity_id,
                            product_id,
                            quantity,
                            reason,
                            user_id
                FROM initial_product_quantity
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "initial_product_quantity_id": row["initial_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "reason": row["reason"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
