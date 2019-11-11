import os
import sys
import fire
import code
import sqlite3


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)
  
cur = conn.cursor()

sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "Incomplete",
    userid INTEGER DEFAULT "",
    projectid INTEGER DEFAULT ""
  )

"""
cur.execute(sql)
conn.commit()


sql = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
  )

"""

cur.execute(sql)
conn.commit()


sql = """
CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    userid INTEGER DEFAULT ""
      )

"""

cur.execute(sql)
conn.commit()
