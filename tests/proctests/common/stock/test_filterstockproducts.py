#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class FilterStockProducts(StoredProcedureTestCase):
    def test_filter_stock_products(self):
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

        filteredProducts = filter_stock_products(db=self.db,
                                                    filterText="row",
                                                    sortOrder="ascending",
                                                    productCategoryId=productCategory2["product_category_id"])
                                                

        self.assertEqual(len(filteredProducts), 1, "Expected 1 product.")
        self.assertEqual(filteredProducts[0]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(filteredProducts[0]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(filteredProducts[0]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(filteredProducts[0]["product"],
                            product3["product"],
                            "Product mismatch.")
        self.assertEqual(filteredProducts[0]["description"],
                            product3["description"],
                            "Description mismatch.")
        self.assertEqual(filteredProducts[0]["divisible"],
                            product3["divisible"],
                            "Divisible mismatch.")
        self.assertEqual(filteredProducts[0]["quantity"],
                            currentProductQuantity3["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(filteredProducts[0]["product_unit_id"],
                            productUnit3["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(filteredProducts[0]["product_unit"],
                            productUnit3["unit"],
                            "Product unit mismatch.")
        self.assertEqual(filteredProducts[0]["cost_price"],
                            productUnit3["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(filteredProducts[0]["retail_price"],
                            productUnit3["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(filteredProducts[0]["user_id"],
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

def filter_stock_products(db, filterText, sortOrder, productCategoryId):
    sqlResult = db.call_procedure("FilterStockProducts", (
                                    filterText,
                                    sortOrder,
                                    productCategoryId))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()