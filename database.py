import sqlite3

conn = sqlite3.connect("billing.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   amount REAL,
                   type TEXT,
                   date TEXT
               )
               """)

cursor.execute("""
              INSERT INTO transactions (name, amount, type, date) 
              VALUES (?, ?, ?, ?)
              """, ("Aavuu", 2000, "deposit", "2026-06-30"))


cursor.execute("SELECT * FROM transactions")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.commit()
conn.close()
print("Database Created Successfully!")
