#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddOrUpdateProductCategory(StoredProcedureTestCase):
    def test_add_or_update__product_category(self):
        addedProductCategory = add_or_update__product_category(db=self.db,
                                                                    category="Superheroes",
                                                                    shortForm="hero")
        fetchedProductCategory = fetch__product_category(self.db)

        self.assertEqual(addedProductCategory["product_category_id"],
                            fetchedProductCategory["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(addedProductCategory["category"],
                            fetchedProductCategory["category"],
                            "Product category mismatch.")
        self.assertEqual(addedProductCategory["short_form"],
                            fetchedProductCategory["short_form"],
                            "Short form mismatch.")
        self.assertEqual(addedProductCategory["note_id"],
                            fetchedProductCategory["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedProductCategory["user_id"],
                            1,
                            "Product category mismatch.")

def add_or_update__product_category(db, category, shortForm):
    productCategory = {
        "category": category,
        "short_form": shortForm,
        "note_id": 1,
        "user_id": 1
    }
    db.call_procedure("AddOrUpdateProductCategory", 
                        tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row[0]
        }
    result.update(productCategory)
    return result

def fetch__product_category(db):
    db.execute("""SELECT id AS product_category_id,
                            category,
                            short_form,
                            note_id,
                            user_id
                FROM product_category""")
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "category": row["category"],
            "short_form": row["short_form"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
