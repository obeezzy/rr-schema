#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class FetchProductCategoryId(StoredProcedureTestCase):
    def test_fetch_product(self):
        productCategory1 = add_product_category(self.db,
                                                category="Beastly Mutants")
        productCategory2 = add_product_category(self.db,
                                                category="Normal Mutants")

        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Wolverine")
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="X-23")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Scott Summers")

        productCategoryId1 = fetch_product_category_id(db=self.db,
                                                        productId=product1["product_id"])
        self.assertEqual(product1["product_category_id"],
                            productCategoryId1,
                            "Product category ID mismatch.")

        productCategoryId3 = fetch_product_category_id(db=self.db,
                                                        productId=product3["product_id"])
        self.assertEqual(product3["product_category_id"],
                            productCategoryId3,
                            "Product category ID mismatch.")

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"]
        }
    return result

def add_product(db, productCategoryId, product):
    product = {
        "product_category_id": productCategoryId,
        "product": product,
        "user_id": 1
    }

    db.execute("""INSERT INTO product (product_category_id,
                                        product,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_id,
                    product_category_id,
                    product,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def fetch_product_category_id(db, productId):
    db.call_procedure("FetchProductCategoryId", [productId])
    result = {}
    for row in db:
        result = {
            "product_category_id": row[0],
        }
    return result["product_category_id"]

if __name__ == '__main__':
    unittest.main()
