#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, MySqlError

class AddStockProduct(StoredProcedureTestCase):
    def test_add_stock_product(self):
        try:
            addedProduct = add_stock_product(self)
            fetchedProduct = fetch_stock_product(self)

            print("Added:", addedProduct)
            print("Fetched:", fetchedProduct)
            self.assertEqual(addedProduct, fetchedProduct, "Product table field mismatch.")
        except:
            raise
        finally:
            self.db.cleanup()

    def test_raise_duplicate_entry_exception(self):
        try:
            with self.assertRaises(MySqlError) as context:
                add_stock_product(self)
                add_stock_product(self)

            self.assertEqual(context.exception.errno,
                                DatabaseClient.ErrorCodes.USER_DEFINED_EXCEPTION)
        except:
            raise
        finally:
            self.db.cleanup()

def add_stock_product(self):
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

    return self.db.call_procedure("AddStockProduct",
                                    list(product.values())
    )

def fetch_stock_product(self):
    return self.db.execute("SELECT product_category_id, \
                            product, \
                            short_form, \
                            description, \
                            barcode, \
                            divisible, \
                            image, \
                            note_id, \
                            user_id \
                            FROM product")

if __name__ == '__main__':
    unittest.main()