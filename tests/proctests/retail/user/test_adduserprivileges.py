#!/usr/bin/env python3
import unittest
from psycopg2.extras import Json
from proctests.utils import StoredProcedureTestCase

class AddUserPrivileges(StoredProcedureTestCase):
    def test_add_user_privileges(self):
        addedUser = add_user(db=self.db,
                                user="Spider-Man",
                                firstName="Miles",
                                lastName="Morales")
        addedUserPrivileges = add_user_privileges(db=self.db,
                                                    userPrivileges={
                                                        "type": "sales"
                                                    },
                                                    userId=addedUser["user_id"])
        fetchedUserPrivileges = fetch_user_privileges(db=self.db,
                                                        userId=addedUser["user_id"])

        self.assertEqual(addedUserPrivileges["privileges"],
                            fetchedUserPrivileges["privileges"],
                            "User privileges mismatch.")

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
                    last_name,
                    user_id""", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "user_id": row["user_id"]
        }
    return result

def fetch_user_privileges(db, userId):
    db.execute("""SELECT user_id,
                            privileges
                FROM user_privilege
                WHERE user_id = %s""", [userId])
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "privileges": row["privileges"]
        }
    return result

def add_user_privileges(db, userPrivileges, userId):
    db.call_procedure("AddUserPrivileges", [Json(userPrivileges), userId])
    return {
        "privileges": userPrivileges,
        "user_id": userId
    }

if __name__ == '__main__':
    unittest.main()
