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

streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit Load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
streamlit.write("Thanks for adding " + add_my_fruit)




