import streamlit as st
from defines_sizes_quotas import app3
from set_vinted_scraping_parameters import app1
from set_vinted_scraping_parameters_per_collection import app2
from compare_quantities import app4
from review_app import app5
import pandas as pd
import numpy as np
import plotly.express as px

# Load your data, ensure the path is correct
df = pd.read_csv('../Assets/Data/item_data_scrapped_from_vinted.csv')

colors_list = df['item_color'].str.split(', ').explode().unique()

df['item_location_country'] = df['item_location'].str.split(',').str[-1]


# Convert 'item_price' to a string type
df['item_price'] = df['item_price'].astype(str)

# Replace '€' and ',' with respective characters
df['item_price'] = df['item_price'].str.replace('€', '').str.replace(',', '.')

# Handling non-numeric entries (if any)
df['item_price'] = pd.to_numeric(df['item_price'], errors='coerce')

# Handling NaN entries (if any)
df['item_price'] = df['item_price'].fillna(0)


def app6():
    # Filter Activation
    filters_active = {
        'brand': st.sidebar.checkbox("Activate Brand Filter", False),
        'color': st.sidebar.checkbox("Activate Color Filter", False),
        'location': st.sidebar.checkbox("Activate Location Filter", False),
        'status': st.sidebar.checkbox("Activate Status Filter", False)
    }

    filtered_df = df.copy()

    if filters_active['brand']:
        selected_brand = st.sidebar.multiselect('Brand', df['item_brand'].unique())
        filtered_df = filtered_df[filtered_df['item_brand'].isin(selected_brand)]

    if filters_active['color']:
        selected_color = st.sidebar.multiselect('Color', colors_list)
        filtered_df = filtered_df[filtered_df['item_color'].isin(selected_color)]

    if filters_active['location']:
        selected_location = st.sidebar.multiselect('Location', df['item_location_country'].unique())
        filtered_df = filtered_df[filtered_df['item_location_country'].isin(selected_location)]

    if filters_active['status']:
        selected_status = st.sidebar.multiselect('Status', df['status'].unique())
        filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]

    else:
        filtered_df = df

    # Plots
    st.sidebar.subheader('Data to display')
    data_to_show = st.sidebar.selectbox("Choose the data to display", ["Median", "Average", "Count"])

    if data_to_show == "Median":
        group_func = 'median'
    elif data_to_show == "Average":
        group_func = 'mean'
    elif data_to_show == "Count":
        group_func = 'count'

    # Item views
    st.subheader('Item views')
    fig1 = px.histogram(filtered_df, x='item_current_views')
    st.plotly_chart(fig1)

    # Item followers
    st.subheader('Item followers')
    fig2 = px.histogram(filtered_df, x='item_current_followers')
    st.plotly_chart(fig2)

    # Item price
    st.subheader('Item price')
    fig3 = px.histogram(filtered_df, x='item_price')
    st.plotly_chart(fig3)

    # Brand price
    st.subheader('Brand price')
    df_grouped = filtered_df.groupby('item_brand')['item_price'].agg(group_func).reset_index()
    fig4 = px.bar(df_grouped, x='item_brand', y='item_price')
    st.plotly_chart(fig4)

    # Size pie chart
    st.subheader('Available Sizes')
    fig5 = px.pie(filtered_df, names='item_size')
    st.plotly_chart(fig5)

    # Color pie chart
    st.subheader('Available Colors')
    fig6 = px.pie(filtered_df, names='item_color')
    st.plotly_chart(fig6)


if __name__ == "__main__":
    app6()
