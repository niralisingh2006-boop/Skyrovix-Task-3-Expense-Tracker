import sqlite3
def connect(path='expenses.db'):
 c=sqlite3.connect(path);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');return c
def init_db(c):
 c.executescript("""CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY,name TEXT UNIQUE NOT NULL);CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY,amount REAL NOT NULL CHECK(amount>0),category_id INTEGER NOT NULL,description TEXT NOT NULL,expense_date TEXT NOT NULL,FOREIGN KEY(category_id) REFERENCES categories(id));CREATE TABLE IF NOT EXISTS budgets(id INTEGER PRIMARY KEY,month TEXT UNIQUE NOT NULL,amount REAL NOT NULL CHECK(amount>0));""");c.commit()
def seed(c):
 for x in ['Food','Travel','Education','Bills','Shopping','Other']:c.execute('INSERT OR IGNORE INTO categories(name) VALUES(?)',(x,))
 c.commit()
