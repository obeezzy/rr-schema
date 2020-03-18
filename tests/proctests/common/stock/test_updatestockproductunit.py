#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class UpdateStockProductUnit(StoredProcedureTestCase):
    def test_update_stock_product_unit(self):
        product = add_product(db=self.db,
                                productCategoryId=1,
                                product="Cannabis")
        productUnit = add_product_unit(db=self.db,
                                        productId=product["product_id"],
                                        unit="gram(s)",
                                        shortForm="Kush",
                                        costPrice=3882.18,
                                        retailPrice=4819.57)
        fetchedProductUnit = fetch_product_unit(db=self.db)

        self.assertEqual(fetchedProductUnit["product_unit_id"],
                            productUnit["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedProductUnit["product_id"],
                            productUnit["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProductUnit["unit"],
                            productUnit["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProductUnit["short_form"],
                            productUnit["short_form"],
                            "Short form mismatch.")
        self.assertEqual(fetchedProductUnit["cost_price"],
                            productUnit["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProductUnit["retail_price"],
                            productUnit["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedProductUnit["currency"],
                            productUnit["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedProductUnit["note_id"],
                            productUnit["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(fetchedProductUnit["user_id"],
                            productUnit["user_id"],
                            "User ID mismatch.")

        updatedProductUnit = update_stock_product_unit(db=self.db,
                                                        productId=product["product_id"],
                                                        unit="gram(s)",
                                                        shortForm="Kush",
                                                        costPrice=1000.38,
                                                        retailPrice=2000.84)
        fetchedProductUnit = fetch_product_unit(db=self.db)

        self.assertEqual(fetchedProductUnit["product_id"],
                            updatedProductUnit["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProductUnit["unit"],
                            updatedProductUnit["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProductUnit["short_form"],
                            updatedProductUnit["short_form"],
                            "Short form mismatch.")
        self.assertEqual(fetchedProductUnit["cost_price"],
                            updatedProductUnit["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProductUnit["retail_price"],
                            updatedProductUnit["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedProductUnit["currency"],
                            updatedProductUnit["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedProductUnit["note_id"],
                            updatedProductUnit["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(fetchedProductUnit["user_id"],
                            updatedProductUnit["user_id"],
                            "User ID mismatch.")

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

def add_product_unit(db, productId, unit, shortForm, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "short_form": shortForm,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "currency": "NGN",
        "note_id": 1,
        "user_id": 1
    }

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "short_form",
                                        "base_unit_equivalent",
                                        "preferred",
                                        "cost_price",
                                        "retail_price",
                                        "currency",
                                        "note_id",
                                        "user_id") \
                                .values(tuple(productUnit.values())) \
                                .execute()
    productUnit.update(DatabaseResult(result).fetch_one("product_unit_id"))
    return productUnit

def update_stock_product_unit(db, productId, unit, shortForm, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
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

    sqlResult = db.call_procedure("UpdateStockProductUnit", tuple(productUnit.values()))
    return productUnit

def fetch_product_unit(db):
    productUnitTable = db.schema.get_table("product_unit")
    rowResult = productUnitTable.select("id AS product_unit_id",
                                        "product_id AS product_id",
                                        "unit AS unit",
                                        "short_form AS short_form",
                                        "cost_price AS cost_price",
                                        "retail_price AS retail_price",
                                        "base_unit_equivalent AS base_unit_equivalent",
                                        "preferred AS preferred",
                                        "currency AS currency",
                                        "note_id AS note_id",
                                        "user_id AS user_id") \
                                .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()