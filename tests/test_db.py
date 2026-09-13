import sqlite3,unittest
from expense_tracker.db import init_db,seed
class T(unittest.TestCase):
 def test_schema(self):
  c=sqlite3.connect(':memory:');init_db(c);seed(c);self.assertEqual(c.execute('select count(*) from categories').fetchone()[0],6)
