#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from psycopg2.errors import RaiseException

class AddProduct(StoredProcedureTestCase):
    def test_add_product(self):
        addedProduct = add_product(self.db)
        fetchedProduct = fetch_product(self.db)

        self.assertEqual(addedProduct["product_category_id"], fetchedProduct["product_category_id"], "Product category ID mismatch.")
        self.assertEqual(addedProduct["product"], fetchedProduct["product"], "Product mismatch.")
        self.assertEqual(addedProduct["short_form"], fetchedProduct["short_form"], "Short form mismatch.")
        self.assertEqual(addedProduct["description"], fetchedProduct["description"], "Description mismatch.")
        self.assertEqual(addedProduct["barcode"], fetchedProduct["barcode"], "Barcode mismatch.")
        self.assertEqual(addedProduct["divisible"], fetchedProduct["divisible"], "Divisible mismatch.")
        self.assertEqual(addedProduct["image"], fetchedProduct["image"], "Image mismatch.")
        self.assertEqual(addedProduct["note_id"], fetchedProduct["note_id"], "Note ID mismatch.")
        self.assertEqual(addedProduct["user_id"], fetchedProduct["user_id"], "User ID mismatch.")

    def test_raise_duplicate_entry_exception(self):
        with self.assertRaises(RaiseException) as context:
            add_product(self.db)
            add_product(self.db)

        self.assertEqual("P0001", context.exception.pgcode)
        self.assertIn("Product already exists.", context.exception.pgerror)

def add_product(db):
    product = {
        "product_category_id": 1,
        "product": "Product",
        "short_form": "Short",
        "description": "Description",
        "barcode": "Barcode",
        "divisible": True,
        "image": None,
        "note_id": None,
        "user_id": 1
    }

    db.call_procedure("AddProduct", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row[0]
        }
    result.update(product)
    return result

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
        result = {
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
