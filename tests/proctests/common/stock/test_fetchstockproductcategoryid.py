#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class FetchStockProductCategoryId(StoredProcedureTestCase):
    def test_fetch_stock_product(self):
        product1 = add_product(db=self.db,
                                productCategoryId=1,
                                product="Wolverine")
        product2 = add_product(db=self.db,
                                productCategoryId=1,
                                product="X-23")
        product3 = add_product(db=self.db,
                                productCategoryId=2,
                                product="Scott Summers")

        productCategoryId1 = fetch_stock_product_category_id(db=self.db,
                                                                productId=product1["product_id"])
        self.assertEqual(product1["product_category_id"],
                            productCategoryId1,
                            "Product category ID mismatch.")

        productCategoryId3 = fetch_stock_product_category_id(db=self.db,
                                                                productId=product3["product_id"])
        self.assertEqual(product3["product_category_id"],
                            productCategoryId3,
                            "Product category ID mismatch.")

def add_product(db, productCategoryId, product):
    productDict = {
        "product_category_id": productCategoryId,
        "product": product,
        "user_id": 1
    }

    productTable = db.schema.get_table("product")
    result = productTable.insert("product_category_id",
                                    "product",
                                    "user_id") \
                                .values(tuple(productDict.values())) \
                                .execute()
    productDict.update(DatabaseResult(result).fetch_one("product_id"))
    return productDict

def fetch_stock_product_category_id(db, productId):
    sqlResult = db.call_procedure("FetchStockProductCategoryId", (productId,))
    return DatabaseResult(sqlResult).fetch_one()["product_category_id"]

if __name__ == '__main__':
    unittest.main()