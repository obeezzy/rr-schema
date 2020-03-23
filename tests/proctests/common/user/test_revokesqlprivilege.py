#!/usr/bin/env python3
import unittest
import json
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class RevokeSqlPrivilege(StoredProcedureTestCase):
    def setUp(self):
        super().setUp()
        self.userName = "testuser"
        add_sql_user(db=self.db,
                        user=self.userName,
                        password="mypassword")

    def test_revoke_sql_privileges(self):
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

    sqlResult = db.call_procedure("AddSqlUser",
                                    tuple(user.values()))
    user.update(DatabaseResult(sqlResult).fetch_one())
    return user

def add_user(db, user, firstName, lastName):
    user = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "user_id": 1
    }

    userTable = db.schema.get_table("rr_user")
    result = userTable.insert("user",
                                "first_name",
                                "last_name",
                                "user_id") \
                        .values(tuple(user.values())) \
                        .execute()
    user.update(DatabaseResult(result).fetch_one("user_id"))
    return user

def revoke_sql_privilege(db, user, privilege):
    db.call_procedure("RevokeSqlPrivilege", (user, privilege))

def fetch_sql_user(db, user):
    sqlResult = db.session.sql(f"SELECT user AS user FROM mysql.user WHERE user = '{user}'") \
                    .execute()
    return DatabaseResult(sqlResult).fetch_one()

def drop_user(db, user):
    db.session.sql(f"DROP USER '{user}'@'localhost';") \
        .execute()

if __name__ == '__main__':
    unittest.main()