from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import ListProperty

import sqlite3
import re
from datetime import date
import time
import sys
import shutil

# Set window size (half of Samsung S5 screen res).
Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')
Config.write()

# Related to sqlite database.
file = "grocery_list.sqlite"
file_bk = "grocery_list_bk.sqlite"
conn = sqlite3.connect(file)
c = conn.cursor()
grocery_row = "!Grocery!"

# Name of kv file containing layout info.
Builder.load_file('main.kv')

# Misc. global variables.
start_time = elapsed_time = 0
my_list = []
day = dish = ""
days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
max_input_char = 20


class MyLayout(FloatLayout):

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.short_click_time = 1
        self.elapsed_time = 0
        self.grocery_list = ""
        self.saved_list = ""
        self.saved_menu_sun = ""
        self.saved_menu_mon = ""
        self.saved_menu_tue = ""
        self.saved_menu_wed = ""
        self.saved_menu_thu = ""
        self.saved_menu_fri = ""
        self.saved_menu_sat = ""
        self.text_input_1 = ""
        self.text_input_2 = ""
        self.msg_text = ""
        self.input_string = ""
        self.skip = False
        self.row, self.msg = build_dropdown()

    @staticmethod
    # Start time when spinner item is pressed.
    def start_clock():
        global start_time
        start_time = time.time()

    # End time when spinner item is released to give elapsed time.
    # Can then be used to trigger other events but not currently used.
    def stop_clock(self):
        global start_time
        self.elapsed_time = time.time() - start_time

    # Select (indicated by "*") or de-select spinner item  in global "my_list".
    def select_spinner(self, item):
        global my_list, dish
        self.msg = ""

        i = item.rstrip("*")
        if i in my_list:
            my_list.remove(i)
        else:
            my_list.append(i)
        dish = item

    # Add or update dish and ingredients in database.
    def add_update_dish(self, text1, text2):
        self.msg = ""

        if text1 == "" or text2 == "":
            self.msg = "Please enter both values."
            return

        today = str(date.today())

        sql_cmd = "REPLACE into grocery_list values('" +\
                  text1 + \
                  "', '" +\
                  text2 +\
                  "', '" +\
                  today + \
                  "')"

        try:
            c.execute(sql_cmd)
            conn.commit()
            self.msg = "Item created/updated."

        except Exception as e:
            self.msg = str(e)

    # Load shopping cart with list of ingredients into "self.grocery_list".
    def load_cart(self):
        self.msg = ""
        my_glist = ""

        for x in my_list:
            sql_cmd = "SELECT ingredients from  grocery_list WHERE dish = '" + x + "'"

            try:
                ingredients_list = c.execute(sql_cmd).fetchall()

            except Exception as e:
                self.msg_text = str(e)
                return

            my_ingredients = parse_string(str(ingredients_list))
            glist = ""
            for i in range(0, len(my_ingredients)):
                if i < len(my_ingredients) - 1:
                    glist += my_ingredients[i] + "\n"
                else:
                    glist += my_ingredients[i]
            my_glist += glist + "\n"
            self.grocery_list = str(my_glist).rstrip("\n")

    # Empty the shopping cart in "self.grocery_list" to start over.
    # Note does not commit changes until user saves.
    def empty_cart(self):
        self.grocery_list = self.saved_list = ""
        self.msg = "Press Save or back to cancel."

    # Delete dish(es) selected in global "my_list".
    def delete_dish(self):
        global my_list
        self.msg = ""

        if not my_list:
            self.msg = "Must select item(s) first."
            return

        for i in my_list:
            sql_cmd = "DELETE FROM grocery_list WHERE dish = '" + i + "'"

            try:
                c.execute(sql_cmd)
                conn.commit()
                self.msg = "Item(s) deleted."

            except Exception as e:
                self.msg = str(e)
                return

        my_list = []

    # Build grocery list "self.saved_list" from "!Grocery! row in the database.
    def build_saved_items(self):
        self.msg_text = self.saved_list = ""

        sql_cmd = "SELECT ingredients FROM grocery_list WHERE dish = '" +\
                  grocery_row +\
                  "'"

        try:
            ingredients_list = c.execute(sql_cmd).fetchall()

        except Exception as e:
            self.msg_text = str(e)
            return

        my_ingredients = parse_string(str(ingredients_list))
        my_ing = ""
        for i in range(0, len(my_ingredients)):
            if i < len(my_ingredients) - 1:
                my_ing += my_ingredients[i] + "\n"
            else:
                my_ing += my_ingredients[i]

        self.saved_list = str(dedupe_string(str(my_ing), self.grocery_list))

    # Save the grocery list from text input to "!Grocery!" row in the database.
    def save_items(self, string):
        global my_list
        self.msg_text = self.saved_list = ""

        today = str(date.today())
        sql_cmd = "REPLACE into grocery_list values('" +\
                  grocery_row +\
                  "', '" +\
                  string + \
                  "', '" + \
                  today + \
                  "')"

        try:
            c.execute(sql_cmd)
            conn.commit()
            self.msg = "Saved to shopping cart."

        except Exception as e:
            self.msg_text = str(e)
            return

        my_ingredients = parse_string(str(string))
        my_ing = ""
        for i in range(0, len(my_ingredients)):
            if i < len(my_ingredients) - 1:
                my_ing += my_ingredients[i] + "\n"
            else:
                my_ing += my_ingredients[i]
        self.saved_list = str(my_ing).rstrip("\n")

        self.grocery_list = ""
        my_list = []

    # Save selected day / dish into the database. Rows are "!Sun!", "!Mon!", etc.
    def save_menu(self):
        global day, dish
        self.skip = False

        if day in ("All", ""):
            self.msg = "Select a valid day."
            self.skip = True
            return

        day_row = "!" + day + "!"
        try:
            today = str(date.today())
            sql_cmd = "REPLACE into grocery_list values('" + \
                      day_row + "', '" +\
                      dish + "', '" +\
                      today + \
                      "')"

            c.execute(sql_cmd)
            conn.commit()

        except Exception as e:
            self.msg = str(e)
            return

    # Clear the dish for the selected day - note "..." will appear instead.
    def clear_menu(self):
        global day
        self.msg = ""

        if day == "":
            self.msg = "Must select day to clear."
            return

        today = str(date.today())
        for d in days_of_week:
            if d != day:
                continue

            day_row = "!" + d + "!"
            sql_cmd = "REPLACE into grocery_list values('" + \
                      day_row + "', ' ', '" +\
                      today + \
                      "')"

            try:
                c.execute(sql_cmd)
                conn.commit()

            except Exception as e:
                self.msg = str(e)
                return

    # Build list of dishes for the week.
    def get_saved_menu(self):

        for d in days_of_week:
            day_row = "!" + d + "!"
            sql_cmd = "SELECT ingredients FROM grocery_list WHERE dish = '" + \
                      day_row + \
                      "'"

            try:
                dishes_list = c.execute(sql_cmd).fetchall()

            except Exception as e:
                self.msg = str(e)
                return

            s = str(parse_string(str(dishes_list)))
            if s == "[]":
                s = "..."

            my_dish = s\
                .replace("'", "") \
                .replace("[", "")\
                .replace("]", "")

            if d == "Sun":
                self.saved_menu_sun = my_dish
            elif d == "Mon":
                self.saved_menu_mon = my_dish
            elif d == "Tue":
                self.saved_menu_tue = my_dish
            elif d == "Wed":
                self.saved_menu_wed = my_dish
            elif d == "Thu":
                self.saved_menu_thu = my_dish
            elif d == "Fri":
                self.saved_menu_fri = my_dish
            elif d == "Sat":
                self.saved_menu_sat = my_dish

    # Save selected day in global "day".
    @staticmethod
    def select_day(d):
        global day
        day = d

    # Clear the text input boxes, message line and other global variables when requested.
    def clear_text_input(self):
        global my_list, day
        self.text_input_1 = ""
        self.text_input_2 = ""
        self.msg = ""
        self.grocery_list = ""
        my_list = []
        day = ""

    # Read database for selected dish and display details.
    def search_dish_details(self):
        if not my_list:
            self.msg = "Must select search item first."
            return

        if len(my_list) > 1:
            self.msg = "Select only one item to search."
            return

        text = my_list[0]

        sql_cmd = "SELECT dish, ingredients from grocery_list where dish = '" + text + "'"

        try:
            r = c.execute(sql_cmd).fetchall()
            first = True
            for i in r:
                for j in i:
                    if first:
                        self.text_input_1 = j
                        first = False
                    else:
                        self.text_input_2 = j

        except Exception as e:
            self.msg = str(e)
            return

    # Restore previously saved backup database file ("grocery_list_bk.sqlite" to "grocery_list.sqlite").
    def restore_data(self):
        try:
            copy_file(file_bk, file)
            self.msg = "Backup file restored."
        except Exception as e:
            if "No such file or directory" in str(e):
                self.msg = "No backup file found."
            else:
                self.msg = str(e)

    # Backup current database file ("grocery_list.sqlite" to "grocery_list_bk.sqlite").
    def backup_data(self):
        try:
            copy_file(file, file_bk)
            self.msg = "Backup file created."
        except Exception as e:
            self.msg = str(e)

    # Refresh spinner items, typically after a change has been made.
    def refresh_spinner(self):
        self.msg = ""
        self.row, self.msg = build_dropdown()

    # Count no. of characters entered in text input box to impose an upper limit.
    # Used for dish name that otherwise may mess up the display.
    def count_input_char(self, string):
        if len(string) > max_input_char:
            self.input_string = string[:max_input_char]
        else:
            self.input_string = string

    # Exit app.
    @staticmethod
    def exit_app():
        close_file_and_quit()


# Build spinner items with dishes in the database.
def build_dropdown():
    row = {}
    msg = ""

    sql_cmd = "SELECT dish FROM grocery_list WHERE NOT dish LIKE '!%!'"

    try:
        grocery_list = c.execute(sql_cmd).fetchall()
        a_list = parse_string(str(grocery_list))
        row = ListProperty()
        row = [str(i) for i in a_list]

        for i, j in enumerate(row):
            if j in my_list:
                row[i] = j + "*"

    except Exception as e:
        msg = str(e)

    return row, msg


# Takes a string and returns a list after stripping away unwanted characters.
# Used to clean up data before presenting it on screen.
def parse_string(string):
    string_strip = string \
        .replace("\\n", ", ") \
        .replace("[", "")\
        .replace("',), ('", ", ")\
        .replace("',)", "")\
        .replace(" ('", "")\
        .replace("('", "")\
        .replace("]", "")

    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    a_list = ([i for i in pattern.split(string_strip) if i])
    return a_list


# Combine 2 lists and remove duplicates.
# Used to combine grocery lists that contain common ingredients.
def dedupe_string(text1, text2):
    list1 = parse_string(text1)
    list2 = parse_string(text2)

    list1a = parse_string(str(list1).replace("'", ""))
    list2a = parse_string(str(list2).replace("'", ""))

    list_out = list2a
    for i in list1a:
        if i not in list2a:
            list_out.append(i)

    return str(list_out)\
        .replace("[", "")\
        .replace("]", "")\
        .replace("'", "")\
        .replace(", ", "\n")


# Copy files function used to backup and restore database file.
def copy_file(file1, file2):
    shutil.copy2(file1, file2)


class MyApp(App):
    title = 'Mai Sung'

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.msg = ""
        self.row = ""
        self.grocery_list = []

    def build(self):

        sql_cmd = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='grocery_list'"
        c.execute(sql_cmd)

        if c.fetchone()[0] == 1:   # Test to see if table already exists, otherwise create it.
            pass
        else:
            self.create_table()

        self.row, self.msg = build_dropdown()

        return MyLayout()

    def create_table(self):
        try:
            sql_cmd = "CREATE TABLE grocery_list(" + \
                      "dish adLongVarWChar NOT NULL, " + \
                      "ingredients adLongVarWChar NOT NULL, " + \
                      "last_date DATE, " + \
                      "PRIMARY KEY (dish))"

            c.execute(sql_cmd)
            conn.commit()
            self.msg = "Database table created."

        except Exception as e:
            self.msg = str(e)
            return

        try:
            today = str(date.today())
            sql_cmd = "REPLACE into grocery_list values('" + \
                      grocery_row + \
                      "', '" + \
                      today + \
                      "')"

            c.execute(sql_cmd)
            conn.commit()
            self.msg = "Database table 'grocery_list' created."

        except Exception as e:
            self.msg = str(e)
            return


# Close database file and exit app.
# Currently works in windows but crashes in android!
def close_file_and_quit():
    conn.close()
    sys.exit()


if __name__ == "__main__":
    MyApp().run()
