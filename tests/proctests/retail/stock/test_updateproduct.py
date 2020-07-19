#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class UpdateProduct(StoredProcedureTestCase):
    def test_update_product(self):
        productCategory = add_product_category(self.db,
                                                category="Battle Rappers")
        product = add_product(self.db,
                                productCategoryId=productCategory["product_category_id"],
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

        addedNote = add_note(self.db)
        updatedProduct = update_product(db=self.db,
                                        productCategoryId=1,
                                            productId=1,
                                            product="Ill Mac",
                                            shortForm="Day",
                                            description="Battle rapper",
                                            barcode="barcode",
                                            divisible=True,
                                            noteId=addedNote["note_id"])
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

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"]
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
                    short_form,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "short_form": row["short_form"],
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

def update_product(db, productCategoryId, productId, product, shortForm, description, barcode, noteId, divisible=True):
    note = {
        "product_category_id": productCategoryId,
        "product_id": productId,
        "product": product,
        "short_form": shortForm,
        "description": description,
        "barcode": barcode,
        "divisible": divisible,
        "image": None,
        "note_id": noteId,
        "user_id": 1
    }

    db.call_procedure("UpdateProduct", tuple(note.values()))
    return note

def fetch_product(db):
    db.execute("""SELECT id AS product_id,
                    product_category_id,
                    product,
                    short_form,
                    description,
                    barcode,
                    divisible,
                    image,
                    note_id,
                    user_id
                FROM product""")
    result = {}
    for row in db:
        return {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "short_form": row["short_form"],
            "description": row["description"],
            "barcode": row["barcode"],
            "divisible": row["divisible"],
            "image": row["image"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
