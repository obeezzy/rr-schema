#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class FilterClients(StoredProcedureTestCase):
    def filter_clients(self):
        try:
            add_single_client(self, 1, "First client", "123456789")
            add_single_client(self, 2, "Second client", "987654321")
            filteredClients = filter_clients(self,
                                            filterColumn="preferred_name",
                                            filterText="Fir",
                                            archived=False)
            fetchedClients = fetch_clients(self)

            self.assertEqual(filteredClients, fetchedClients, "Record mismatch for client table.")
        except:
            raise
        finally:
            self.db.cleanup()

def add_single_client(self, clientId, preferredName, phoneNumber):
    client = {
        "client_id": clientId,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "created": self.now,
        "last_edited": self.now,
        "user_id": 1
    }

    self.db.execute("INSERT INTO client (\
                            id, \
                            first_name, \
                            last_name, \
                            preferred_name, \
                            phone_number, \
                            created, \
                            last_edited, \
                            user_id) \
                            VALUES (\
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s)",
                            tuple(client.values()))

def filter_clients(self, filterColumn, filterText, archived):
    return self.db.call_procedure("FilterClients", [
                                        filterColumn,
                                        filterText,
                                        archived
    ])

def fetch_clients(self):
    return self.db.execute("SELECT id AS client_id, \
                            first_name, \
                            last_name, \
                            preferred_name, \
                            phone_number, \
                            user_id \
                            FROM client")

if __name__ == '__main__':
    unittest.main()