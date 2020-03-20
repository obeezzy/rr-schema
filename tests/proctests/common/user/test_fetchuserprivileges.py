#!/usr/bin/env python3
import unittest
import json
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class FetchUserPrivileges(StoredProcedureTestCase):
    def test_fetch_user_privileges(self):
        addedRRUser = add_rr_user(db=self.db,
                                    user="Spider-Man",
                                    firstName="Miles",
                                    lastName="Morales")
        addedUserPrivilege = add_user_privilege(db=self.db,
                                                userId=addedRRUser["user_id"],
                                                userPrivilege={
                                                    "type": "sales"
                                                })
        fetchedUserPrivileges = fetch_user_privileges(db=self.db,
                                                        userId=addedRRUser["user_id"])

        self.assertEqual(addedUserPrivilege["user_privileges"],
                            json.loads(fetchedUserPrivileges["user_privileges"]),
                            "User privileges field mismatch.")

def add_rr_user(db, user, firstName, lastName):
    user = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "user_id": 1
    }

    rrUserTable = db.schema.get_table("rr_user")
    result = rrUserTable.insert("user",
                                "first_name",
                                "last_name",
                                "user_id") \
                        .values(tuple(user.values())) \
                        .execute()
    user.update(DatabaseResult(result).fetch_one("user_id"))
    return user

def add_user_privilege(db, userId, userPrivilege):
    userPrivilege = {
        "user_id": userId,
        'user_privileges': userPrivilege
    }
    userPrivilegeTable = db.schema.get_table("user_privilege")
    result = userPrivilegeTable.insert("user_id AS user_id",
                                        "privileges AS user_privileges") \
                                .values(tuple(userPrivilege.values())) \
                                .execute()
    userPrivilege.update(DatabaseResult(result).fetch_one("user_privilege_id"))
    return userPrivilege

def fetch_user_privileges(db, userId):
    sqlResult = db.call_procedure("FetchUserPrivileges", (userId,))
    return DatabaseResult(sqlResult).fetch_one()

if __name__ == '__main__':
    unittest.main()