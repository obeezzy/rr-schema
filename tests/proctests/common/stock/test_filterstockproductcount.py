#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class FilterStockProductCount(StoredProcedureTestCase):
    def test_fetch_stock_product_count(self):
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

        fetchedProductCount = filter_stock_product_count(db=self.db,
                                                            filterColumn="product_category",
                                                            filterText="con",
                                                            archived=False)
        self.assertEqual(fetchedProductCount["product_count"], 1, "Product count mismatch.")

        fetchedProductCount = filter_stock_product_count(db=self.db,
                                                            filterColumn="product_category",
                                                            filterText="car",
                                                            archived=False)
        self.assertEqual(fetchedProductCount["product_count"], 5, "Product count mismatch.")

        fetchedProductCount = filter_stock_product_count(db=self.db,
                                                            filterColumn="product",
                                                            filterText="t",
                                                            archived=False)
        self.assertEqual(fetchedProductCount["product_count"], 2, "Product count mismatch.")

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

def filter_stock_product_count(db, filterColumn, filterText, archived=False):
    sqlResult = db.call_procedure("FilterStockProductCount", (filterColumn, filterText, archived))
    return DatabaseResult(sqlResult).fetch_one()

if __name__ == '__main__':
    unittest.main()