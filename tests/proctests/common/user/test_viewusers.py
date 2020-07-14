#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ViewUsers(StoredProcedureTestCase):
    def test_view_users(self):
        user1 = add_user(db=self.db,
                            user="Spider-Man",
                            firstName="Miles",
                            lastName="Morales",
                            active=True)
        user2 = add_user(db=self.db,
                            user="Spider-Gwen",
                            firstName="Gwen",
                            lastName="Stacy",
                            active=False)
        user3 = add_user(db=self.db,
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
                            "User ID mismatch.")
        self.assertEqual(user1["username"],
                            viewedUsers[0]["username"],
                            "User mismatch.")
        self.assertEqual(user1["active"],
                            viewedUsers[0]["active"],
                            "Active mismatch.")
        self.assertEqual(user1["username"],
                            viewedUsers[0]["username"],
                            "User mismatch.")

        self.assertEqual(user2["user_id"],
                            viewedUsers[1]["user_id"],
                            "User ID mismatch.")
        self.assertEqual(user2["username"],
                            viewedUsers[1]["username"],
                            "User mismatch.")
        self.assertEqual(user2["active"],
                            viewedUsers[1]["active"],
                            "Active mismatch.")
        self.assertEqual(user2["username"],
                            viewedUsers[1]["username"],
                            "User mismatch.")

        viewedUsers = view_users(db=self.db,
                                    archived=True)

        self.assertEqual(len(viewedUsers), 1, "Expected 1 user.")
        self.assertEqual(user3["user_id"],
                            viewedUsers[0]["user_id"],
                            "User ID mismatch.")
        self.assertEqual(user3["username"],
                            viewedUsers[0]["username"],
                            "User mismatch.")
        self.assertEqual(user3["active"],
                            viewedUsers[0]["active"],
                            "Active mismatch.")
        self.assertEqual(user3["username"],
                            viewedUsers[0]["username"],
                            "User mismatch.")

def add_user(db, user, firstName, lastName, active, archived=False):
    user = {
        "username": user,
        "first_name": firstName,
        "last_name": lastName,
        "active": active,
        "archived": archived,
        "user_id": 1
    }

    db.execute("""INSERT INTO rr_user (username,
                                        first_name,
                                        last_name,
                                        active,
                                        archived,
                                        user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS user_id,
                    username,
                    first_name,
                    last_name,
                    active,
                    archived""", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "active": row["active"],
            "archived": row["archived"]
        }
    return result

def add_user_privilege(db, userId, userPrivilege):
    userPrivilege = {
        "user_id": userId,
        'user_privileges': userPrivilege
    }
    db.execute("""INSERT INTO user_privilege (user_id,
                                                privileges)
                VALUES (%s, %s)
                RETURNING user_id,
                    privileges AS user_privileges""", tuple(userPrivileges.values()))

def view_users(db, archived):
    db.call_procedure("ViewUsers", [archived])
    results = []
    for row in db:
        result = {
            "user_id": row["user_id"],
            "username": row["username"],
            "active": row["active"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
