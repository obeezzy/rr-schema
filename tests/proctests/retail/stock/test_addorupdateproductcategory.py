#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddOrUpdateProductCategory(StoredProcedureTestCase):
    def test_add_or_update__product_category(self):
        addedNote = add_note(self.db)
        addedProductCategory = add_or_update_product_category(db=self.db,
                                                                    category="Superheroes",
                                                                    shortForm="hero",
                                                                    noteId=addedNote["note_id"])
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

def add_or_update_product_category(db, category, shortForm, noteId):
    productCategory = {
        "category": category,
        "user_id": 1,
        "short_form": shortForm,
        "note_id": noteId
    }
    db.call_procedure("AddOrUpdateProductCategory", 
                        tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"]
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
