#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class FilterStockProductCategoriesByProduct(StoredProcedureTestCase):
    @unittest.skip("Needs to be refactored.")
    def test_filter_stock_product_categories_by_product(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Pianos")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Yamaha")
        productCategory2 = add_product_category(db=self.db,
                                                category="Guitars")
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Yamaha")
        productCategory3 = add_product_category(db=self.db,
                                                category="Drums")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory3["product_category_id"],
                                product="Rowland")

        fetchedProductCategories = filter_stock_product_categories_by_product(db=self.db,
                                                                                filterText="ya",
                                                                                sortOrder="ascending")
        self.assertEqual(len(fetchedProductCategories), 2, "Expected 2 product categories.")
        self.assertEqual(fetchedProductCategories[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProductCategories[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")

        self.assertEqual(fetchedProductCategories[1]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProductCategories[1]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")

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
            "user_id": row["user_id"]
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
                RETURNING id AS product_category_id,
                    product,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def filter_stock_product_categories_by_product(db, filterText, sortOrder=None):
    db.call_procedure("FilterStockProductCategoriesByProduct", [filterText, sortOrder])
    results = []
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
