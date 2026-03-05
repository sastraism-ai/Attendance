
import sqlite3

conn = sqlite3.connect("saradhi.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS employees(
id INTEGER PRIMARY KEY,
name TEXT,
email TEXT,
password TEXT,
role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_id INTEGER,
date TEXT,
check_in TEXT,
check_out TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS work_reports(
id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_id INTEGER,
date TEXT,
task TEXT
)
""")

employees=[
(1,"Jayavardhan","jay@saradhi.ai","123","employee"),
(2,"Pavan","pavan@saradhi.ai","123","employee"),
(3,"Kumar","kumar@saradhi.ai","123","employee"),
(4,"Nikhil","nikhil@saradhi.ai","123","employee"),
(5,"Lokesh","lokesh@saradhi.ai","123","employee"),
(6,"Nithyakalyani","nithya@saradhi.ai","123","employee"),
(7,"Harini","harini@saradhi.ai","123","employee"),
(8,"Venkatesh","admin@saradhi.ai","admin","admin")
]

c.executemany("INSERT OR IGNORE INTO employees VALUES(?,?,?,?,?)",employees)

conn.commit()
conn.close()

print("Database initialized")
