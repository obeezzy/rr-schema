#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class UpdateProductUnit(StoredProcedureTestCase):
    def test_update_product_unit(self):
        product = add_product(db=self.db,
                                productCategoryId=1,
                                product="Cannabis")
        productUnit = add_product_unit(db=self.db,
                                        productId=product["product_id"],
                                        unit="gram(s)",
                                        shortForm="Kush",
                                        costPrice=Decimal("3882.18"),
                                        retailPrice=Decimal("4819.57"))
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

        updatedProductUnit = update_product_unit(db=self.db,
                                                        productId=product["product_id"],
                                                        unit="gram(s)",
                                                        shortForm="Kush",
                                                        costPrice=Decimal("1000.38"),
                                                        retailPrice=Decimal("2000.84"))
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
    product = {
        "product_category_id": productCategoryId,
        "product": product,
        "user_id": 1
    }

    db.execute("""INSERT INTO product (product_category_id,
                                        product,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_id,
                    product_category_id,
                    product,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

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

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            short_form,
                                            base_unit_equivalent,
                                            preferred,
                                            cost_price,
                                            retail_price,
                                            currency,
                                            note_id,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id,
                    product_id,
                    unit,
                    short_form,
                    base_unit_equivalent,
                    preferred,
                    cost_price,
                    retail_price,
                    currency,
                    note_id,
                    user_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "unit": row["unit"],
            "short_form": row["short_form"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "preferred": row["preferred"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def update_product_unit(db, productId, unit, shortForm, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
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

    db.call_procedure("UpdateProductUnit", tuple(productUnit.values()))
    return productUnit

def fetch_product_unit(db):
    db.execute("""SELECT id AS product_unit_id,
                            product_id,
                            unit,
                            short_form,
                            cost_price,
                            retail_price,
                            base_unit_equivalent,
                            preferred,
                            currency,
                            note_id,
                            user_id
                FROM product_unit""")
    result = {}
    for row in db:
        return {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "unit": row["unit"],
            "short_form": row["short_form"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "preferred": row["preferred"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
