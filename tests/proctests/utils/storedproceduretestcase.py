import unittest
import logging
import sys
from datetime import datetime
import time
from .databaseclient import DatabaseClient

class StoredProcedureTestCase(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseClient()

    def tearDown(self):
        print(f"({round(self.elapsed, 2)}s)")

    @property
    def elapsed(self):
        return time.time() - self.startTime

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)