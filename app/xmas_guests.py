import sqlite3

# Open the database connection
conn = sqlite3.connect('Christmas_Table.db')

# Create a cursor
cursor = conn.cursor()

# Execute the query to select all entries
cursor.execute('SELECT * FROM guests')

# Commit the changes
conn.commit()

# Print the Guest List
for row in cursor.fetchall():
    print(row)

# Close the database connection
conn.close()
