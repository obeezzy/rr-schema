import unittest
import logging
import sys
from .databaseclient import DatabaseClient

class StoredProcedureTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.client = DatabaseClient()

    def tearDown(self):
        pass

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)