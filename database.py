import sqlite3 as sl

base = sl.connect('users_stg.db')
try:
    with base:
        base.execute("""
            CREATE TABLE SETTINGS (
                token TEXT,
                lang TEXT
            );
        """)
except sl.OperationalError as e:
    print("Something went wrong.", e)
