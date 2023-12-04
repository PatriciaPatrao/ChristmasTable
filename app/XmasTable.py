import sqlite3

# Open the database connection
conn = sqlite3.connect('Christmas_Table.db')

# Create a cursor
cursor = conn.cursor()

# Execute the query
cursor.execute('DELETE FROM guests')

# Retrieve the results
results = cursor.fetchall()

# Print the results
for name in results:
    print(name)

# Close the database connection
conn.close()
