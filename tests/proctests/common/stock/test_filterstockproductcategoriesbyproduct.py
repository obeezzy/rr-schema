#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class FilterStockProductCategoriesByProduct(StoredProcedureTestCase):
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
        self.assertEqual(len(fetchedProductCategories), 2, "Expected 1 product category.")
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

    categoryTable = db.schema.get_table("product_category")
    result = categoryTable.insert("category",
                                    "user_id") \
                            .values(tuple(productCategory.values())) \
                            .execute()
    productCategory.update(DatabaseResult(result).fetch_one("product_category_id"))
    return productCategory

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

def filter_stock_product_categories_by_product(db, filterText, sortOrder=None):
    sqlResult = db.call_procedure("FilterStockProductCategoriesByProduct", (
                                    filterText,
                                    sortOrder))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()