#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, MySqlError

class AddStockProduct(StoredProcedureTestCase):
    def test_add_stock_product(self):
        try:
            inputValues = add_stock_product(self)
            storedValues = fetch_stock_product(self)

            self.assertEqual(inputValues, storedValues, "Product table field mismatch.")
        except:
            raise
        finally:
            self.client.cleanup()

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
            self.client.cleanup()

def add_stock_product(self):
    iProductCategoryId = 1
    iProduct = "Product"
    iShortForm = "Short"
    iDescription = "Description"
    iBarcode = "Barcode"
    iDivisible = True
    iImage = None
    iNoteId = None
    iUserId = 1

    self.client.call_procedure("AddStockProduct", [
        iProductCategoryId,
        iProduct,
        iShortForm,
        iDescription,
        iBarcode,
        iDivisible,
        iImage,
        iNoteId,
        iUserId
    ])

    return (iProductCategoryId,
            iProduct,
            iShortForm,
            iDescription,
            iBarcode,
            iDivisible,
            iImage,
            iNoteId,
            iUserId)

def fetch_stock_product(self):
    self.client.execute("SELECT product_category_id, \
                            product, \
                            short_form, \
                            description, \
                            barcode, \
                            divisible, \
                            image, \
                            note_id, \
                            user_id \
                            FROM product")

    return self.client.fetchone()

if __name__ == '__main__':
    unittest.main()