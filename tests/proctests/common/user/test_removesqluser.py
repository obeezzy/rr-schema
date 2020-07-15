#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class RemoveSqlUser(StoredProcedureTestCase):
    def setUp(self):
        super().setUp()
        self.userName = "testuser"
        self.addedUser = add_sql_user(db=self.db,
                                        user=self.userName,
                                        password="mypassword")

    def test_remove_sql_user(self):
        fetchedUser = fetch_sql_user(db=self.db,
                                        user=self.addedUser["username"])
        self.assertNotEqual(fetchedUser, None, "User should be returned.")

        remove_sql_user(db=self.db, user=self.userName)
        fetchedUser = fetch_sql_user(db=self.db,
                                        user=self.userName)
        self.assertNotEqual(fetchedUser, None, "User should be returned.")

    def tearDown(self):
        drop_user_if_exists(db=self.db, user=self.userName)
        super().tearDown()

def add_sql_user(db, user, password):
    user = {
        "username": user,
        "password": password
    }

    db.call_procedure("AddSqlUser", tuple(user.values()))
    return user

def remove_sql_user(db, user):
    db.call_procedure("RemoveSqlUser", [user])

def fetch_sql_user(db, user):
    db.execute(f"SELECT usename AS username FROM pg_user WHERE user = %s", [user])
    result = {}
    for row in db:
        result = {
            "username": row["username"]
        }
    return result

def drop_user_if_exists(db, user):
    db.execute(f"DROP USER IF EXISTS {user}")

if __name__ == '__main__':
    unittest.main()
