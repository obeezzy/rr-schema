#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, DatabaseResult

class RemoveSqlUser(StoredProcedureTestCase):
    def setUp(self):
        super().setUp()
        self.userName = "testuser"
        self.addedUser = add_sql_user(db=self.db,
                                        user=self.userName,
                                        password="mypassword")

    def test_remove_sql_user(self):
        fetchedUser = fetch_sql_user(db=self.db,
                                        user=self.addedUser["user"])
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
        "user": user,
        "password": password
    }

    sqlResult = db.call_procedure("AddSqlUser",
                                    tuple(user.values()))
    user.update(DatabaseResult(sqlResult).fetch_one())
    return user

def remove_sql_user(db, user):
    db.call_procedure("RemoveSqlUser", (user,))

def fetch_sql_user(db, user):
    sqlResult = db.session.sql(f"SELECT host, user FROM mysql.user WHERE user = '{user}'") \
                    .execute()
    return DatabaseResult(sqlResult).fetch_one()

def drop_user_if_exists(db, user):
    db.session.sql(f"DROP USER IF EXISTS '{user}'@'localhost';") \
        .execute()

if __name__ == '__main__':
    unittest.main()