#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddProductUnit(StoredProcedureTestCase):
    def test_add_product_unit(self):
        addedProductCategory = add_product_category(self.db,
                                                    category="Category")
        addedProduct = add_product(self.db,
                                    productCategoryId=addedProductCategory["product_category_id"],
                                    product="Product")
        addedNote = add_note(self.db)
        addedProductUnit = add_product_unit(db=self.db,
                                                    productId=addedProduct["product_id"],
                                                    unit="G-Unit",
                                                    shortForm="50cent",
                                                    costPrice=Decimal("832.38"),
                                                    retailPrice=Decimal("943.28"),
                                                    noteId=addedNote["note_id"])
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

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id,
                    category,
                    user_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "category": row["category"],
            "user_id": row["user_id"]
        }
    return result

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
            "prodcut": row["product"],
            "user_id": row["user_id"]
        }
    return result

def add_note(db):
    note = {
        "note": "Note",
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"]
        }
    return result

def add_product_unit(db, productId, unit, shortForm, costPrice, retailPrice, noteId, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "short_form": shortForm,
        "base_unit_equivalent": baseUnitEquivalent,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "preferred": preferred,
        "currency": "NGN",
        "note_id": noteId,
        "user_id": 1
    }
    db.call_procedure("AddProductUnit",
                        tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row[0]
        }
    result.update(productUnit)
    return result

def fetch_product_unit(db, productId):
    db.execute("""SELECT id AS product_unit_id,
                            product_id,
                            unit,
                            short_form,
                            base_unit_equivalent,
                            cost_price,
                            retail_price,
                            preferred,
                            currency,
                            note_id,
                            user_id
                FROM product_unit
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "unit": row["unit"],
            "short_form": row["short_form"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "preferred": row["preferred"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
