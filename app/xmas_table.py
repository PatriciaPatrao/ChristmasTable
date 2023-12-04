import sqlite3

# Open the database connection
conn = sqlite3.connect('Christmas_Table.db')

# Create a cursor
cursor = conn.cursor()

# Execute the query to select all entries
cursor.execute('SELECT * FROM guests')

# Execute the query to delete all entries
# cursor.execute('DELETE FROM guests')

# Commit the changes
conn.commit()

# Close the database connection
conn.close()

# print to make sure all entries were delected
# print('All entries have been deleted from the database.')
