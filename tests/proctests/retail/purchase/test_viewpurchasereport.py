#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class ViewPurchaseReport(StoredProcedureTestCase):
    def test_view_purchase_report(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Weapons")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Mjolnir")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(6.38),
                                        retailPrice=locale.currency(50.38))
        currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=38.28)
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Captain America's shield")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(489.28),
                                        retailPrice=locale.currency(550.38))
        currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=66.28)

        productCategory2 = add_product_category(db=self.db,
                                                category="More Weapons")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Hawkeye's arrow")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(138456.83),
                                        retailPrice=locale.currency(383593.32))
        currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=78.90)

        purchaseTransaction1 = add_purchase_transaction(db=self.db,
                                                        vendorName="Selena Kyle")
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=locale.currency(38.27),
                                                    quantity=583.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=locale.currency(378.28),
                                                    discount=locale.currency(8.28))
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=locale.currency(38.27),
                                                    quantity=583.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=locale.currency(378.28),
                                                    discount=locale.currency(8.28))
        purchasedProduct3 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=locale.currency(38.27),
                                                    quantity=583.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=locale.currency(378.28),
                                                    discount=locale.currency(8.28))

        purchaseTransaction2 = add_purchase_transaction(db=self.db,
                                                        vendorName="Harley Quinn")
        purchasedProduct4 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction2["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=locale.currency(38.27),
                                                    quantity=583.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=locale.currency(378.28),
                                                    discount=locale.currency(8.28))
        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedPurchaseReport = view_purchase_report(db=self.db,
                                                        fromDate=today,
                                                        toDate=tomorrow)

        self.assertEqual(len(viewedPurchaseReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedPurchaseReport[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedPurchaseReport[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedPurchaseReport[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedPurchaseReport[0]["product"],
                            product1["product"],
                            "Product mismatch")
        self.assertEqual(viewedPurchaseReport[0]["quantity_bought"],
                            purchasedProduct1["quantity"],
                            "Quantity mismatch")
        self.assertEqual(viewedPurchaseReport[0]["total_expenditure"],
                            purchasedProduct1["cost"],
                            "Total expenditure mismatch")

        self.assertEqual(viewedPurchaseReport[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedPurchaseReport[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedPurchaseReport[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedPurchaseReport[1]["product"],
                            product2["product"],
                            "Product mismatch")
        self.assertEqual(viewedPurchaseReport[1]["quantity_bought"],
                            purchasedProduct2["quantity"] + purchasedProduct3["quantity"],
                            "Quantity mismatch")
        self.assertEqual(viewedPurchaseReport[1]["total_expenditure"],
                            locale.currency(Decimal(purchasedProduct2["cost"].strip(self.db.currency_symbol)) + Decimal(purchasedProduct3["cost"].strip(self.db.currency_symbol))),
                            "Total expenditure mismatch")

        self.assertEqual(viewedPurchaseReport[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedPurchaseReport[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch")
        self.assertEqual(viewedPurchaseReport[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedPurchaseReport[2]["product"],
                            product3["product"],
                            "Product mismatch")
        self.assertEqual(viewedPurchaseReport[2]["quantity_bought"],
                            purchasedProduct4["quantity"],
                            "Quantity mismatch")
        self.assertEqual(viewedPurchaseReport[2]["total_expenditure"],
                            purchasedProduct4["cost"],
                            "Total expenditure mismatch")

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

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, discount=0):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": productId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "currency": "NGN",
        "cost": cost,
        "discount": discount,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchased_product (purchase_transaction_id,
                                                    product_id,
                                                    unit_price,
                                                    quantity,
                                                    product_unit_id,
                                                    currency,
                                                    cost,
                                                    discount,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS purchased_product_id,
                    purchase_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
                    discount,
                    user_id""", tuple(purchasedProduct.values()))
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row["purchased_product_id"],
            "product_id": row["product_id"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "currency": row["currency"],
            "cost": row["cost"],
            "discount": row["discount"],
            "user_id": row["user_id"]
        }
    return result

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            base_unit_equivalent,
                                            preferred,
                                            cost_price,
                                            retail_price,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id,
                    product_id,
                    unit,
                    base_unit_equivalent,
                    preferred,
                    cost_price,
                    retail_price,
                    currency,
                    user_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "unit": row["unit"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "preferred": row["preferred"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def add_purchase_transaction(db, vendorName):
    purchaseTransaction = {
        "vendor_name": vendorName,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_name,
                                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_name,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_name": row["vendor_name"],
            "user_id": row["user_id"]
        }
    return result

def add_current_product_quantity(db, productId, quantity):
    currentProductQuantity = {
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
                    user_id""", tuple(currentProductQuantity.values()))
    result = {}
    for row in db:
        result = {
            "current_product_quantity_id": row["current_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def view_purchase_report(db, fromDate, toDate):
    db.call_procedure("ViewPurchaseReport", [fromDate, toDate])
    results = []
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product_id": row["product_id"],
            "product": row["product"],
            "quantity_bought": row["quantity_bought"],
            "product_unit_id": row["product_unit_id"],
            "product_unit_": row["product_unit"],
            "total_expenditure": row["total_expenditure"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
