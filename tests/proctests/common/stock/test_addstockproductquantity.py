#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddStockProductQuantity(StoredProcedureTestCase):
    def test_add_stock_product_quantity(self):
        productCategory = add_product_category(db=self.db,
                                                category="Some category")
        product = add_product(db=self.db,
                                productCategoryId=productCategory["product_category_id"],
                                product="Some product")
        productUnit = add_product_unit(db=self.db,
                                        productId=product["product_id"],
                                        unit="G-Unit",
                                        costPrice=832.38,
                                        retailPrice=943.28)
        currentProductQuantity = add_current_product_quantity(db=self.db,
                                                                productId=product["product_id"],
                                                                quantity=200.5)
        newQuantity = 200.125
        add_stock_product_quantity(db=self.db,
                                    productId=product["product_id"],
                                    quantity=newQuantity,
                                    reason="sale_transaction")
        fetchedInitialProductQuantity = fetch_initial_product_quantity(db=self.db, productId=product["product_id"])
        fetchedCurrentProductQuantity = fetch_current_product_quantity(db=self.db, productId=product["product_id"])

        self.assertEqual(len(fetchedInitialProductQuantity), 1, "Expected 1 row.")
        self.assertEqual(len(fetchedCurrentProductQuantity), 1, "Expected 1 row.")
        self.assertEqual(fetchedCurrentProductQuantity[0]["quantity"],
                            currentProductQuantity["quantity"] + newQuantity,
                            "Quantity mismatch.")

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

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "cost_price": costPrice,
        "retailPrice": retailPrice,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "currency": "NGN",
        "user_id": 1
    }

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "cost_price",
                                        "retail_price",
                                        "base_unit_equivalent",
                                        "preferred",
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

def add_stock_product_quantity(db, productId, quantity, reason, userId=1):
    sqlResult = db.call_procedure("AddStockProductQuantity", (
                                    productId,
                                    quantity,
                                    reason,
                                    userId))
    return DatabaseResult(sqlResult).fetch_one()

def fetch_initial_product_quantity(db, productId):
    initialProductQuantity = db.schema.get_table("initial_product_quantity")
    rowResult = initialProductQuantity.select("product_id AS product_id",
                                                "quantity AS quantity",
                                                "user_id AS user_id") \
                                        .where("product_id = :productId") \
                                        .bind("productId", productId) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

def fetch_current_product_quantity(db, productId):
    currentProductQuantity = db.schema.get_table("current_product_quantity")
    rowResult = currentProductQuantity.select("product_id AS product_id",
                                                "quantity AS quantity",
                                                "user_id AS user_id") \
                                        .where("product_id = :productId") \
                                        .bind("productId", productId) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()