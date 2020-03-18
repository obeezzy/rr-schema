#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddInitialProductQuantity(StoredProcedureTestCase):
    def test_add_initial_product_quantity(self):
        addedInitialProductQuantity = add_initial_product_quantity(db=self.db,
                                                                    productId=1,
                                                                    quantity=200.125,
                                                                    productUnitId=1,
                                                                    reason="sale_transaction")
        fetchedInitialProductQuantity = fetch_initial_product_quantity(db=self.db,
                                                                        productId=addedInitialProductQuantity["product_id"])

        self.assertEqual(fetchedInitialProductQuantity["product_id"],
                            addedInitialProductQuantity["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["quantity"],
                            addedInitialProductQuantity["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["product_unit_id"],
                            addedInitialProductQuantity["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["reason"],
                            addedInitialProductQuantity["reason"],
                            "Reason mismatch.")
        self.assertEqual(fetchedInitialProductQuantity["user_id"],
                            addedInitialProductQuantity["user_id"],
                            "User ID mismatch.")

def add_initial_product_quantity(db, productId, quantity, productUnitId, reason):
    initialProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "reason": "sale_transaction",
        "user_id": 1
    }
    sqlResult = db.call_procedure("AddInitialProductQuantity", 
                                    tuple(initialProductQuantity.values()))
    initialProductQuantity.update(DatabaseResult(sqlResult).fetch_one())
    return initialProductQuantity

def fetch_initial_product_quantity(db, productId):
    initialProductQuantity = db.schema.get_table("initial_product_quantity")
    rowResult = initialProductQuantity.select("id AS product_unit_id",
                                                "product_id AS product_id",
                                                "quantity AS quantity",
                                                "product_unit_id AS product_unit_id",
                                                "reason AS reason",
                                                "user_id AS user_id") \
                                        .where("product_id = :productId") \
                                        .bind("productId", productId) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()