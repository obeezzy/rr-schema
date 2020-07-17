#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class ViewStockReport(StoredProcedureTestCase):
    def test_view_stock_report(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Weapons")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Mjolnir")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=Decimal("6.38"),
                                        retailPrice=Decimal("50.38"))
        productQuantitySnapshot1 = add_product_quantity_snapshot(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=39294.28)
        productQuantity1 = add_product_quantity(db=self.db,
                                                    productId=product1["product_id"],
                                                    quantity=productQuantitySnapshot1["quantity"])
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Captain America's shield")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=Decimal("489.28"),
                                        retailPrice=Decimal("550.38"))
        productQuantitySnapshot2 = add_product_quantity_snapshot(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=3452.28)
        productQuantity2 = add_product_quantity(db=self.db,
                                                    productId=product2["product_id"],
                                                    quantity=productQuantitySnapshot2["quantity"])

        productCategory2 = add_product_category(db=self.db,
                                                category="More Weapons")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Hawkeye's arrow")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=Decimal("138456.83"),
                                        retailPrice=Decimal("383593.32"))
        productQuantitySnapshot3 = add_product_quantity_snapshot(db=self.db,
                                                            productId=product3["product_id"],
                                                            quantity=2333.90)
        productQuantity3 = add_product_quantity(db=self.db,
                                                    productId=product3["product_id"],
                                                    quantity=productQuantitySnapshot3["quantity"])
        saleTransaction1 = add_sale_transaction(db=self.db, 
                                                customerName="Susan Richards",
                                                discount=0)
        soldProduct1 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            unitPrice=Decimal("38.27"),
                                            quantity=29.5,
                                            productUnitId=productUnit1["product_unit_id"],
                                            cost=Decimal("378.28"),
                                            discount=Decimal("8.28"))
        newQuantity1 = productQuantity1["quantity"] - soldProduct1["quantity"]
        alter_product_quantity(db=self.db,
                                productId=product1["product_id"],
                                newQuantity=newQuantity1)

        soldProduct2 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            unitPrice=Decimal("38.27"),
                                            quantity=44.5,
                                            productUnitId=productUnit2["product_unit_id"],
                                            cost=Decimal("378.28"),
                                            discount=Decimal("8.28"))
        soldProduct3 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            unitPrice=Decimal("38.27"),
                                            quantity=33.5,
                                            productUnitId=productUnit2["product_unit_id"],
                                            cost=Decimal("378.28"),
                                            discount=Decimal("8.28"))
        newQuantity2 = productQuantity2["quantity"] - soldProduct2["quantity"] - soldProduct3["quantity"]
        alter_product_quantity(db=self.db,
                                productId=product2["product_id"],
                                newQuantity=newQuantity2)

        purchaseTransaction1 = add_purchase_transaction(db=self.db,
                                                        vendorName="Harley Quinn",
                                                        discount=0)
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=Decimal("38.27"),
                                                    quantity=38.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=Decimal("378.28"),
                                                    discount=Decimal("8.28"))

        purchaseTransaction2 = add_purchase_transaction(db=self.db,
                                                        vendorName="Harley Quinn",
                                                        discount=0)
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction2["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=Decimal("38.27"),
                                                    quantity=22.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=Decimal("378.28"),
                                                    discount=Decimal("8.28"))
        newQuantity3 = productQuantity3["quantity"] + purchasedProduct1["quantity"] + purchasedProduct2["quantity"]
        alter_product_quantity(db=self.db,
                                productId=product3["product_id"],
                                newQuantity=newQuantity3)

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedStockReport = view_stock_report(db=self.db,
                                                fromDate=today,
                                                toDate=tomorrow)

        self.assertEqual(len(viewedStockReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedStockReport[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedStockReport[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedStockReport[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedStockReport[0]["product"],
                            product1["product"],
                            "Product mismatch")
        self.assertEqual(viewedStockReport[0]["quantity_sold"],
                            soldProduct1["quantity"],
                            "Quantity sold mismatch")
        self.assertEqual(viewedStockReport[0]["quantity_bought"],
                            0,
                            "Quantity bought mismatch")
        self.assertEqual(viewedStockReport[0]["quantity_in_stock"],
                            newQuantity1,
                            "Quantity in stock mismatch")

        self.assertEqual(viewedStockReport[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedStockReport[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedStockReport[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedStockReport[1]["product"],
                            product2["product"],
                            "Product mismatch")
        self.assertEqual(viewedStockReport[1]["quantity_sold"],
                            soldProduct2["quantity"] + soldProduct3["quantity"],
                            "Quantity sold mismatch")
        self.assertEqual(viewedStockReport[1]["quantity_bought"],
                            0,
                            "Quantity bought mismatch")
        self.assertEqual(viewedStockReport[1]["quantity_in_stock"],
                            newQuantity2,
                            "Quantity in stock mismatch")

        self.assertEqual(viewedStockReport[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedStockReport[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch")
        self.assertEqual(viewedStockReport[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedStockReport[2]["product"],
                            product3["product"],
                            "Product mismatch")
        self.assertEqual(viewedStockReport[2]["quantity_sold"],
                            0,
                            "Quantity sold mismatch")
        self.assertEqual(viewedStockReport[2]["quantity_bought"],
                            purchasedProduct1["quantity"] + purchasedProduct2["quantity"],
                            "Quantity bought mismatch")
        self.assertEqual(viewedStockReport[2]["quantity_in_stock"],
                            newQuantity3,
                            "Quantity in stock mismatch")

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
            "product_category_id": row["product_category_id"],
            "product_id": row["product_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def add_sale_transaction(db, customerName, discount, suspended=False, noteId=None):
    saleTransaction = {
        "customer_name": customerName,
        "customer_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_name,
                                                customer_id,
                                                discount,
                                                suspended,
                                                note_id,
                                                user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_name,
                    customer_id,
                    discount,
                    suspended,
                    note_id,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_name": row["customer_name"],
            "customer_id": row["customer_id"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def add_purchase_transaction(db, vendorName, discount, suspended=False, noteId=None):
    purchaseTransaction = {
        "vendor_name": vendorName,
        "vendor_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_name,
                                                    vendor_id,
                                                    discount,
                                                    suspended,
                                                    note_id,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_name,
                    vendor_id,
                    discount,
                    suspended,
                    note_id,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_name": row["vendor_name"],
            "vendor_id": row["vendor_id"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def add_sold_product(db, saleTransactionId, productId, unitPrice, quantity, productUnitId, cost, discount=0):
    soldProduct = {
        "sale_transactionId": saleTransactionId,
        "product_id": productId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "currency": "NGN",
        "cost": cost,
        "discount": discount,
        "user_id": 1
    }

    db.execute("""INSERT INTO sold_product (sale_transaction_id,
                                            product_id,
                                            unit_price,
                                            quantity,
                                            product_unit_id,
                                            currency,
                                            cost,
                                            discount,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
                    discount,
                    user_id""", tuple(soldProduct.values()))
    result = {}
    for row in db:
        result = {
            "sold_product_id": row["sold_product_id"],
            "sale_transaction_id": row["sale_transaction_id"],
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

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, noteId=None, discount=0):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": productId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "currency": "NGN",
        "cost": cost,
        "note_id": noteId,
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
                                                    note_id,
                                                    discount,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS purchased_product_id,
                    purchase_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
                    note_id,
                    discount,
                    user_id""", tuple(purchasedProduct.values()))
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row["purchased_product_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "product_id": row["product_id"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "currency": row["currency"],
            "cost": row["cost"],
            "note_id": row["note_id"],
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

def add_product_quantity_snapshot(db, productId, quantity):
    productQuantitySnapshot = {
        "product_id": productId,
        "quantity": quantity,
        "reason": "sale_transaction",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_quantity_snapshot (product_id,
                                                            quantity,
                                                            reason,
                                                            user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS product_quantity_snapshot_id,
                    product_id,
                    quantity,
                    reason,
                    user_id""", tuple(productQuantitySnapshot.values()))
    result = {}
    for row in db:
        result = {
            "product_quantity_snapshot_id": row["product_quantity_snapshot_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "reason": row["reason"],
            "user_id": row["user_id"]
        }
    return result

def add_product_quantity(db, productId, quantity):
    productQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    db.execute("""INSERT INTO product_quantity (product_id,
                                                        quantity,
                                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_quantity_id,
                    product_id,
                    quantity,
                    user_id""", tuple(productQuantity.values()))
    result = {}
    for row in db:
        result = {
            "product_quantity_id": row["product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def alter_product_quantity(db, productId, newQuantity):
    db.execute("""UPDATE product_quantity
                    SET quantity = %s
                    WHERE product_id = %s""", [newQuantity, productId])

def view_stock_report(db, fromDate, toDate):
    db.call_procedure("ViewStockReport", [fromDate, toDate])
    results = []
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product": row["product"],
            "opening_stock_quantity": row["opening_stock_quantity"],
            "quantity_sold": row["quantity_sold"],
            "quantity_bought": row["quantity_bought"],
            "quantity_in_stock": row["quantity_in_stock"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
