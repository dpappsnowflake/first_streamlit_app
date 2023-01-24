import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.title("My parents' new healthy diner")
streamlit.header("Breakfast menu")
streamlit.text("🥣    Omega 3 and blueberry oatmeal")
streamlit.text("🥗    Kale, spinach & rocket smoothie")
streamlit.text("🐔    Hard-boiled free-range egg")
streamlit.text("🥑🍞 Avocado toast")

########################################
# Build your own smoothie
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include
# First Set the index to be fruit names (don't want numbers on the table)
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) # Defaults

# Display the table on the page.
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

########################################
# Fruityvice integration
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(my_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + my_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information on')
  else:
    fruityvice_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_data)
except URLError as e:
  streamlit.error()


########################################
# Snowflake integration
streamlit.header("The fruit Load list contains:")

def get_fruit_load_list():
  with snowflake.connector.connect(**streamlit.secrets["snowflake"]) as cnx:
    my_cur = cnx.cursor()
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

# Button to show fruit load list
if streamlit.button('Get fruit load list'):
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
  with snowflake.connector.connect(**streamlit.secrets["snowflake"]) as cnx:
    my_cur = cnx.cursor()
    my_cur.execute(f"insert into FRUIT_LOAD_LIST values ({new_fruit})")
    return "Thanks for adding " + new_fruit

# Option to add fruit to list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit to list'):
  message = insert_row_snowflake(add_my_fruit)
  streamlit.text(message)



