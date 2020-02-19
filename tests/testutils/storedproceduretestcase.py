import unittest
from .databaseclient import DatabaseClient

class StoredProcedureTestCase(unittest.TestCase):
    def setUp(self):
        self.client = DatabaseClient()

    def tearDown(self):
        pass