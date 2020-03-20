#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, OperationalError, DatabaseResult

class AddSqlUser(StoredProcedureTestCase):
    def test_add_sql_user(self):
        self.userName = "testuser"
        addedUser = add_sql_user(db=self.db,
                                    user=self.userName,
                                    password="mypassword")
        fetchedUser = fetch_sql_user(db=self.db,
                                    user=self.userName)

        self.assertEqual(addedUser["user"], fetchedUser["user"], "User field mismatch.")
        self.assertEqual("localhost", fetchedUser["host"], "Host field mismatch.")

    def tearDown(self):
        drop_user(db=self.db, user=self.userName)
        super().tearDown()

def add_sql_user(db, user, password):
    user = {
        "user": user,
        "password": password
    }

    sqlResult = db.call_procedure("AddSqlUser",
                                    tuple(user.values()))

    user.update(DatabaseResult(sqlResult).fetch_one())
    return user

def fetch_sql_user(db, user):
    sqlResult = db.session.sql(f"SELECT host, user FROM mysql.user WHERE user = '{user}'") \
                    .execute()
    return DatabaseResult(sqlResult).fetch_one()

def drop_user(db, user):
    db.session.sql(f"DROP USER '{user}'@'localhost';") \
        .execute()

if __name__ == '__main__':
    unittest.main()