# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  


# App Title
st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Name Input
name_on_order = st.text_input('Name on Smoothie:')

st.write(
    'The name on your Smoothie will be:',
    name_on_order
)

# Snowflake Session
cnx = st.connection("snowflake")
session = cnx.session()

# Get Fruit Options
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

# Convert dataframe to list for multiselect
fruit_options = [
    row["FRUIT_NAME"]
    for row in my_dataframe.collect()
]

# Ingredient Selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options, max_selections=5
)

# Submit Section
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)
    st.subheader(fruit_chosen + 'Nutrition Information')
    
    smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen
    )

    sf_df = st.dataframe(
        data=smoothiefroot_response.json(),
        use_container_width=True
    )

    submit_order = st.button('Submit Order')

    if submit_order:

        my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (
            NAME_ON_ORDER,
            INGREDIENTS
        )
        VALUES
        (
            '{name_on_order}',
            '{ingredients_string}'
        )
        """

        session.sql(my_insert_stmt).collect()

        st.success(
            f'✅ Your Smoothie is ordered, {name_on_order}!'
        )



      
