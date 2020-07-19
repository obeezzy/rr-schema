#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class ViewSaleCart(StoredProcedureTestCase):
    def test_view_sale_cart(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Yamaha")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Keyboard")
        currentProductQuantity1 = add_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=57.29)
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=Decimal("183.32"),
                                        retailPrice=Decimal("182.95"))
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Guitar")
        currentProductQuantity2 = add_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=23.86)
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=Decimal("183.32"),
                                        retailPrice=Decimal("182.95"))

        productCategory2 = add_product_category(db=self.db,
                                                category="Logitech")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="MX Master")
        currentProductQuantity3 = add_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=92.88)
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=Decimal("400.32"),
                                        retailPrice=Decimal("382.95"))

        client = add_client(db=self.db,
                            firstName="Carol",
                            lastName="Denvers",
                            preferredName="Ms. Marvel",
                            phoneNumber="38492847")
        customer = add_customer(db=self.db,
                            clientId=client["client_id"])
        note = add_note(db=self.db,
                        note="Note")
        saleTransaction = add_sale_transaction(self.db,
                                                        customerId=customer["customer_id"],
                                                        customerName=client["preferred_name"],
                                                        noteId=note["note_id"])
        soldProduct1 = add_sold_product(db=self.db,
                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=Decimal("89.66"),
                                                    quantity=43.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=Decimal("459.34"),
                                                    discount=Decimal("96.38"),
                                                    noteId=note["note_id"])
        soldProduct2 = add_sold_product(db=self.db,
                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=Decimal("27.36"),
                                                    quantity=54.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=Decimal("389.22"),
                                                    discount=Decimal("28.38"),
                                                    noteId=note["note_id"])
        soldProduct3 = add_sold_product(db=self.db,
                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=Decimal("36.86"),
                                                    quantity=64.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=Decimal("483.23"),
                                                    discount=Decimal("38.48"),
                                                    noteId=note["note_id"])

        viewedSaleCart = view_sale_transaction_products(db=self.db,
                                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                                    saleTransactionArchived=False,
                                                                    soldProductArchived=False)

        self.assertEqual(len(viewedSaleCart), 3, "Expected 3 transactions.")
        self.assertEqual(viewedSaleCart[0]["sale_transaction_id"],
                            saleTransaction["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(viewedSaleCart[0]["customer_name"],
                            saleTransaction["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(viewedSaleCart[0]["customer_id"],
                            saleTransaction["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(viewedSaleCart[0]["customer_phone_number"],
                            client["phone_number"],
                            "Customer phone number mismatch.")
        self.assertEqual(viewedSaleCart[0]["suspended"],
                            saleTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedSaleCart[0]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedSaleCart[0]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedSaleCart[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedSaleCart[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedSaleCart[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedSaleCart[0]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(viewedSaleCart[0]["unit_price"],
                            soldProduct1["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedSaleCart[0]["quantity"],
                            soldProduct1["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedSaleCart[0]["available_quantity"],
                            currentProductQuantity1["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedSaleCart[0]["product_unit_id"],
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedSaleCart[0]["product_unit"],
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedSaleCart[0]["cost_price"],
                            productUnit1["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(viewedSaleCart[0]["retail_price"],
                            productUnit1["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(viewedSaleCart[0]["cost"],
                            soldProduct1["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedSaleCart[0]["discount"],
                            soldProduct1["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSaleCart[0]["currency"],
                            soldProduct1["currency"],
                            "Currency mismatch.")

        self.assertEqual(viewedSaleCart[1]["sale_transaction_id"],
                            saleTransaction["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(viewedSaleCart[1]["customer_name"],
                            saleTransaction["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(viewedSaleCart[1]["customer_id"],
                            saleTransaction["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(viewedSaleCart[1]["customer_phone_number"],
                            client["phone_number"],
                            "Customer phone number mismatch.")
        self.assertEqual(viewedSaleCart[1]["suspended"],
                            saleTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedSaleCart[1]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedSaleCart[1]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedSaleCart[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedSaleCart[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedSaleCart[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedSaleCart[1]["product"],
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(viewedSaleCart[1]["unit_price"],
                            soldProduct2["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedSaleCart[1]["quantity"],
                            soldProduct2["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedSaleCart[1]["available_quantity"],
                            currentProductQuantity2["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedSaleCart[1]["product_unit_id"],
                            productUnit2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedSaleCart[1]["product_unit"],
                            productUnit2["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedSaleCart[1]["cost_price"],
                            productUnit2["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(viewedSaleCart[1]["retail_price"],
                            productUnit2["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(viewedSaleCart[1]["cost"],
                            soldProduct2["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedSaleCart[1]["discount"],
                            soldProduct2["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSaleCart[1]["currency"],
                            soldProduct2["currency"],
                            "Currency mismatch.")

        self.assertEqual(viewedSaleCart[2]["sale_transaction_id"],
                            saleTransaction["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(viewedSaleCart[2]["customer_name"],
                            saleTransaction["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(viewedSaleCart[2]["customer_id"],
                            saleTransaction["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(viewedSaleCart[2]["customer_phone_number"],
                            client["phone_number"],
                            "Customer phone number mismatch.")
        self.assertEqual(viewedSaleCart[2]["suspended"],
                            saleTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedSaleCart[2]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedSaleCart[2]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedSaleCart[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedSaleCart[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedSaleCart[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedSaleCart[2]["product"],
                            product3["product"],
                            "Product mismatch.")
        self.assertEqual(viewedSaleCart[2]["unit_price"],
                            soldProduct3["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedSaleCart[2]["quantity"],
                            soldProduct3["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedSaleCart[2]["available_quantity"],
                            currentProductQuantity3["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedSaleCart[2]["product_unit_id"],
                            productUnit3["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedSaleCart[2]["product_unit"],
                            productUnit3["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedSaleCart[2]["cost_price"],
                            productUnit3["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(viewedSaleCart[2]["retail_price"],
                            productUnit3["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(viewedSaleCart[2]["cost"],
                            soldProduct3["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedSaleCart[2]["discount"],
                            soldProduct3["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSaleCart[2]["currency"],
                            soldProduct3["currency"],
                            "Currency mismatch.")

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

def add_sold_product(db, saleTransactionId, productId, unitPrice, quantity, productUnitId, cost, noteId, discount):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
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

    db.execute("""INSERT INTO sold_product (sale_transaction_id,
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
                RETURNING id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
                    note_id,
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
            "note_id": row["note_id"],
            "discount": row["discount"],
            "user_id": row["user_id"]
        }
    return result

def add_product_unit(db, productId, unit, baseUnitEquivalent, costPrice, retailPrice):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "base_unit_equivalent": baseUnitEquivalent,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "preferred": True,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            base_unit_equivalent,
                                            cost_price,
                                            retail_price,
                                            preferred,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id,
                    product_id,
                    unit,
                    base_unit_equivalent,
                    cost_price,
                    retail_price,
                    preferred,
                    currency,
                    user_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "unit": row["unit"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "preferred": row["preferred"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def add_sale_transaction(db, customerId, customerName, noteId, discount=0, suspended=False):
    saleTransaction = {
        "customer_id": customerId,
        "customer_name": customerName,
        "note_id": noteId,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_id,
                                                customer_name,
                                                note_id,
                                                discount,
                                                suspended,
                                                user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_id,
                    customer_name,
                    note_id,
                    discount,
                    suspended,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "note_id": row["note_id"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def add_product_quantity(db, productId, quantity):
    currentProductQuantity = {
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
                    user_id""", tuple(currentProductQuantity.values()))
    result = {}
    for row in db:
        result = {
            "product_quantity_id": row["product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def add_client(db, firstName, lastName, preferredName, phoneNumber):
    client = {
        "first_name": firstName,
        "last_name": lastName,
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "user_id": 1
    }

    db.execute("""INSERT INTO client (first_name,
                                        last_name,
                                        preferred_name,
                                        phone_number,
                                        user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS client_id,
                    first_name,
                    last_name,
                    preferred_name,
                    phone_number,
                    user_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "user_id": row["user_id"]
        }
    return result

def add_customer(db, clientId):
    customer = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO customer (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS customer_id,
                    client_id,
                    user_id""", tuple(customer.values()))
    result = {}
    for row in db:
        result = {
            "customer_id": row["customer_id"],
            "client_id": row["client_id"],
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
            "user_id": row["user_id"]
        }
    return result

def view_sale_transaction_products(db, saleTransactionId, saleTransactionArchived=None, soldProductArchived=None):
    args = {
        "sale_transaction_id": saleTransactionId,
        "sale_transaction_archived": saleTransactionArchived,
        "sold_product_archived": soldProductArchived
    }
    db.call_procedure("ViewSaleCart", tuple(args.values()))
    results = []
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_name": row["customer_name"],
            "customer_id": row["customer_id"],
            "customer_phone_number": row["customer_phone_number"],
            "total_cost": row["total_cost"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "note": row["note"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"],
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product_id": row["product_id"],
            "product": row["product"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "unit_price": row["unit_price"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "quantity": row["quantity"],
            "available_quantity": row["available_quantity"],
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
