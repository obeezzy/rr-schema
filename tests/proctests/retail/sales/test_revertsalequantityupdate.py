#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

class RevertSaleQuantityUpdate(StoredProcedureTestCase):
    def test_revert_sale_quantity_update(self):
        addedSaleTransaction = add_sale_transaction(db=self.db,
                                                        customerName="Tony Stark")
        addedProductCategory = add_product_category(db=self.db,
                                                    category="Suits")
        addedProduct = add_product(db=self.db,
                                    productCategoryId=addedProductCategory["product_category_id"],
                                    product="Iron Man suit")
        addedProductUnit = add_product_unit(db=self.db,
                                            productId=addedProduct["product_id"],
                                            unit="unit(s)",
                                            costPrice=locale.currency(283.18),
                                            retailPrice=locale.currency(844.23))
        addedProductQuantity = add_product_quantity(db=self.db,
                                                    productId=addedProduct["product_id"],
                                                    quantity=200.25)
        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"], fetchedProductQuantity["quantity"], "Quantity mismatch.")

        addedSoldProduct = add_sold_product(db=self.db,
                                            saleTransactionId=addedSaleTransaction["sale_transaction_id"],
                                            productId=addedProduct["product_id"],
                                            productUnitId=addedProductUnit["product_unit_id"],
                                            unitPrice=locale.currency(389.23),
                                            quantity=88.32,
                                            cost=locale.currency(184.28),
                                            discount=locale.currency(101.32))
        alter_product_quantity(db=self.db,
                                productId=addedProduct["product_id"],
                                newQuantity=round(addedProductQuantity["quantity"] - addedSoldProduct["quantity"], 2))
        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(round(addedProductQuantity["quantity"] - addedSoldProduct["quantity"], 2),
                            fetchedProductQuantity["quantity"],
                            "Quantity mismatch.")

        revert_sale_quantity_update(db=self.db, 
                                        saleTransactionId=addedSaleTransaction["sale_transaction_id"])

        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"],
                            fetchedProductQuantity["quantity"],
                            "Quantity mismatch.")

def add_sale_transaction(db, customerName, suspended=False):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_id,
                                                customer_name,
                                                suspended,
                                                user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_id,
                    customer_name,
                    suspended,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id,
                    category,
                    user_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "category": row["category"],
            "user_id": row["user_id"]
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
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            cost_price,
                                            retail_price,
                                            base_unit_equivalent,
                                            preferred,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id,
                    product_id,
                    cost_price,
                    retail_price,
                    base_unit_equivalent,
                    preferred,
                    currency,
                    user_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "preferred": row["preferred"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def add_sold_product(db, saleTransactionId, productId, productUnitId, unitPrice, quantity, cost, discount=0):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
        "product_id": productId,
        "product_unit_id": productUnitId,
        "unit_price": 1038.39,
        "quantity": 183.25,
        "cost": 1832.28,
        "discount": 138.23,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO sold_product (sale_transaction_id,
                                            product_id,
                                            product_unit_id,
                                            unit_price,
                                            quantity,
                                            cost,
                                            discount,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    product_unit_id,
                    unit_price,
                    quantity,
                    cost,
                    discount,
                    currency,
                    user_id""", tuple(soldProduct.values()))
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

def add_product_quantity(db, productId, quantity):
    productQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    db.execute("""INSERT INTO current_product_quantity (product_id,
                                                        quantity,
                                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS current_product_quantity_id,
                    product_id,
                    quantity,
                    user_id""", tuple(productQuantity.values()))
    result = {}
    for row in db:
        result = {
            "current_product_quantity_id": row["current_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def alter_product_quantity(db, productId, newQuantity):
    db.execute("""UPDATE current_product_quantity
                    SET quantity = %s
                    WHERE product_id = %s""", [newQuantity, productId])

def revert_sale_quantity_update(db, saleTransactionId, userId=1):
    db.call_procedure("RevertSaleQuantityUpdate", (saleTransactionId, userId))

def fetch_current_product_quantity(db, productId):
    db.execute("""SELECT id AS current_product_quantity_id,
                            product_id,
                            quantity,
                            user_id
                FROM current_product_quantity
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "current_product_quantity_id": row["current_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
