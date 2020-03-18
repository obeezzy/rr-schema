#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddCurrentProductQuantity(StoredProcedureTestCase):
    def test_add_current_product_quantity(self):
        addedCurrentProductQuantity = add_current_product_quantity(db=self.db,
                                                                    productId=1,
                                                                    quantity=200.125,
                                                                    productUnitId=1)
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

def add_current_product_quantity(db, productId, quantity, productUnitId):
    currentProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }
    sqlResult = db.call_procedure("AddCurrentProductQuantity", 
                                    tuple(currentProductQuantity.values()))
    currentProductQuantity.update(DatabaseResult(sqlResult).fetch_one())
    return currentProductQuantity

def fetch_current_product_quantity(db, productId):
    currentProductQuantity = db.schema.get_table("current_product_quantity")
    rowResult = currentProductQuantity.select("id AS current_product_quantity_id",
                                                "product_id AS product_id",
                                                "quantity AS quantity",
                                                "user_id AS user_id") \
                                        .where("product_id = :productId") \
                                        .bind("productId", productId) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()