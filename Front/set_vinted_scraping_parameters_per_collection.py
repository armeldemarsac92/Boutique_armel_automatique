import streamlit as st
import json

# Load the collections from the JSON file
with open("../Assets/Data/item_quantites_per_cat_and_size_summed_up.json", "r") as collections_file:
    collections = json.load(collections_file)

# Load catalogs from the JSON files
with open("../Assets/Catalogs/brand_catalog.json", "r") as brand_catalog:
    brand_dict = json.load(brand_catalog)

with open("../Assets/Catalogs/category_catalog.json", "r") as category_catalog:
    category_dict = json.load(category_catalog)

with open("../Assets/Catalogs/color_catalog.json", "r") as color_catalog:
    color_dict = json.load(color_catalog)

def save_query_urls_to_json(file_name, data, urls):
    with open(file_name, "w") as file:
        json.dump({"data": data, "urls": urls}, file)

# Read the existing query URLs and parameters from the JSON file
query_urls_file = "../Assets/Data/query_urls.json"
try:
    with open(query_urls_file, "r") as file:
        data = json.load(file)
        query_urls = data.get("data", {})
        query_urls_only = data.get("urls", {})
except FileNotFoundError:
    query_urls = {}
    query_urls_only = {}

# Create a dropdown menu to select a collection
selected_collection = st.selectbox("Select a collection", list(collections.keys()))

# Get the current query parameters for the selected collection
current_parameters = query_urls.get(selected_collection, {})

# Set the default values for the input widgets based on the current parameters
default_query = current_parameters.get("query", "")
default_brand = [brand for brand in brand_dict.keys() if brand_dict[brand] in current_parameters.get("brand_ids", [])]
default_category = [category for category in category_dict.keys() if category_dict[category] in current_parameters.get("category_ids", [])]
default_colors = [color for color in color_dict.keys() if color_dict[color]["id"] in current_parameters.get("color_ids", [])]
default_desired_number_of_items = current_parameters.get("desired_number_of_items", 0)

# Create input widgets for query parameters
query = st.text_input("Quel vêtement cherchez-vous ?", value=default_query)
selected_brand = st.multiselect("Quelles marque(s)", list(brand_dict.keys()), default=default_brand)
selected_category = st.multiselect("Quelle catégorie (une seule)", list(category_dict.keys()), default=default_category)
selected_colors = st.multiselect("Sélectionnez une ou plusieurs couleurs", list(color_dict.keys()), default=default_colors)
desired_number_of_items = st.number_input("Desired number of items", min_value=0, value=default_desired_number_of_items, step=1)

if st.button("Save Query Parameters"):
    # Create query parameters
    brand_ids = [brand_dict[brand] for brand in selected_brand]
    category_ids = [category_dict[category] for category in selected_category]
    color_ids = [color_dict[color]["id"] for color in selected_colors]

    # Store the query parameters for the selected collection
    query_urls[selected_collection] = {
        "query": query,
        "brand_ids": brand_ids,
        "category_ids": category_ids,
        "color_ids": color_ids,
        "desired_number_of_items": desired_number_of_items,
    }

    # Create the query URL
    base_url = "https://www.vinted.fr/catalog?{}{}{}{}"
    query_str = "search_text={}".format(query)
    color_ids_str = "".join([f"&color_ids[]={color_id}" for color_id in color_ids])
    category_ids_str = f"&catalog[]={','.join(map(str, category_ids))}"
    brand_ids_str = "".join([f"&brand_id[]={brand_id}" for brand_id in brand_ids])
    site = base_url.format(query_str, color_ids_str, category_ids_str, brand_ids_str)

    # Save the query URLs and parameters to the JSON file
    save_query_urls_to_json(query_urls_file, query_urls, {selected_collection: site})

    st.success(f"Query parameters and URL saved for the {selected_collection} collection.")

# Show the current query URL for the selected collection
if selected_collection in query_urls_only:
    site = query_urls_only[selected_collection]
    st.write(f"Query URL for {selected_collection}:")
    st.write(site)

    # Show the desired number of items for the selected collection
    desired_items = query_urls[selected_collection].get("desired_number_of_items", 0)
    st.write(f"Desired number of items for {selected_collection}: {desired_items}")
