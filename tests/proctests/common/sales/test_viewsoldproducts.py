#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

class ViewSoldProducts(StoredProcedureTestCase):
    def test_view_sold_products(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Consoles")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Xbox One")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="box(es)",
                                        costPrice=locale.currency(95.22),
                                        retailPrice=locale.currency(199.33))
        productCategory2 = add_product_category(db=self.db,
                                                category="Mice")
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Logitech MX Master")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="box(es)",
                                        costPrice=locale.currency(95.22),
                                        retailPrice=locale.currency(199.33))
        note = add_note(db=self.db, note="Disregard this note")
        saleTransaction = add_sale_transaction(db=self.db,
                                                customerName="Mary-Jane Watson")
        soldProduct1 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            productUnitId=productUnit1["product_unit_id"],
                                            unitPrice=locale.currency(1038.38),
                                            quantity=375.25,
                                            cost=locale.currency(69.57),
                                            discount=locale.currency(38.21))
        soldProduct2 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            productUnitId=productUnit1["product_unit_id"],
                                            unitPrice=locale.currency(38.38),
                                            quantity=99.25,
                                            cost=locale.currency(39.57),
                                            discount=locale.currency(38.21))
        soldProduct3 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            productUnitId=productUnit2["product_unit_id"],
                                            unitPrice=locale.currency(23.38),
                                            quantity=399.25,
                                            cost=locale.currency(11.57),
                                            discount=locale.currency(53.21),
                                            noteId=note["note_id"])
        viewedSoldProducts = view_sold_products(db=self.db,
                                                saleTransactionId=saleTransaction["sale_transaction_id"])

        self.assertEqual(len(viewedSoldProducts), 3, "Expected 3 sold products.")
        self.assertEqual(viewedSoldProducts[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedSoldProducts[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedSoldProducts[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedSoldProducts[0]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(viewedSoldProducts[0]["unit_price"],
                            soldProduct1["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedSoldProducts[0]["quantity"],
                            soldProduct1["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedSoldProducts[0]["product_unit_id"],
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedSoldProducts[0]["product_unit"],
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedSoldProducts[0]["quantity"],
                            soldProduct1["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedSoldProducts[0]["cost"],
                            soldProduct1["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedSoldProducts[0]["discount"],
                            soldProduct1["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSoldProducts[0]["currency"],
                            soldProduct1["currency"],
                            "Currency mismatch.")
        self.assertEqual(viewedSoldProducts[0]["note_id"],
                            None,
                            "Note ID mismatch.")
        self.assertEqual(viewedSoldProducts[0]["note"],
                            None,
                            "Note mismatch.")
        self.assertEqual(viewedSoldProducts[0]["user_id"],
                            soldProduct1["user_id"],
                            "User ID mismatch.")

        self.assertEqual(viewedSoldProducts[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedSoldProducts[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedSoldProducts[1]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedSoldProducts[1]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(viewedSoldProducts[1]["unit_price"],
                            soldProduct2["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedSoldProducts[1]["quantity"],
                            soldProduct2["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedSoldProducts[1]["product_unit_id"],
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedSoldProducts[1]["product_unit"],
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedSoldProducts[1]["cost"],
                            soldProduct2["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedSoldProducts[1]["discount"],
                            soldProduct2["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSoldProducts[1]["currency"],
                            soldProduct2["currency"],
                            "Currency mismatch.")
        self.assertEqual(viewedSoldProducts[1]["note_id"],
                            None,
                            "Note ID mismatch.")
        self.assertEqual(viewedSoldProducts[1]["note"],
                            None,
                            "Note mismatch.")
        self.assertEqual(viewedSoldProducts[1]["user_id"],
                            soldProduct2["user_id"],
                            "User ID mismatch.")

        self.assertEqual(viewedSoldProducts[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedSoldProducts[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedSoldProducts[2]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedSoldProducts[2]["product"],
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(viewedSoldProducts[2]["unit_price"],
                            soldProduct3["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedSoldProducts[2]["quantity"],
                            soldProduct3["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedSoldProducts[2]["product_unit_id"],
                            productUnit2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedSoldProducts[2]["product_unit"],
                            productUnit2["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedSoldProducts[2]["cost"],
                            soldProduct3["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedSoldProducts[2]["discount"],
                            soldProduct3["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSoldProducts[2]["currency"],
                            soldProduct3["currency"],
                            "Currency mismatch.")
        self.assertEqual(viewedSoldProducts[2]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedSoldProducts[2]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedSoldProducts[2]["user_id"],
                            soldProduct3["user_id"],
                            "User ID mismatch.")

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

def add_note(db, note):
    note = {
        "note": note,
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id,
                    note,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "note": row["note"],
            "user_id": row["user_id"],
        }
    return result

def add_sale_transaction(db, customerName):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_id,
                                                customer_name,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_id,
                    customer_name,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "user_id": row["user_id"]
        }
    return result

def add_sold_product(db, saleTransactionId, productId, productUnitId, unitPrice, quantity, cost, discount="$0", noteId=None):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
        "product_id": productId,
        "product_unit_id": productUnitId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "cost": cost,
        "discount": discount,
        "currency": "NGN",
        "note_id": noteId,
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
                                            note_id,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    product_unit_id,
                    unit_price,
                    quantity,
                    cost,
                    discount,
                    currency,
                    note_id,
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
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def view_sold_products(db, saleTransactionId, suspended=False, archived=False):
    db.call_procedure("ViewSoldProducts", (saleTransactionId, suspended, archived))
    results = []
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product_id": row["product_id"],
            "product": row["product"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "note": row["note"],
            "archived": row["archived"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"],
            "username": row["username"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
