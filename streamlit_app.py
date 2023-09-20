import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


# import streamlit ############################################################################################################################
streamlit.title('My Parents Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣    Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗    Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔    Hard-Boiled Free-Ranged Egg')
streamlit.text('🥑🍞  Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



# import pandas ############################################################################################################################
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# create function
def get_fruityvice_data(this_fruit_choice):
    # import requests ############################################################################################################################
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
    else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()



# import snowflake.connector ############################################################################################################################
streamlit.header("The fruit load list contains:")
# snowflake retaled function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# add a button to load friut
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


# allow the end user to add fruit to the list
def inster_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Insert into fruit_load_list values ('" + add_my_fruit + "')")
        return "Thanks for adding " + new_fruit       

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = inster_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)






# stops running codes unit here
streamlit.stop()






