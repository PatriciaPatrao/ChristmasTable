import sqlite3

conn = sqlite3.connect('Christmas_Table.db')

cursor = conn.cursor()

# Erase table
cursor.execute('DROP TABLE guests')

conn.commit()

conn.close()

print('Table guest has been deleted!')
