#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddSoldProduct(StoredProcedureTestCase):
    def test_add_sold_product(self):
        addedProductCategory = add_product_category(self.db)
        addedProduct = add_product(self.db,
                                    productCategoryId=addedProductCategory["product_category_id"])
        addedProductUnit = add_product_unit(self.db,
                            productId=addedProduct["product_id"])
        addedSaleTransaction = add_sale_transaction(self.db)
        addedSoldProduct = add_sold_product(self.db,
                                            saleTransactionId=addedSaleTransaction["sale_transaction_id"], productId=addedProduct["product_id"],
                                            productUnitId=addedProductUnit["product_unit_id"])
        fetchedSoldProduct = fetch_sold_product(self.db)

        self.assertEqual(addedSoldProduct["sold_product_id"],
                            fetchedSoldProduct["sold_product_id"],
                            "Sold product ID mismatch.")
        self.assertEqual(addedSoldProduct["sale_transaction_id"],
                            fetchedSoldProduct["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(addedSoldProduct["product_id"],
                            fetchedSoldProduct["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(addedSoldProduct["product_unit_id"],
                            fetchedSoldProduct["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(addedSoldProduct["unit_price"],
                            fetchedSoldProduct["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(addedSoldProduct["quantity"],
                            fetchedSoldProduct["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(addedSoldProduct["cost"],
                            fetchedSoldProduct["cost"],
                            "Cost mismatch.")
        self.assertEqual(addedSoldProduct["discount"],
                            fetchedSoldProduct["discount"],
                            "Discount mismatch.")
        self.assertEqual(addedSoldProduct["currency"],
                            fetchedSoldProduct["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedSoldProduct["user_id"],
                            fetchedSoldProduct["user_id"],
                            "User ID mismatch.")

def add_product_category(db):
    productCategory = {
        "category": "Category",
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
    result.update(productCategory)
    return result

def add_product(db, productCategoryId):
    product = {
        "product_category_id": productCategoryId,
        "product": "Product",
        "user_id": 1
    }

    db.execute("""INSERT INTO product (product_category_id,
                                        product,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"]
        }
    result.update(product)
    return result

def add_product_unit(db, productId):
    productUnit = {
        "product_id": productId,
        "unit": "unit",
        "base_unit_equivalent": 1,
        "cost_price": Decimal("200.00"),
        "retail_price": Decimal("420.00"),
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            base_unit_equivalent,
                                            cost_price,
                                            retail_price,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"]
        }
    result.update(productUnit)
    return result

def add_sale_transaction(db):
    saleTransaction = {
        "customer_name": "Customer name",
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_name,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS sale_transaction_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"]
        }
    result.update(saleTransaction)
    return result

def add_sold_product(db, saleTransactionId, productId, productUnitId):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
        "product_id": productId,
        "product_unit_id": productUnitId,
        "unit_price": Decimal("1038.39"),
        "quantity": Decimal("183.25"),
        "cost": Decimal("1832.28"),
        "discount": Decimal("138.23"),
        "currency": "NGN",
        "user_id": 1
    }

    db.call_procedure("AddSoldProduct",
                        tuple(soldProduct.values()))
    result = {}
    for row in db:
        result = {
            "sold_product_id": row[0]
        }
    result.update(soldProduct)
    return result

def fetch_sold_product(db):
    db.execute("""SELECT id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    product_unit_id,
                    unit_price,
                    quantity,
                    cost,
                    discount,
                    currency,
                    user_id
                FROM sold_product""")
    result = {}
    for row in db:
        result = {
            "sold_product_id": row["sold_product_id"],
            "sale_transaction_id": row["sale_transaction_id"],
            "product_id": row["product_id"],
            "product_unit_id": row["product_unit_id"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
