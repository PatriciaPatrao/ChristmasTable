import re
import sqlite3
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.config import Config
# from kivy.lang import Builder  # Importe o módulo Builder

# Carregue o arquivo KV manualmente
# Builder.load_file('myapp.kv')


# # App configurations
# Config.set('graphics', 'width', '400')
# Config.set('graphics', 'height', '300')
# Config.set('graphics', 'resizable', False)


def valid_name(name):

    '''Ensures that the Name:
- is between 5 and 50 characters long,
- is uniquely alphabetic,
- contains no spaces,
- has the first letter in uppercase,
- has no more than 2 consecutive duplicates.'''

    name = name.strip()
    return (
        4 <= len(name) <= 50 and
        name.isalpha() and
        not name.isspace() and
        name[0].isupper() and
        not consecutive_duplicates(name)
        )


def consecutive_duplicates(duplicate):

    '''This function makes sure there is no more
    than 2 duplicate cosecutive letters in Name'''

    return bool(re.search(r'(.)\1{3,}', duplicate))


def valid_origin(origin):

    '''This function mas sure that country 
    is numeric and no more than 20 caracters'''

    return origin.isalpha() and len(origin) <= 20


def check_guests_registration():

    '''Conecting with DB'''

    conn = sqlite3.connect('Christmas_Table.db')

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM guests')

        rows = cursor.fetchall()

        # Verificar se há registros na tabela
        if not rows:
            print('Nobody at the Christmas Table!')
        else:
            print('These are the lucky guests on the Christmas Table:')
            for row in rows:
                print(row)

    except sqlite3.Error as e:
        print(f"Error acessing data base: {e}")

    finally:
        conn.close()


class MyApp(GridLayout):

    '''Class that defines the APP'''

    def __init__(self, **kwargs):
        super(MyApp, self).__init__()
        self.cols = 2
        self.spacing = [15, 15]

        self.add_widget(Label(text='Name'))
        self.st_name = TextInput(multiline=False,
                                 on_text_validate=self.validate_name)
        self.add_widget(self.st_name)

        self.add_widget(Label(text='Surname'))
        self.st_surname = TextInput(multiline=False,
                                    on_text_validate=self.validate_name)
        self.add_widget(self.st_surname)

        self.add_widget(Label(text='Gender'))
        self.st_gender = Spinner(text='Select',
                                 values=('Female', 'Male'))
        self.add_widget(self.st_gender)

        self.add_widget(Label(text='Age'))
        self.st_age = TextInput(multiline=False,
                                input_type='number',
                                on_text_validate=self.validate_numeric)
        self.add_widget(self.st_age)

        self.add_widget(Label(text='Where do you come from?'))
        self.st_country = TextInput(multiline=False,
                                    on_text_validate=self.validate_origin)
        self.add_widget(self.st_country)

        self.add_widget(Label(text='Something you would like to share'))
        self.st_thoughts = TextInput(multiline=True)
        self.add_widget(self.st_thoughts)

        self.add_widget(Label(text='How many Gifts do you bring?'))
        self.st_gifts = TextInput(multiline=False,
                                  input_type='number',
                                  on_text_validate=self.validate_numeric)
        self.add_widget(self.st_gifts)

        self.add_widget(Label(text='Did you behave this year?'))
        self.st_behave = Spinner(text='Select',
                                 values=('Off Course!', 'Maybe Not...'))
        self.add_widget(self.st_behave)

        self.press = Button(text='Save')
        self.press.bind(on_press=self.save)
        self.add_widget(self.press)

        # SQLite DB
        self.conn = sqlite3.connect('Christmas_Table.db')
        self.cursor = self.conn.cursor()

        # Table Creation
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS guests (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            surname NOT NULL,
                            gender TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            country TEXT NOT NULL,
                            thoughts TEXT NOT NULL,
                            gifts INTEGER NOT NULL,
                            behave TEXT NOT NULL
                            )
                        ''')
        self.conn.commit()

        self.error_displayed = False

    def validate_name(self, input_name):

        '''Name input Validation'''

        if not valid_name(input_name.text):
            self.st_name.text = ''
            self.st_surname.text = ''
            print('Invalid Entry!\nPlease enter a valid one!\n')

    def validate_numeric(self, input_number):

        '''Age and Numeber of Gifts Validation'''

        if not input_number.isnumeric():
            if not self.error_displayed:
                self.st_age.text = ''
                self.st_gifts.text = ''
                print('Invalid entry!\nPlease enter an integer value!\n')
                self.error_displayed = True
            return False

        number = int(input_number)
        if number < 0:
            if not self.error_displayed:
                print('You cannot input a negative number!\n')
                self.error_displayed = True
                return False

        return True

    def validate_origin(self, origin):

        '''Country input Validation'''

        if not valid_origin(origin.text):
            self.st_country.text = ''
            print('Please enter a Valid Region!\n')
        return False

    def save(self, instance):

        '''Function that saves the correct entries'''

        # Reset error_displayed for each new user
        self.error_displayed = False

        # Name is Valid
        person_name = self.st_name.text.strip()
        if not valid_name(self.st_name.text):
            self.st_name.text = ''
            print('Invalid Name!\nPlease enter a valid one!')
            return

        # Surname is Valid
        person_surname = self.st_surname.text.strip()
        if not valid_name(self.st_surname.text):
            self.st_surname.text = ''
            print('Invalid Surname!\nPlease enter a valid one!')
            return

        # Name and Surname are not equal
        if person_name.lower() == person_surname.lower():
            print('Name and Surname must be different!\n')
            return

        # Age and Gits are integers
        age_is_numeric = self.validate_numeric(self.st_age.text)
        if not age_is_numeric:
            print('Please enter a valid age, must be an integer!\n')
            return
        gifts_is_numeric = self.validate_numeric(self.st_gifts.text)
        if not gifts_is_numeric:
            print('Please enter a valid number of gifts, must be an integer!\n') # noqa E401
            return

        # Gender and Behaviour Buttons were used
        if self.st_gender.text == 'Select':
            print('Please enter your Gender!\n')
            return
        if self.st_behave.text == 'Select':
            print('Please enter if you behave this year!\n')
            return

        # Country is introduced
        if not self.st_country.text:
            print('Please enter your country of origin!\n')
            return

        # Thoughts were introduced
        if not self.st_thoughts.text:
            print('Please share something with the other guests!\n')
            return

        # Checking if the nº of gifts is enough
        if gifts_is_numeric and int(self.st_gifts.text) < 5:
            print("Is that all the magic you've got in your sleigh?\nLooks like someone might be on the 'Naughty List' for a gift shortage!\n")  # noqa E401
            return

        if valid_name(person_name) and valid_name(person_surname) and age_is_numeric and gifts_is_numeric:  # noqa E401
            print('Name ', self.st_name.text)
            print('Surname ', self.st_surname.text)
            print('Gender ', self.st_gender.text)
            print('Age ', self.st_age.text)
            print('Country ', self.st_country.text)
            print('Thoughts ', self.st_thoughts.text)
            print('Number of Gifts ', self.st_gifts.text)
            print('Good Behaviour ', self.st_behave.text)

            if self.st_behave.text == 'Maybe Not...':
                print("Looks like Santa has detected some questionable behavior on his radar!\nYour case is under review.\nHang tight and reconsider those life choices!\n")  # noqa E401
            else:
                print('Congratulations!\nYour seat at the Christmas Table is secured!\nGet ready to jingle all the way!!\n')  # noqa E401

        # Acess to DB
        self.cursor.execute('''
            INSERT INTO guests (
                name, surname, gender, age, country,
                thoughts, gifts, behave)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                            (person_name, person_surname, self.st_gender.text,
                                age_is_numeric, self.st_country.text,
                                self.st_thoughts.text, gifts_is_numeric,
                                self.st_behave.text))

        self.conn.commit()

        # To Check guests register
        check_guests_registration()

    def stop(self):

        '''Stops the connection with de DB'''

        self.conn.close()


class ParentApp(App):

    '''Parent App that makes the original App run'''

    def build(self):
        return MyApp()


if __name__ == '__main__':
    ParentApp().run()
