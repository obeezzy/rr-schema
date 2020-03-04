#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, OperationalError, DatabaseResult

class AddStockProduct(StoredProcedureTestCase):
    def test_add_stock_product(self):
        addedProduct = add_stock_product(self.db)
        fetchedProduct = fetch_stock_product(self.db)

        self.assertEqual(addedProduct, fetchedProduct, "Product table field mismatch.")

    def test_raise_duplicate_entry_exception(self):
        with self.assertRaises(OperationalError) as context:
            add_stock_product(self.db)
            add_stock_product(self.db)

        self.assertEqual(context.exception.errno,
                            DatabaseErrorCodes.USER_DEFINED_EXCEPTION)

def add_stock_product(db):
    product = {
        "product_category_id": 1,
        "product": "Product",
        "short_form": "Short",
        "description": "Description",
        "barcode": "Barcode",
        "divisible": int(True),
        "image": None,
        "note_id": None,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddStockProduct",
                                        tuple(product.values())
    )

    addedProduct = DatabaseResult(sqlResult).fetch_one()
    product.update(addedProduct)
    return product

def fetch_stock_product(db):
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