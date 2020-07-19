#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class ViewPurchaseCart(StoredProcedureTestCase):
    def test_view_purchase_cart(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Yamaha")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Keyboard")
        productQuantity1 = add_product_quantity(db=self.db,
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
        productQuantity2 = add_product_quantity(db=self.db,
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
        productQuantity3 = add_product_quantity(db=self.db,
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
        vendor = add_vendor(db=self.db,
                            clientId=client["client_id"])
        note = add_note(db=self.db,
                        note="Note")
        purchaseTransaction = add_purchase_transaction(self.db,
                                                        vendorId=vendor["vendor_id"],
                                                        vendorName=client["preferred_name"],
                                                        noteId=note["note_id"])
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=Decimal("89.66"),
                                                    quantity=43.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=Decimal("459.34"),
                                                    discount=Decimal("96.38"),
                                                    noteId=note["note_id"])
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=Decimal("27.36"),
                                                    quantity=54.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=Decimal("389.22"),
                                                    discount=Decimal("28.38"),
                                                    noteId=note["note_id"])
        purchasedProduct3 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=Decimal("36.86"),
                                                    quantity=64.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=Decimal("483.23"),
                                                    discount=Decimal("38.48"),
                                                    noteId=note["note_id"])

        viewedPurchaseCart = view_purchase_cart(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    purchaseTransactionArchived=False,
                                                    purchasedProductArchived=False)

        self.assertEqual(len(viewedPurchaseCart), 3, "Expected 3 transactions.")
        self.assertEqual(viewedPurchaseCart[0]["purchase_transaction_id"],
                            purchaseTransaction["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["vendor_name"],
                            purchaseTransaction["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["vendor_id"],
                            purchaseTransaction["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["vendor_phone_number"],
                            client["phone_number"],
                            "Vendor phone number mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["suspended"],
                            purchaseTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["unit_price"],
                            purchasedProduct1["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["quantity"],
                            purchasedProduct1["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["available_quantity"],
                            productQuantity1["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["product_unit_id"],
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["product_unit"],
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["cost_price"],
                            productUnit1["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["retail_price"],
                            productUnit1["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["cost"],
                            purchasedProduct1["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["discount"],
                            purchasedProduct1["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedPurchaseCart[0]["currency"],
                            purchasedProduct1["currency"],
                            "Currency mismatch.")

        self.assertEqual(viewedPurchaseCart[1]["purchase_transaction_id"],
                            purchaseTransaction["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["vendor_name"],
                            purchaseTransaction["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["vendor_id"],
                            purchaseTransaction["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["vendor_phone_number"],
                            client["phone_number"],
                            "Vendor phone number mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["suspended"],
                            purchaseTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["product"],
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["unit_price"],
                            purchasedProduct2["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["quantity"],
                            purchasedProduct2["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["available_quantity"],
                            productQuantity2["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["product_unit_id"],
                            productUnit2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["product_unit"],
                            productUnit2["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["cost_price"],
                            productUnit2["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["retail_price"],
                            productUnit2["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["cost"],
                            purchasedProduct2["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["discount"],
                            purchasedProduct2["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedPurchaseCart[1]["currency"],
                            purchasedProduct2["currency"],
                            "Currency mismatch.")

        self.assertEqual(viewedPurchaseCart[2]["purchase_transaction_id"],
                            purchaseTransaction["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["vendor_name"],
                            purchaseTransaction["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["vendor_id"],
                            purchaseTransaction["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["vendor_phone_number"],
                            client["phone_number"],
                            "Vendor phone number mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["suspended"],
                            purchaseTransaction["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["note_id"],
                            note["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["note"],
                            note["note"],
                            "Note mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["product"],
                            product3["product"],
                            "Product mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["unit_price"],
                            purchasedProduct3["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["quantity"],
                            purchasedProduct3["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["available_quantity"],
                            productQuantity3["quantity"],
                            "Available quantity mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["product_unit_id"],
                            productUnit3["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["product_unit"],
                            productUnit3["unit"],
                            "Product unit mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["cost_price"],
                            productUnit3["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["retail_price"],
                            productUnit3["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["cost"],
                            purchasedProduct3["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["discount"],
                            purchasedProduct3["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedPurchaseCart[2]["currency"],
                            purchasedProduct3["currency"],
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
                    product,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, noteId, discount=Decimal("0.00")):
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

def add_purchase_transaction(db, vendorId, vendorName, noteId, discount=Decimal("0.00"), suspended=False):
    purchaseTransaction = {
        "vendor_id": vendorId,
        "vendor_name": vendorName,
        "note_id": noteId,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_id,
                                                    vendor_name,
                                                    note_id,
                                                    discount,
                                                    suspended,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_id,
                    vendor_name,
                    note_id,
                    discount,
                    suspended,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "note_id": row["note_id"],
            "discount": row["discount"],
            "suspended": row["suspended"],
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

def add_vendor(db, clientId):
    vendor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO vendor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS vendor_id,
                    client_id,
                    user_id""", tuple(vendor.values()))
    result = {}
    for row in db:
        result = {
            "vendor_id": row["vendor_id"],
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

def view_purchase_cart(db, purchaseTransactionId, purchaseTransactionArchived=False, purchasedProductArchived=False):
    args = {
        "purchase_transaction_id": purchaseTransactionId,
        "purchase_transaction_archived": purchaseTransactionArchived,
        "purchased_product_archived": purchasedProductArchived
    }
    db.call_procedure("ViewPurchaseCart", tuple(args.values()))
    results = []
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_name": row["vendor_name"],
            "vendor_id": row["vendor_id"],
            "vendor_phone_number": row["vendor_phone_number"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "note": row["note"],
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product_id": row["product_id"],
            "product": row["product"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "available_quantity": row["available_quantity"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
