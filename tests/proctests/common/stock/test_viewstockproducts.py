#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, date

class ViewStockProducts(StoredProcedureTestCase):
    def test_view_stock_products(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Pianos")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Yamaha",
                                description="The best",
                                divisible=False)
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=23.48,
                                        retailPrice=76.33)
        currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=50.125)
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Casio",
                                description="I've used the cheap version.",
                                divisible=True)
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=23.48,
                                        retailPrice=76.33)
        currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=20.25)
        productCategory2 = add_product_category(db=self.db,
                                                category="Guitars")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Rowland",
                                description="Think I had these back in Covenant University.",
                                divisible=False)
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=23.48,
                                        retailPrice=76.33)
        currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=10.625)

        fetchedProducts = view_stock_products(db=self.db,
                                                productCategoryId=productCategory1["product_category_id"],
                                                sortOrder="ascending")

        self.assertEqual(len(fetchedProducts), 2, "Expected 2 product categories.")
        self.assertEqual(fetchedProducts[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedProducts[0]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product"],
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedProducts[0]["description"],
                            product2["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedProducts[0]["divisible"],
                            product2["divisible"],
                            "Divisible mismatch.")
        self.assertEqual(fetchedProducts[0]["quantity"],
                            currentProductQuantity2["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedProducts[0]["product_unit_id"],
                            productUnit2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product_unit"],
                            productUnit2["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProducts[0]["cost_price"],
                            productUnit2["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProducts[0]["retail_price"],
                            productUnit2["retail_price"],
                            "Retail price mismatch.")
        self.assertLess(DatabaseDateTime(fetchedProducts[0]["created"]).date(),
                            date.today(),
                            "Time created mismatch.")
        self.assertLess(DatabaseDateTime(fetchedProducts[0]["last_edited"]).date(),
                            date.today(),
                            "Time modified mismatch.")
        self.assertEqual(fetchedProducts[0]["user_id"],
                            product2["user_id"],
                            "User ID mismatch.")

        self.assertEqual(fetchedProducts[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedProducts[1]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedProducts[1]["description"],
                            product1["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedProducts[1]["divisible"],
                            product1["divisible"],
                            "Divisible mismatch.")
        self.assertEqual(fetchedProducts[1]["quantity"],
                            currentProductQuantity1["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedProducts[1]["product_unit_id"],
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product_unit"],
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProducts[1]["cost_price"],
                            productUnit1["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProducts[1]["retail_price"],
                            productUnit1["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(DatabaseDateTime(fetchedProducts[1]["created"]),
                            date.today(),
                            "Time created mismatch.")
        self.assertLess(DatabaseDateTime(fetchedProducts[1]["last_edited"]),
                            date.today(),
                            "Time modified mismatch.")
        self.assertEqual(fetchedProducts[1]["user_id"],
                            product1["user_id"],
                            "User ID mismatch.")

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

def add_product(db, productCategoryId, product, description, divisible):
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

def view_stock_products(db, productCategoryId, sortOrder=None):
    sqlResult = db.call_procedure("ViewStockProducts", (
                                    productCategoryId,
                                    sortOrder))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()