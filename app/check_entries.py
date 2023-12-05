import sqlite3

# Searching for a specific name

name_to_check = 'John'


def get_guest(name):
    '''Returns information about a guest when given a name'''

    # Open the database connection
    conn = sqlite3.connect('Christmas_Table.db')

    # Create a cursor
    cursor = conn.cursor()

    # Execute the query to select all entries and fetch one
    cursor.execute('''SELECT * FROM guests
                   WHERE name =?''',
                   (name,))
    guest = cursor.fetchone()

    # Close the DB
    conn.close()

    # Print Guest
    if guest is None:
        print('Select a registered Guest!\n')
        return None
    else:
        return guest


# Get guest info
guest_info = get_guest(name_to_check)

if guest_info is not None:
    print("Name: ", guest_info[1])
    print("Surname: ", guest_info[2])
    print("Gender: ", guest_info[3])
    print("Age: ", guest_info[4])
    print("Country: ", guest_info[5])
    print("Thoughts: ", guest_info[6])
    print("Number of Gifts: ", guest_info[7])
    print("Good Behaviour: ", guest_info[8])

    if guest_info[8] == 'Off Course!':
        print('''
              Congratulations!
              Your seat at the Christmas Table is secured!
              Get ready to jingle all the way!!
            ''')
    else:
        print('''
            Looks like Santa has detected some questionable behavior on his radar!
            Your case is under review...
            Hang tight and reconsider those life choices!
            ''')
