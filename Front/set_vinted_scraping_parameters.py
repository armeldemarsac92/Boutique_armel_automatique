
def app1():
    import streamlit as st
    import subprocess
    import time
    import json
    import csv
    import random
    session_token = random.randint(0,10000)

    with open("../Assets/Catalogs/size_catalog.json", "r") as size_catalog:
        size_dict=json.load(size_catalog)

    with open("../Assets/Catalogs/brand_catalog.json", "r") as brand_catalog:
        brand_dict=json.load(brand_catalog)

    with open("../Assets/Catalogs/category_catalog.json", "r") as category_catalog:
        category_dict=json.load(category_catalog)

    with open("../Assets/Catalogs/color_catalog.json", "r") as color_catalog:
        color_dict = json.load(color_catalog)

    # Initialize an empty dictionary to store your data
    collection_dict = {}

    # Open your CSV file
    with open('../Assets/Data/item_quantities_per_tags_and_collections.csv', 'r', encoding='utf-8') as f:
        # Use the csv library to read the file
        reader = csv.DictReader(f)

        # Loop through each row in the file
        for row in reader:
            # Extract the title
            title = row["Title"]
            id = row["ID"]

            # Add the new dictionary to the item quantities dictionary
            collection_dict[title] = id

    query = st.text_input("Quel vêtement cherchez-vous ?")
    selected_brand = st.multiselect("Quelles marque(s)", list(brand_dict.keys()))
    selected_category = st.multiselect("Quelle catégorie (une seule)", list(category_dict.keys()))
    pieces_a_chercher = st.number_input("Combien de pièces souhaitez-vous ?", min_value=1, step=1)
    selected_sizes = st.multiselect("Sélectionnez une ou plusieurs tailles", list(size_dict.keys()))
    selected_colors = st.multiselect("Sélectionnez une ou plusieurs couleurs", list(color_dict.keys()))
    selected_collection = st.selectbox("Dans quelle catégorie iront les produits ?",list(collection_dict.keys()))

    # Create an empty placeholder element for the progress bar
    progress_placeholder = st.empty()

    # Create an empty placeholder element for the status message
    status_placeholder = st.empty()

    if st.button("Lancer la recherche"):
        if query and pieces_a_chercher and selected_category:
            brand_ids = [brand_dict[brand] for brand in selected_brand]
            category_ids = [category_dict[category] for category in selected_category]
            size_ids = [size_dict[size] for size in selected_sizes]
            color_ids = [color_dict[color]["id"] for color in selected_colors]
            collection = collection_dict[selected_collection]

            base_url = "https://www.vinted.fr/catalog?{}{}{}{}{}"

            query = "search_text={}".format(query)

            parameters1 = ""
            if color_ids:
                parameters1 = "".join([f"&color_ids[]={color_id}" for color_id in color_ids])

            parameter2 = f"&catalog[]={','.join(map(str, category_ids))}"

            parameters3 = ""
            if brand_ids:
                parameters3 = "".join([f"&brand_id[]={brand_id}" for brand_id in brand_ids])

            parameters4 = "".join([f"&size_id[]={size_id}" for size_id in size_ids])

            site = base_url.format(query, parameters1, parameter2, parameters3, parameters4)

            try:
                cmd = ['python', '../Utilitaries/vinted_scraping_script.py', site, str(pieces_a_chercher), str(query),
                       str(session_token), str(selected_collection), str(collection)]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                st.error(f"An error occurred while running the script: {str(e)}")

            while process.poll() is None:
                with open("../Assets/Data/progress_bar_data.txt", "r") as f:
                    progress = float(f.read().strip())
                    normalized_progress = progress / 100
                    progress_placeholder.progress(normalized_progress)
                    time.sleep(1)

            status_placeholder.success("Script B has finished.")
            st.balloons()

            stdout, stderr = process.communicate()
            if stderr:
                st.error(f"An error occurred during the subprocess:\n{stderr}")
            else:
                st.success(f"Subprocess completed successfully. Output:\n{stdout}")





