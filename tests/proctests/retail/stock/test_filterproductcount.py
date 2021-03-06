#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class FilterProductCount(StoredProcedureTestCase):
    @unittest.skip("Needs to be refactored.")
    def test_fetch_product_count(self):
        productCategory1 = add_product_category(db=self.db,
                                                    category="Cars")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Tesla")
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Dodge")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Toyota")
        product4 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Nissan")
        product5 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="BMW")

        productCategory2 = add_product_category(db=self.db,
                                                category="Consoles")
        product6 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Xbox One")

        fetchedProductCount = filter_product_count(db=self.db,
                                                            filterColumn="product_category",
                                                            filterText="con",
                                                            archived=False)
        self.assertEqual(fetchedProductCount["product_count"], 1, "Product count mismatch.")

        fetchedProductCount = filter_product_count(db=self.db,
                                                            filterColumn="product_category",
                                                            filterText="car",
                                                            archived=False)
        self.assertEqual(fetchedProductCount["product_count"], 5, "Product count mismatch.")

        fetchedProductCount = filter_product_count(db=self.db,
                                                            filterColumn="product",
                                                            filterText="t",
                                                            archived=False)
        self.assertEqual(fetchedProductCount["product_count"], 2, "Product count mismatch.")

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id,
                    category,
                    user_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "category": row["category"],
            "user_id": row["user_id"],
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

def filter_product_count(db, filterColumn, filterText, archived=False):
    db.call_procedure("FilterProductCount", [filterColumn, filterText, archived])
    result = {}
    for row in db:
        result = {
            "product_count": row["product_count"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
