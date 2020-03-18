#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class UpdateStockProduct(StoredProcedureTestCase):
    def test_update_stock_product(self):
        product = add_product(self.db,
                                productCategoryId=1,
                                product="Daylyt")
        fetchedProduct = fetch_product(db=self.db)

        self.assertEqual(fetchedProduct["product_id"],
                            product["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProduct["product_category_id"],
                            product["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProduct["product"],
                            product["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedProduct["short_form"],
                            None,
                            "Short form mismatch.")
        self.assertEqual(fetchedProduct["description"],
                            None,
                            "Description mismatch.")
        self.assertEqual(fetchedProduct["barcode"],
                            None,
                            "Barcode mismatch.")
        self.assertEqual(fetchedProduct["divisible"],
                            True,
                            "Divisible flag mismatch.")
        self.assertEqual(fetchedProduct["image"],
                            None,
                            "Image mismatch.")
        self.assertEqual(fetchedProduct["note_id"],
                            None,
                            "Note ID mismatch.")
        self.assertEqual(fetchedProduct["user_id"],
                            product["user_id"],
                            "User ID mismatch.")

        updatedProduct = update_stock_product(db=self.db,
                                                productCategoryId=1,
                                                productId=1,
                                                product="Ill Mac",
                                                shortForm="Day",
                                                description="Battle rapper",
                                                barcode="barcode",
                                                divisible=True)
        fetchedProduct = fetch_product(db=self.db)

        self.assertEqual(fetchedProduct["product_id"],
                            updatedProduct["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProduct["product_category_id"],
                            updatedProduct["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProduct["product"],
                            updatedProduct["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedProduct["short_form"],
                            updatedProduct["short_form"],
                            "Short form mismatch.")
        self.assertEqual(fetchedProduct["description"],
                            updatedProduct["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedProduct["barcode"],
                            updatedProduct["barcode"],
                            "Barcode mismatch.")
        self.assertEqual(fetchedProduct["divisible"],
                            updatedProduct["divisible"],
                            "Divisible flag mismatch.")
        self.assertEqual(fetchedProduct["image"],
                            updatedProduct["image"],
                            "Image mismatch.")
        self.assertEqual(fetchedProduct["note_id"],
                            updatedProduct["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(fetchedProduct["user_id"],
                            updatedProduct["user_id"],
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

def update_stock_product(db, productCategoryId, productId, product, shortForm, description, barcode, divisible=True):
    note = {
        "product_category_id": productCategoryId,
        "product_id": productId,
        "product": product,
        "short_form": shortForm,
        "description": description,
        "barcode": barcode,
        "divisible": divisible,
        "image": None,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("UpdateStockProduct", tuple(note.values()))
    return note

def fetch_product(db):
    productTable = db.schema.get_table("product")
    rowResult = productTable.select("id AS product_id",
                                    "product_category_id AS product_category_id",
                                    "product AS product",
                                    "short_form AS short_form",
                                    "description AS description",
                                    "barcode AS barcode",
                                    "divisible AS divisible",
                                    "image AS image",
                                    "note_id AS note_id",
                                    "user_id AS user_id") \
                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()