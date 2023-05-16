def app2():
    import pandas as pd
    import streamlit as st
    import json
    import csv

    # Load the existing data
    df = pd.read_csv('../Assets/Data/item_quantities_per_tags_and_collections.csv')

    # Load catalogs from the JSON files
    with open("../Assets/Catalogs/brand_catalog.json", "r") as brand_catalog:
        brand_dict = json.load(brand_catalog)

    with open("../Assets/Catalogs/category_catalog.json", "r") as category_catalog:
        category_dict = json.load(category_catalog)

    with open("../Assets/Catalogs/color_catalog.json", "r") as color_catalog:
        color_dict = json.load(color_catalog)

    # Read the existing query URLs and parameters from the DataFrame
    query_urls = {}
    if 'query' in df.columns:
        for _, row in df.iterrows():
            collection = row['Title']
            parameters = {
                'query': row['query'],
                'brand_ids': row['brand_ids'],
                'category_ids': row['category_ids'],
                'color_ids': row['color_ids'],
                'desired_number_of_items': row['desired_number_of_items'],
                'url': row['url']
            }
            query_urls[collection] = parameters

    # Create a dropdown menu to select a collection
    selected_collection = st.selectbox("Select a collection", df['Title'].tolist())

    # Get the current query parameters for the selected collection
    current_parameters = query_urls.get(selected_collection, {})

    # Get the current query parameters for the selected collection
    current_parameters = query_urls.get(selected_collection, {})

    # Set the default values for the input widgets based on the current parameters
    try:
        default_query = current_parameters.get("query", " ")
        default_brand = [brand for brand, brand_id in brand_dict.items() if
                         str(brand_id) in current_parameters.get("brand_ids", [])]
        default_category = [category for category, category_id in category_dict.items() if
                            str(category_id) in current_parameters.get("category_ids", [])]
        default_colors = [color for color, color_dict_item in color_dict.items() if
                          str(color_dict_item["id"]) in current_parameters.get("color_ids", [])]
        default_desired_number_of_items = current_parameters.get("desired_number_of_items", 0)
    except:
        default_query = ""
        default_brand = []
        default_category = []
        default_colors = []
        default_desired_number_of_items = 0

    # Create input widgets for query parameters
    query = st.text_input("Quel vêtement cherchez-vous ?", value=default_query)
    selected_brand = st.multiselect("Quelles marque(s)", list(brand_dict.keys()), default=default_brand)
    selected_category = st.multiselect("Quelle catégorie (une seule)", list(category_dict.keys()),
                                       default=default_category)
    selected_colors = st.multiselect("Sélectionnez une ou plusieurs couleurs", list(color_dict.keys()),
                                     default=default_colors)
    desired_number_of_items = st.number_input("Desired number of items", min_value=0,
                                              value=int(default_desired_number_of_items), step=1)

    # ...
    # ...

    if st.button("Sauvegarder les paramètres de recherche"):
        # Create query parameters
        brand_ids = [brand_dict[brand] for brand in selected_brand]
        category_ids = [category_dict[category] for category in selected_category]
        color_ids = [color_dict[color]["id"] for color in selected_colors]
        # Create the query URL
        base_url = "https://www.vinted.fr/catalog?{}{}{}"
        query_str = "search_text={}".format(query)
        color_ids_str = "".join([f"&color_ids[]={color_id}" for color_id in color_ids])
        category_ids_str = f"&catalog[]={','.join(map(str, category_ids))}"
        site = base_url.format(query_str, color_ids_str, category_ids_str)

        # Store the query parameters for the selected collection
        query_urls[selected_collection] = {
            "query": query,
            "brand_ids": brand_ids,
            "category_ids": category_ids,
            "color_ids": color_ids,
            "desired_number_of_items": desired_number_of_items,
            "url": site
        }

        # Update the dataframe
        df.loc[df['Title'] == selected_collection, 'query'] = query
        df.loc[df['Title'] == selected_collection, 'brand_ids'] = str(brand_ids)
        df.loc[df['Title'] == selected_collection, 'category_ids'] = str(category_ids)
        df.loc[df['Title'] == selected_collection, 'color_ids'] = str(color_ids)
        df.loc[df['Title'] == selected_collection, 'desired_number_of_items'] = desired_number_of_items
        df.loc[df['Title'] == selected_collection, 'url'] = site

        # Save the updated dataframe back to the CSV file
        df.to_csv('../Assets/Data/item_quantities_per_tags_and_collections.csv', index=False)

        st.success(f"Query parameters and URL saved for the {selected_collection} collection.")

    if selected_collection in query_urls:
        site = query_urls[selected_collection].get('url', '')
        st.write(f"Query URL for {selected_collection}:")
        st.write(site)
        # Show the desired number of items for the selected collection
        desired_items = query_urls[selected_collection].get("desired_number_of_items", 0)
        st.write(f"Desired number of items for {selected_collection}: {desired_items}")
