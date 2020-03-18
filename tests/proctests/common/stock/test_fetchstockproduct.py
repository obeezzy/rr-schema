#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class FetchStockProduct(StoredProcedureTestCase):
    def test_fetch_stock_product(self):
        productCategory = add_product_category(db=self.db,
                                                category="TVs")
        product = add_product(db=self.db,
                                productCategoryId=productCategory["product_category_id"],
                                product="LG",
                                description="Description")
        productUnit = add_product_unit(db=self.db,
                                        productId=product["product_id"],
                                        unit="unit(s)",
                                        costPrice=285.28,
                                        retailPrice=302.31)
        currentProductQuantity = add_current_product_quantity(db=self.db,
                                                                productId=product["product_id"],
                                                                quantity=38.825)

        fetchedStockProduct = fetch_stock_product(db=self.db,
                                                    productId=product["product_id"])
        self.assertEqual(fetchedStockProduct["product_category_id"], 
                            productCategory["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedStockProduct["product_category"], 
                            productCategory["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedStockProduct["product_id"], 
                            product["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedStockProduct["product"], 
                            product["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedStockProduct["product_unit_id"], 
                            productUnit["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedStockProduct["product_unit"], 
                            productUnit["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedStockProduct["description"], 
                            product["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedStockProduct["divisible"], 
                            product["divisible"],
                            "Divisible flag mismatch.")
        self.assertEqual(fetchedStockProduct["quantity"], 
                            currentProductQuantity["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedStockProduct["cost_price"], 
                            productUnit["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedStockProduct["retail_price"], 
                            productUnit["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedStockProduct["currency"], 
                            productUnit["currency"],
                            "Currency mismatch.")
        self.assertLess(DatabaseDateTime(fetchedStockProduct["created"]), 
                            datetime.now(),
                            "Created date/time mismatch.")
        self.assertLess(DatabaseDateTime(fetchedStockProduct["last_edited"]), 
                            datetime.now(),
                            "Last edited date/time flag mismatch.")
        self.assertEqual(fetchedStockProduct["user_id"], 
                            1,
                            "User ID mismatch.")
        self.assertEqual(fetchedStockProduct["user"], 
                            "admin",
                            "User mismatch.")

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

def add_product(db, productCategoryId, product, description, divisible=True):
    productDict = {
        "product_category_id": productCategoryId,
        "product": product,
        "description": description,
        "divisible": divisible,
        "user_id": 1
    }

    productTable = db.schema.get_table("product")
    result = productTable.insert("product_category_id",
                                    "product",
                                    "description",
                                    "divisible",
                                    "user_id") \
                                .values(tuple(productDict.values())) \
                                .execute()
    productDict.update(DatabaseResult(result).fetch_one("product_id"))
    return productDict

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "currency": "NGN",
        "user_id": 1
    }

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "base_unit_equivalent",
                                        "preferred",
                                        "cost_price",
                                        "retail_price",
                                        "currency",
                                        "user_id") \
                                    .values(tuple(productUnit.values())) \
                                    .execute()
    productUnit.update(DatabaseResult(result).fetch_one("product_unit_id"))
    return productUnit

def add_current_product_quantity(db, productId, quantity):
    currentProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.insert("product_id",
                                                "quantity",
                                                "user_id") \
                                            .values(tuple(currentProductQuantity.values())) \
                                            .execute()
    currentProductQuantity.update(DatabaseResult(result).fetch_one("current_product_quantity_id"))
    return currentProductQuantity

def fetch_stock_product(db, productId):
    sqlResult = db.call_procedure("FetchStockProduct", (productId,))
    return DatabaseResult(sqlResult).fetch_one()

if __name__ == '__main__':
    unittest.main()