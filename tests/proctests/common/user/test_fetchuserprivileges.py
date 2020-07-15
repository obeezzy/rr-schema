#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from psycopg2.extras import Json

class FetchUserPrivileges(StoredProcedureTestCase):
    def test_fetch_user_privileges(self):
        addedUser = add_user(db=self.db,
                                    user="Spider-Man",
                                    firstName="Miles",
                                    lastName="Morales")
        addedUserPrivilege = add_user_privilege(db=self.db,
                                                userId=addedUser["user_id"],
                                                userPrivilege={
                                                    "type": "sales"
                                                })
        fetchedUserPrivileges = fetch_user_privileges(db=self.db,
                                                        userId=addedUser["user_id"])

        self.assertEqual(addedUserPrivilege["user_privileges"],
                            fetchedUserPrivileges["user_privileges"],
                            "User privileges mismatch.")

def add_user(db, user, firstName, lastName):
    user = {
        "username": user,
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
            "username": row["username"],
            "user_id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
        }
    return result

def add_user_privilege(db, userId, userPrivilege):
    userPrivilege = {
        "user_id": userId,
        'user_privileges': Json(userPrivilege)
    }

    db.execute("""INSERT INTO user_privilege (user_id,
                                                privileges)
                    VALUES (%s, %s)
                    RETURNING user_id,
                        privileges""", tuple(userPrivilege.values()))
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "user_privileges": row["privileges"],
        }
    return result

def fetch_user_privileges(db, userId):
    db.call_procedure("FetchUserPrivileges", [userId])
    result = {}
    for row in db:
        result = {
            "user_privileges": row["user_privileges"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
