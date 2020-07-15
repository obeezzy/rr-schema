#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class FilterStockProductCategories(StoredProcedureTestCase):
    def test_filter_stock_product_categories(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Pianos")
        productCategory2 = add_product_category(db=self.db,
                                                category="Guitars")
        productCategory3 = add_product_category(db=self.db,
                                                category="Drums")

        fetchedProductCategories = filter_stock_product_categories(db=self.db,
                                                                    filterText="Pi",
                                                                    sortOrder="ascending")
        self.assertEqual(len(fetchedProductCategories), 1, "Expected 1 product category.")
        self.assertEqual(fetchedProductCategories[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProductCategories[0]["product_category"],
                            productCategory1["category"],
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

def filter_stock_product_categories(db, filterText, sortOrder=None):
    db.call_procedure("FilterStockProductCategories", [filterText, sortOrder])
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
