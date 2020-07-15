#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class RevokeSqlPrivilege(StoredProcedureTestCase):
    @unittest.skip("Needs to be refactored.""")
    def setUp(self):
        self.userName = "testuser"
        super().setUp()
        drop_user(db=self.db, user=self.userName)
        add_sql_user(db=self.db,
                        user=self.userName,
                        password="mypassword")

    def test_revoke_sql_privileges(self):
        grant_sql_privilege(db=self.db,
                            user=self.userName,
                            privilege="SELECT")
        revoke_sql_privilege(db=self.db,
                            user=self.userName,
                            privilege="SELECT")

    def tearDown(self):
        drop_user(db=self.db, user=self.userName)
        super().tearDown()

def add_sql_user(db, user, password):
    user = {
        "user": user,
        "password": password
    }

    db.call_procedure("AddSqlUser", tuple(user.values()))

def add_user(db, user, firstName, lastName):
    user = {
        "username": user,
        "first_name": firstName,
        "last_name": lastName,
        "user_id": 1
    }

    db.execute("""INSERT INTO rr_user (username,
                                        first_name,
                                        last_name)
                VALUES (%s, %s, %s)
                RETURNING id AS user_id,
                    first_name,
                    last_name""", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "user_id": row["user_id"]
        }
    return result

def grant_sql_privilege(db, user, privilege):
    db.execute(f"""GRANT CONNECT ON DATABASE rr_test TO {user}""")
    db.execute(f"""GRANT USAGE ON SCHEMA public TO {user}""")
    db.execute(f"""GRANT {privilege} TO {user}""")

def revoke_sql_privilege(db, user, privilege):
    db.call_procedure("RevokeSqlPrivilege", [user, privilege])

def fetch_sql_user(db, user):
    db.execute(f"""SELECT usename AS username FROM pg_user WHERE username = %s""", [user])
    result = {}
    for row in db:
        result = {
            "username": row["username"]
        }
    return result

def drop_user(db, user):
    db.execute(f"""DROP USER IF EXISTS {user}""")

if __name__ == '__main__':
    unittest.main()
