import csv
import sqlite3

conn = sqlite3.connect("friday.db")
cursor = conn.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
# cursor.execute(query)
# query = "CREATE TABLE reminders(id integer primary key AUTOINCREMENT, task_name text not null,reminder_time Text not null)"
# cursor.execute(query)
# Create table if not exists
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS reminders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     task_name TEXT NOT NULL,
#     interval INTEGER NOT NULL
# )
# """)
# query = """
# CREATE TABLE IF NOT EXISTS reminders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     task_name TEXT NOT NULL,
#     interval INTEGER NOT NULL
# )
# """
# cursor.execute(query)
        
# query = "INSERT INTO sys_command VALUES (null,'notepad','C:\\Windows\\System32\\notepad.exe')"
# cursor.execute(query)
# conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'gmail','https://mail.google.com/mail/u/0/#inbox')"
# cursor.execute(query)
# conn.commit()

# query = "DELETE FROM sys_command where name ='Notepad'"
# cursor.execute(query)
# conn.commit()

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# query= "DROP Table reminders"
# cursor.execute(query)
# conn.commit()

# query= "DROP Table reminders"
# cursor.execute(query)
# conn.commit()

# query = "INSERT INTO contacts VALUES (null,'Clara James', '09 755 371046', 'null')"
# cursor.execute(query)
# conn.commit()

# desired_columns_indices = [0, 16]  # Adjust this based on your actual column structure

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
    
#     for row in csvreader:
#         # Check if the row has enough columns for the desired indices
#         if len(row) > max(desired_columns_indices):  # Ensure the row has at least as many columns as the max index
#             # Extract the selected columns
#             selected_data = []
#             for i in desired_columns_indices:
#                 # If the index exists in the row, append its value, otherwise use an empty string or None
#                 selected_data.append(row[i] if i < len(row) else "")
            
#             # Insert into the database
#             cursor.execute('''INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?);''', tuple(selected_data))
#         else:
#             print(f"Skipping row, not enough columns: {row}")

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])