#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, OperationalError, DatabaseResult

class AddOrUpdateStockProductCategory(StoredProcedureTestCase):
    def test_add_or_update_stock_product_category(self):
        addedProductCategory = add_or_update_stock_product_category(db=self.db,
                                                                    category="Superheroes",
                                                                    shortForm="hero")
        fetchedProductCategory = fetch_stock_product_category(self.db)

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

def add_or_update_stock_product_category(db, category, shortForm):
    productCategory = {
        "category": category,
        "short_form": shortForm,
        "note_id": 1,
        "user_id": 1
    }
    sqlResult = db.call_procedure("AddOrUpdateStockProductCategory", 
                                    tuple(productCategory.values()))
    productCategory.update(DatabaseResult(sqlResult).fetch_one())
    return productCategory

def fetch_stock_product_category(db):
    productCategoryTable = db.schema.get_table("product_category")
    rowResult = productCategoryTable.select("id AS product_category_id",
                                            "category AS category",
                                            "short_form AS short_form",
                                            "note_id AS note_id",
                                            "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()
    

if __name__ == '__main__':
    unittest.main()