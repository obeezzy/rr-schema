#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ViewSaleCart(StoredProcedureTestCase):
    def test_view_sale_cart(self):
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
        customer = add_customer(db=self.db,
                            clientId=client["client_id"])
        note = add_note(db=self.db,
                        note="Note",
                        tableName="sale")
        saleTransaction = add_sale_transaction(self.db,
                                                        customerId=customer["customer_id"],
                                                        customerName=client["preferred_name"],
                                                        noteId=note["note_id"])
        soldProduct1 = add_sold_product(db=self.db,
                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=89.66,
                                                    quantity=43.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=459.34,
                                                    discount=96.38,
                                                    noteId=note["note_id"])
        soldProduct2 = add_sold_product(db=self.db,
                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=27.36,
                                                    quantity=54.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=389.22,
                                                    discount=28.38,
                                                    noteId=note["note_id"])
        soldProduct3 = add_sold_product(db=self.db,
                                                    saleTransactionId=saleTransaction["sale_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=36.86,
                                                    quantity=64.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=483.23,
                                                    discount=38.48,
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

def add_sold_product(db, saleTransactionId, productId, unitPrice, quantity, productUnitId, cost, noteId, discount=0):
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

    soldProductTable = db.schema.get_table("sold_product")
    result = soldProductTable.insert("sale_transaction_id",
                                            "product_id",
                                            "unit_price",
                                            "quantity",
                                            "product_unit_id",
                                            "currency",
                                            "cost",
                                            "note_id",
                                            "discount",
                                            "user_id") \
                                    .values(tuple(soldProduct.values())) \
                                    .execute()
    soldProduct.update(DatabaseResult(result).fetch_one("sold_product_id"))
    return soldProduct

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

def add_sale_transaction(db, customerId, customerName, noteId, discount=0, suspended=False):
    saleTransaction = {
        "customer_id": customerId,
        "customer_name": customerName,
        "note_id": noteId,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_id",
                                                "customer_name",
                                                "note_id",
                                                "discount",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(saleTransaction.values())) \
                                        .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

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

def add_customer(db, clientId):
    customer = {
        "client_id": clientId,
        "user_id": 1
    }

    customerTable = db.schema.get_table("customer")
    result = customerTable.insert("client_id",
                                "user_id") \
                            .values(tuple(customer.values())) \
                            .execute()
    customer.update(DatabaseResult(result).fetch_one("customer_id"))
    return customer

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

def view_sale_transaction_products(db, saleTransactionId, saleTransactionArchived=None, soldProductArchived=None):
    args = {
        "sale_transaction_id": saleTransactionId,
        "sale_transaction_archived": saleTransactionArchived,
        "sold_product_archived": soldProductArchived
    }
    sqlResult = db.call_procedure("ViewSaleCart", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()