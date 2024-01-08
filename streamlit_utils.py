import json

import requests
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st

api_url = st.secrets["API_BASE_URL"]

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # modify = st.checkbox("Add filters")
    #
    # if not modify:
    #     return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter data on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[column], pd.CategoricalDtype) or df[column].nunique() < 4:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    #default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


search_page_columns = [
  {
    "headerName": "PRODUCT NAME",
    "field": "product_name",
    "pinned": "left"
  },
  {
    "headerName": "CUSTOMER RATING (1-5)",
    "field": "customer_rating"
  },
  {
    "headerName": "DESCRIPTION",
    "field": "description"
  },
  {
    "headerName": "INGREDIENTS",
    "field": "ingredients"
  },
  {
    "headerName": "NUTRIENT (OF WHICH SATURATES) (g)",
    "field": "nutrient_(of_which_saturates)"
  },
  {
    "headerName": "NUTRIENT (OF WHICH SUGARS) (g)",
    "field": "nutrient_(of_which_sugars)"
  },
  {
    "headerName": "NUTRIENT - B12",
    "field": "nutrient_-_b12"
  },
  {
    "headerName": "NUTRIENT - CALCIUM",
    "field": "nutrient_-_calcium"
  },
  {
    "headerName": "NUTRIENT - D2",
    "field": "nutrient_-_d2"
  },
  {
    "headerName": "NUTRIENT - IODINE",
    "field": "nutrient_-_iodine"
  },
  {
    "headerName": "NUTRIENT - RIBOFLAVIN (B2) (mg)",
    "field": "nutrient_-_riboflavin_(b2)"
  },
  {
    "headerName": "NUTRIENT B12 (µg)",
    "field": "nutrient_b12"
  },
  {
    "headerName": "NUTRIENT CALCIUM (mg)",
    "field": "nutrient_calcium"
  },
  {
    "headerName": "NUTRIENT CARBOHYDRATE (g)",
    "field": "nutrient_carbohydrate"
  },
  {
    "headerName": "NUTRIENT CARBOHYDRATE (g)",
    "field": "nutrient_carbohydrate:"
  },
  {
    "headerName": "NUTRIENT D2 (µg)",
    "field": "nutrient_d2"
  },
  {
    "headerName": "NUTRIENT E (mg)",
    "field": "nutrient_e"
  },
  {
    "headerName": "NUTRIENT ENERGY (kcal)",
    "field": "nutrient_energy"
  },
  {
    "headerName": "NUTRIENT ENERGY:",
    "field": "nutrient_energy:"
  },
  {
    "headerName": "NUTRIENT FAT (g)",
    "field": "nutrient_fat"
  },
  {
    "headerName": "NUTRIENT FAT (g)",
    "field": "nutrient_fat:"
  },
  {
    "headerName": "NUTRIENT FIBRE (g)",
    "field": "nutrient_fibre"
  },
  {
    "headerName": "NUTRIENT IODINE (µg)",
    "field": "nutrient_iodine"
  },
  {
    "headerName": "NUTRIENT OF WHICH SATURATES (g)",
    "field": "nutrient_of_which_saturates"
  },
  {
    "headerName": "NUTRIENT OF WHICH SATURATES (g)",
    "field": "nutrient_of_which_saturates:"
  },
  {
    "headerName": "NUTRIENT OF WHICH SUGARS (g)",
    "field": "nutrient_of_which_sugars"
  },
  {
    "headerName": "NUTRIENT OF WHICH SUGARS (g)",
    "field": "nutrient_of_which_sugars:"
  },
  {
    "headerName": "NUTRIENT PROTEIN (g)",
    "field": "nutrient_protein"
  },
  {
    "headerName": "NUTRIENT PROTEIN (g)",
    "field": "nutrient_protein:"
  },
  {
    "headerName": "NUTRIENT RIBOFLAVIN (B2) (mg)",
    "field": "nutrient_riboflavin_(b2)"
  },
  {
    "headerName": "NUTRIENT SALT (g)",
    "field": "nutrient_salt"
  },
  {
    "headerName": "NUTRIENT SALT: (g)",
    "field": "nutrient_salt:"
  },
  {
    "headerName": "NUTRIENT VITAMIN B12 (µg)",
    "field": "nutrient_vitamin_b12"
  },
  {
    "headerName": "NUTRIENT VITAMIN D (µg)",
    "field": "nutrient_vitamin_d"
  },
  {
    "headerName": "PRICE RAW UOM",
    "field": "price_raw_uom"
  },
  {
    "headerName": "PRICE RAW WEIGHT",
    "field": "price_raw_weight"
  },
  {
    "headerName": "PRICE SELLING PRICE",
    "field": "price_selling_price"
  },
  {
    "headerName": "PRODUCT ID",
    "field": "product_id"
  },
  {
    "headerName": "PRODUCT TYPE",
    "field": "product_type"
  },
  {
    "headerName": "PRODUCT URL",
    "field": "product_url"
  },
  {
    "headerName": "SOURCE",
    "field": "source"
  }
]
def find_key_by_value(dictionary: dict, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def send_search_request(q: str, filter_: dict):
    req_body = {"q": q, "filter": filter_}

    if len(q) > 0:
        all_products = requests.post(
            api_url + "/search",
            json=req_body
            )
        products = all_products.json()

        st.session_state.search_results = products
    else:
        st.error("Please enter a query")