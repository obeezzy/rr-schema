#!/usr/bin/env python3
import unittest
import json
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ViewUsers(StoredProcedureTestCase):
    def test_view_users(self):
        user1 = add_rr_user(db=self.db,
                            user="Spider-Man",
                            firstName="Miles",
                            lastName="Morales",
                            active=True)
        user2 = add_rr_user(db=self.db,
                            user="Spider-Gwen",
                            firstName="Gwen",
                            lastName="Stacy",
                            active=False)
        user3 = add_rr_user(db=self.db,
                            user="Silk",
                            firstName="Cindy",
                            lastName="Moon",
                            active=True,
                            archived=True)

        viewedUsers = view_users(db=self.db,
                                    archived=False)

        self.assertEqual(len(viewedUsers), 2, "Expected 2 users.")
        self.assertEqual(user1["user_id"],
                            viewedUsers[0]["user_id"],
                            "User ID field mismatch.")
        self.assertEqual(user1["user"],
                            viewedUsers[0]["user"],
                            "User field mismatch.")
        self.assertEqual(user1["active"],
                            viewedUsers[0]["active"],
                            "Active field mismatch.")
        self.assertEqual(user1["user"],
                            viewedUsers[0]["user"],
                            "User field mismatch.")

        self.assertEqual(user2["user_id"],
                            viewedUsers[1]["user_id"],
                            "User ID field mismatch.")
        self.assertEqual(user2["user"],
                            viewedUsers[1]["user"],
                            "User field mismatch.")
        self.assertEqual(user2["active"],
                            viewedUsers[1]["active"],
                            "Active field mismatch.")
        self.assertEqual(user2["user"],
                            viewedUsers[1]["user"],
                            "User field mismatch.")

        viewedUsers = view_users(db=self.db,
                                    archived=True)

        self.assertEqual(len(viewedUsers), 1, "Expected 1 user.")
        self.assertEqual(user3["user_id"],
                            viewedUsers[0]["user_id"],
                            "User ID field mismatch.")
        self.assertEqual(user3["user"],
                            viewedUsers[0]["user"],
                            "User field mismatch.")
        self.assertEqual(user3["active"],
                            viewedUsers[0]["active"],
                            "Active field mismatch.")
        self.assertEqual(user3["user"],
                            viewedUsers[0]["user"],
                            "User field mismatch.")

def add_rr_user(db, user, firstName, lastName, active, archived=False):
    user = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "active": active,
        "archived": archived,
        "user_id": 1
    }

    rrUserTable = db.schema.get_table("rr_user")
    result = rrUserTable.insert("user",
                                "first_name",
                                "last_name",
                                "active",
                                "archived",
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

def view_users(db, archived):
    sqlResult = db.call_procedure("ViewUsers", (archived,))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()