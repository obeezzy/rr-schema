#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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
        "username": user,
        "password": password
    }

    db.call_procedure("AddSqlUser", tuple(user.values()))
    return user

def change_password(db, user, newPassword):
    db.call_procedure("ChangePassword", [user, newPassword])

def drop_user(db, user):
    db.execute(f"""DROP USER {user}""")

if __name__ == '__main__':
    unittest.main()
