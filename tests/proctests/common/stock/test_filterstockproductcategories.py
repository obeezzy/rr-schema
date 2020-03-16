#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

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

    categoryTable = db.schema.get_table("product_category")
    result = categoryTable.insert("category",
                                    "user_id") \
                            .values(tuple(productCategory.values())) \
                            .execute()
    productCategory.update(DatabaseResult(result).fetch_one("product_category_id"))
    return productCategory

def filter_stock_product_categories(db, filterText, sortOrder=None):
    sqlResult = db.call_procedure("FilterStockProductCategories", (
                                    filterText,
                                    sortOrder))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()