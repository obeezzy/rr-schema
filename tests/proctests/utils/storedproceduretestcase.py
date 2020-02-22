import unittest
import logging
import sys
import datetime
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
    def now(self):
        return datetime.datetime.now().replace(second=0, microsecond=0)

    @property
    def elapsed(self):
        return time.time() - self.startTime

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)