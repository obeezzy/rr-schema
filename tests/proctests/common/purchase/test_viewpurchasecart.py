#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ViewPurchaseCart(StoredProcedureTestCase):
    def test_view_purchase_cart(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Yamaha")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Keyboard")
        currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=57.29)
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=183.32,
                                        retailPrice=182.95)
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Guitar")
        currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=23.86)
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=183.32,
                                        retailPrice=182.95)

        productCategory2 = add_product_category(db=self.db,
                                                category="Logitech")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="MX Master")
        currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=92.88)
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=400.32,
                                        retailPrice=382.95)

        client = add_client(db=self.db,
                            firstName="Carol",
                            lastName="Denvers",
                            preferredName="Ms. Marvel",
                            phoneNumber="38492847")
        vendor = add_vendor(db=self.db,
                            clientId=client["client_id"])
        note = add_note(db=self.db,
                        note="Note",
                        tableName="purchase")
        purchaseTransaction = add_purchase_transaction(self.db,
                                                        vendorId=vendor["vendor_id"],
                                                        vendorName=client["preferred_name"],
                                                        noteId=note["note_id"])
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=89.66,
                                                    quantity=43.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=459.34,
                                                    discount=96.38,
                                                    noteId=note["note_id"])
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=27.36,
                                                    quantity=54.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=389.22,
                                                    discount=28.38,
                                                    noteId=note["note_id"])
        purchasedProduct3 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=36.86,
                                                    quantity=64.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=483.23,
                                                    discount=38.48,
                                                    noteId=note["note_id"])

        viewedPurchaseCart = view_purchase_transaction_products(db=self.db,
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
                            "Quantity mismatch.")
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
                            currentProductQuantity1["quantity"],
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
                            "Quantity mismatch.")
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
                            currentProductQuantity2["quantity"],
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
                            "Quantity mismatch.")
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
                            currentProductQuantity3["quantity"],
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

    productCategoryTable = db.schema.get_table("product_category")
    result = productCategoryTable.insert("category",
                                            "user_id") \
                                    .values(tuple(productCategory.values())) \
                                    .execute()
    productCategory.update(DatabaseResult(result).fetch_one("product_category_id"))
    return productCategory

def add_product(db, productCategoryId, product):
    productDict = {
        "product_category_id": productCategoryId,
        "product": product,
        "user_id": 1
    }

    productTable = db.schema.get_table("product")
    result = productTable.insert("product_category_id",
                                    "product",
                                    "user_id") \
                            .values(tuple(productDict.values())) \
                            .execute()
    productDict.update(DatabaseResult(result).fetch_one("product_id"))
    return productDict

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, noteId, discount=0):
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

    purchasedProductTable = db.schema.get_table("purchased_product")
    result = purchasedProductTable.insert("purchase_transaction_id",
                                            "product_id",
                                            "unit_price",
                                            "quantity",
                                            "product_unit_id",
                                            "currency",
                                            "cost",
                                            "note_id",
                                            "discount",
                                            "user_id") \
                                    .values(tuple(purchasedProduct.values())) \
                                    .execute()
    purchasedProduct.update(DatabaseResult(result).fetch_one("purchased_product_id"))
    return purchasedProduct

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

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "base_unit_equivalent",
                                        "cost_price",
                                        "retail_price",
                                        "preferred",
                                        "currency",
                                        "user_id") \
                                .values(tuple(productUnit.values())) \
                                .execute()
    productUnit.update(DatabaseResult(result).fetch_one("product_unit_id"))
    return productUnit

def add_purchase_transaction(db, vendorId, vendorName, noteId, discount=0, suspended=False):
    purchaseTransaction = {
        "vendor_id": vendorId,
        "vendor_name": vendorName,
        "note_id": noteId,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_id",
                                                "vendor_name",
                                                "note_id",
                                                "discount",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

def add_current_product_quantity(db, productId, quantity):
    currentProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.insert("product_id",
                                                "quantity",
                                                "user_id") \
                                            .values(tuple(currentProductQuantity.values())) \
                                            .execute()
    currentProductQuantity.update(DatabaseResult(result).fetch_one("current_product_quantity_id"))
    return currentProductQuantity

def add_client(db, firstName, lastName, preferredName, phoneNumber):
    client = {
        "first_name": firstName,
        "last_name": lastName,
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "user_id": 1
    }

    clientTable = db.schema.get_table("client")
    result = clientTable.insert("first_name",
                                "last_name",
                                "preferred_name",
                                "phone_number",
                                "user_id") \
                            .values(tuple(client.values())) \
                            .execute()
    client.update(DatabaseResult(result).fetch_one("client_id"))
    return client

def add_vendor(db, clientId):
    vendor = {
        "client_id": clientId,
        "user_id": 1
    }

    vendorTable = db.schema.get_table("vendor")
    result = vendorTable.insert("client_id",
                                "user_id") \
                            .values(tuple(vendor.values())) \
                            .execute()
    vendor.update(DatabaseResult(result).fetch_one("vendor_id"))
    return vendor

def add_note(db, note, tableName):
    noteDict = {
        "note": note,
        "table_name": tableName,
        "user_id": 1
    }

    noteTable = db.schema.get_table("note")
    result = noteTable.insert("note",
                                "table_name",
                                "user_id") \
                        .values(tuple(noteDict.values())) \
                        .execute()
    noteDict.update(DatabaseResult(result).fetch_one("note_id"))
    return noteDict

def view_purchase_transaction_products(db, purchaseTransactionId, purchaseTransactionArchived=None, purchasedProductArchived=None):
    args = {
        "purchase_transaction_id": purchaseTransactionId,
        "purchase_transaction_archived": purchaseTransactionArchived,
        "purchased_product_archived": purchasedProductArchived
    }
    sqlResult = db.call_procedure("ViewPurchaseCart", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()