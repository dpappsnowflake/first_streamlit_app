import streamlit
import pandas as pd
import requests

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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# Normalise json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Display fruityvice
streamlit.dataframe(fruityvice_normalized)










