#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class GrantUserPrivilege(StoredProcedureTestCase):
    @unittest.skip("Needs to be refactored.")
    def setUp(self):
        super().setUp()
        self.userName = "testuser"
        add_sql_user(db=self.db,
                        user=self.userName,
                        password="mypassword")

    def test_grant_user_privileges(self):
        grant_sql_privilege(db=self.db,
                            user=self.userName,
                            privilege="SELECT")

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

def add_user(db, user, firstName, lastName):
    user = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "user_id": 1
    }

    db.execute("""INSERT INTO rr_user (username,
                                        first_name,
                                        last_name,
                                        user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS user_id,
                    username,
                    first_name,
                    last_name""", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"]
        }
    return result

def grant_sql_privilege(db, user, privilege):
    db.call_procedure("GrantSqlPrivilege", [user, privilege])

def fetch_sql_user(db, user):
    db.execute("""SELECT usename as username FROM pg_user WHERE user = %s""", [user])
    result = {}
    for row in db:
        result = {
            "username": row["username"],
        }
    return result

def drop_user(db, user):
    db.execute(f"""DROP USER {user}""")

if __name__ == '__main__':
    unittest.main()
