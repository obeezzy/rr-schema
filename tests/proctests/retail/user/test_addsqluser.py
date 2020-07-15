#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddSqlUser(StoredProcedureTestCase):
    def test_add_sql_user(self):
        self.userName = "testuser"
        addedUser = add_sql_user(db=self.db,
                                    user=self.userName,
                                    password="mypassword")
        fetchedUser = fetch_sql_user(db=self.db,
                                    user=self.userName)

        self.assertEqual(addedUser["username"], fetchedUser["username"], "User name mismatch.")

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

def fetch_sql_user(db, user):
    db.execute("""SELECT usename AS username FROM pg_user
                WHERE usename = %s""", [user])
    result = {}
    for row in db:
        result = {
            "username": row["username"]
        }
    return result

def drop_user(db, user):
    db.execute(f"""DROP USER {user}""")

if __name__ == '__main__':
    unittest.main()
