#!/usr/bin/env python3
import unittest
import json
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class UpdateUserPrivileges(StoredProcedureTestCase):
    def test_update_user_privileges(self):
        addedRRUser = add_rr_user(db=self.db,
                                    user="Spider-Man",
                                    firstName="Miles",
                                    lastName="Morales")
        addedUserPrivileges = add_user_privileges(db=self.db,
                                                        userPrivileges={
                                                            "type": "purchase"
                                                        },
                                                        userId=addedRRUser["user_id"])
        updatedUserPrivileges = update_user_privileges(db=self.db,
                                                        userPrivileges={
                                                            "type": "sales"
                                                        },
                                                        userId=addedRRUser["user_id"])
        fetchedUserPrivileges = fetch_user_privileges(db=self.db,
                                                        userId=addedRRUser["user_id"])

        self.assertEqual(updatedUserPrivileges["user_privileges"],
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

def fetch_user_privileges(db, userId):
    print("UserId=", userId)
    userPrivilegeTable = db.schema.get_table("user_privilege")
    rowResult = userPrivilegeTable.select("user_id AS user_id",
                                            "privileges AS user_privileges") \
                                .where("user_id = :userId") \
                                .bind("userId", userId) \
                                .execute()
    return DatabaseResult(rowResult).fetch_one()

def add_user_privileges(db, userPrivileges, userId):
    userPrivilegesDict = {
        "user_privileges": userPrivileges,
        "user_id": userId
    }

    userPrivilegesTable = db.schema.get_table("user_privilege")
    result = userPrivilegesTable.insert("privileges",
                                        "user_id") \
                                    .values(tuple(userPrivilegesDict.values())) \
                                    .execute()
    return userPrivilegesDict

def update_user_privileges(db, userPrivileges, userId):
    sqlResult = db.call_procedure("UpdateUserPrivileges", (json.dumps(userPrivileges), userId))
    return {
        "user_privileges": userPrivileges,
        "user_id": userId
    }

if __name__ == '__main__':
    unittest.main()