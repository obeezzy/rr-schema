#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddStockProductUnit(StoredProcedureTestCase):
    def test_add_stock_product_unit(self):
        addedProductUnit = add_stock_product_unit(db=self.db,
                                                    productId=1,
                                                    unit="G-Unit",
                                                    shortForm="50cent",
                                                    costPrice=832.38,
                                                    retailPrice=943.28)
        fetchedProductUnit = fetch_product_unit(db=self.db,
                                                productId=addedProductUnit["product_id"])

        self.assertEqual(fetchedProductUnit["product_unit_id"],
                            addedProductUnit["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedProductUnit["product_id"],
                            addedProductUnit["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProductUnit["unit"],
                            addedProductUnit["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProductUnit["short_form"],
                            addedProductUnit["short_form"],
                            "Short form mismatch.")
        self.assertEqual(fetchedProductUnit["base_unit_equivalent"],
                            addedProductUnit["base_unit_equivalent"],
                            "Base unit equivalent mismatch.")
        self.assertEqual(fetchedProductUnit["cost_price"],
                            addedProductUnit["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProductUnit["retail_price"],
                            addedProductUnit["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedProductUnit["preferred"],
                            addedProductUnit["preferred"],
                            "Preferred flag mismatch.")
        self.assertEqual(fetchedProductUnit["currency"],
                            addedProductUnit["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedProductUnit["note_id"],
                            addedProductUnit["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(fetchedProductUnit["user_id"],
                            addedProductUnit["user_id"],
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

def add_stock_product_unit(db, productId, unit, shortForm, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "short_form": shortForm,
        "base_unit_equivalent": baseUnitEquivalent,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "preferred": preferred,
        "currency": "NGN",
        "note_id": 1,
        "user_id": 1
    }
    sqlResult = db.call_procedure("AddStockProductUnit",
                                    tuple(productUnit.values()))
    productUnit.update(DatabaseResult(sqlResult).fetch_one())
    return productUnit

def fetch_product_unit(db, productId):
    productUnitTable = db.schema.get_table("product_unit")
    rowResult = productUnitTable.select("id AS product_unit_id",
                                        "product_id AS product_id",
                                        "unit AS unit",
                                        "short_form AS short_form",
                                        "base_unit_equivalent AS base_unit_equivalent",
                                        "cost_price AS cost_price",
                                        "retail_price AS retail_price",
                                        "preferred AS preferred",
                                        "currency AS currency",
                                        "note_id AS note_id",
                                        "user_id AS user_id") \
                                .where("product_id = :productId") \
                                .bind("productId", productId) \
                                .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()