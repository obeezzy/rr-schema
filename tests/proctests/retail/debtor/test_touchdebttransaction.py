#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
import time

class TouchDebtTransaction(StoredProcedureTestCase):
    @unittest.skip("TouchDebtTransaction works through mysql client, but not through this test. Fix later.")
    def test_touch_debt_transaction(self):
        add_debt_transaction(self.db)
        time.sleep(3)
        touch_debt_transaction(self.db)
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        self.assertLess(fetchedDebtTransaction["created"],
                        fetchedDebtTransaction["last_edited"],
                        "Date/time not updated.")

def add_debt_transaction(db):
    debtTransaction = {
        "debtor_id": 1,
        "table_ref": "sale_transaction",
        "table_id": 20,
        "note_id": 1,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                table_ref,
                                                table_id,
                                                note_id,
                                                user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS debt_transaction_id,
                    debtor_id,
                    table_ref,
                    table_id,
                    note_id,
                    user_id""", tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "table_ref": row["table_ref"],
            "table_id": row["table_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def touch_debt_transaction(db):
    debtTransaction = {
        "debt_transaction_id": 1,
        "user_id": 1
    }

    db.call_procedure("TouchDebtTransaction",
                        tuple(debtTransaction.values()))

def fetch_debt_transaction(db):
    db.execute("""SELECT id AS debt_transaction_id,
                            debtor_id,
                            table_ref,
                            table_id,
                            note_id,
                            created,
                            last_edited,
                            user_id)
                FROM debt_transaction""")
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "table_ref": row["table_ref"],
            "table_id": row["table_id"],
            "note_id": row["note_id"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
