#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta

class FilterSaleReport(StoredProcedureTestCase):
    @unittest.skip("Needs to be refactored!")
    def test_view_sale_report(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Powerful Weapons")
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
                                                category="Weak Weapons")
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

        saleTransaction1 = add_sale_transaction(db=self.db,
                                                customerName="Selena Kyle")
        soldProduct1 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            unitPrice=locale.currency(38.27),
                                            quantity=583.5,
                                            productUnitId=productUnit1["product_unit_id"],
                                            cost=locale.currency(378.28),
                                            discount=locale.currency(8.28))
        soldProduct2 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            unitPrice=locale.currency(38.27),
                                            quantity=583.5,
                                            productUnitId=productUnit2["product_unit_id"],
                                            cost=locale.currency(378.28),
                                            discount=locale.currency(8.28))
        soldProduct3 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            unitPrice=locale.currency(38.27),
                                            quantity=583.5,
                                            productUnitId=productUnit2["product_unit_id"],
                                            cost=locale.currency(378.28),
                                            discount=locale.currency(8.28))

        saleTransaction2 = add_sale_transaction(db=self.db,
                                                customerName="Harley Quinn")
        soldProduct4 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction2["sale_transaction_id"],
                                            productId=product3["product_id"],
                                            unitPrice=locale.currency(38.27),
                                            quantity=583.5,
                                            productUnitId=productUnit3["product_unit_id"],
                                            cost=locale.currency(378.28),
                                            discount=locale.currency(8.28))
        today = date.today()
        tomorrow = today + timedelta(days=1)
        filteredSaleReport = filter_sale_report(db=self.db,
                                                filterColumn="product_category",
                                                filterText="powerful",
                                                sortColumn="product_category",
                                                sortOrder="ascending",
                                                fromDate=today,
                                                toDate=tomorrow)

        self.assertEqual(len(filteredSaleReport), 2, "Expected 2 transactions.")
        self.assertEqual(filteredSaleReport[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(filteredSaleReport[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(filteredSaleReport[0]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredSaleReport[0]["product"],
                            product2["product"],
                            "Product mismatch")
        self.assertEqual(filteredSaleReport[0]["quantity_sold"],
                            soldProduct2["quantity"] + soldProduct3["quantity"],
                            "Quantity mismatch")
        self.assertEqual(filteredSaleReport[0]["total_revenue"],
                            soldProduct2["cost"] + soldProduct3["cost"],
                            "Total revenue mismatch")

        self.assertEqual(filteredSaleReport[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(filteredSaleReport[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(filteredSaleReport[1]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredSaleReport[1]["product"],
                            product1["product"],
                            "Product mismatch")
        self.assertEqual(filteredSaleReport[1]["quantity_sold"],
                            soldProduct1["quantity"],
                            "Quantity mismatch")
        self.assertEqual(filteredSaleReport[1]["total_revenue"],
                            soldProduct1["cost"],
                            "Total revenue mismatch")

        filteredSaleReport = filter_sale_report(db=self.db,
                                                filterColumn="product_category",
                                                filterText="weak",
                                                sortColumn="product_category",
                                                sortOrder="ascending",
                                                fromDate=today,
                                                toDate=tomorrow)

        self.assertEqual(len(filteredSaleReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredSaleReport[0]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(filteredSaleReport[0]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch")
        self.assertEqual(filteredSaleReport[0]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredSaleReport[0]["product"],
                            product3["product"],
                            "Product mismatch")
        self.assertEqual(filteredSaleReport[0]["quantity_sold"],
                            soldProduct4["quantity"],
                            "Quantity mismatch")
        self.assertEqual(filteredSaleReport[0]["total_revenue"],
                            soldProduct4["cost"],
                            "Total revenue mismatch")

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

def add_sold_product(db, saleTransactionId, productId, unitPrice, quantity, productUnitId, cost, discount):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
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

def add_sale_transaction(db, customerName):
    saleTransaction = {
        "customer_name": customerName,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_name,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_name,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_name": row["customer_name"],
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

def filter_sale_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate):
    db.call_procedure("FilterSaleReport", [filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate])
    results = []
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product": row["product"],
            "quantity_sold": row["quantity_sold"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "total_revenue": row["total_revenue"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
