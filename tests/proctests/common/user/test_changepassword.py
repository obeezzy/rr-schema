#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ChangePassword(StoredProcedureTestCase):
    def setUp(self):
        super().setUp()
        self.userName = "testuser"
        add_sql_user(db=self.db,
                        user=self.userName,
                        password="mypassword")

    def test_change_password(self):
        change_password(db=self.db,
                        user=self.userName,
                        newPassword="passwordmy")

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

def change_password(db, user, newPassword):
    sqlResult = db.call_procedure("ChangePassword", (user, newPassword))
    return DatabaseResult(sqlResult).fetch_one()

def drop_user(db, user):
    db.session.sql(f"DROP USER '{user}'@'localhost';") \
        .execute()

if __name__ == '__main__':
    unittest.main()