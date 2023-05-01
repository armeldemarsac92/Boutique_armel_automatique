import streamlit as st
import subprocess
import time
import json

with open ("Assets/Catalogs/size_catalog.json", "r") as size_catalog:
    size_dict=json.load(size_catalog)

with open ("Assets/Catalogs/brand_catalog.json", "r") as brand_catalog:
    brand_dict=json.load(brand_catalog)

with open ("Assets/Catalogs/category_catalog.json", "r") as category_catalog:
    category_dict=json.load(category_catalog)

with open ("Assets/Catalogs/color_catalog.json", "r") as color_catalog:
    color_dict=json.load(color_catalog)

# Create an empty placeholder element for the progress bar
progress_placeholder = st.empty()

# Create an empty placeholder element for the status message
status_placeholder = st.empty()

query = st.text_input("Quel vêtement cherchez-vous ?")
selected_brand = st.multiselect("Quelles marque(s)", list(brand_dict.keys()))
selected_category = st.multiselect("Quelle catégorie (une seule)", list(category_dict.keys()))
pieces_a_chercher = st.number_input("Combien de pièces souhaitez-vous ?", min_value=1, step=1)
selected_sizes = st.multiselect("Sélectionnez une ou plusieurs tailles", list(size_dict.keys()))
selected_colors = st.multiselect("Sélectionnez une ou plusieurs couleurs", list(color_dict.keys()))

if st.button("Lancer la recherche"):
    if query and pieces_a_chercher and selected_category:
        brand_ids = [brand_dict[brand] for brand in selected_brand]
        category_ids = [category_dict[category] for category in selected_category]
        size_ids = [size_dict[size] for size in selected_sizes]
        color_ids = [colors_dict[color]["id"] for color in selected_colors]
        # Appel de la fonction de scrapping avec les paramètres

        base_url = "https://www.vinted.fr/catalog?{}{}{}{}{}"

        #https://www.vinted.fr/catalog?catalog[]=266&size_id[]=206&size_id[]=207&size_id[]=208&brand_id[]=12&brand_id[]=14&search_text=pull&color_ids[]=3&color_ids[]=20

        query = "search_text={}".format(query)

        if color_ids !="":
            parameters1=[]
            for color_id in color_ids:
                parameter1 = "&color_ids[]={}".format(color_id)
                parameters1.append(parameter1)
            parameters1="".join(parameters1)


        parameter2 ="&catalog[]={}".format(str(category_ids).replace("[","").replace("]",""))

        if brand_ids !="":
            parameters3=[]
            for brand_id in brand_ids:
                parameter3 = "&brand_id[]={}".format(brand_id)
                parameters3.append(parameter3)
            parameters3="".join(parameters3)

        parameters4 =[]
        for size_id in size_ids:
            parameter4 = "&size_id[]={}".format(size_id)
            parameters4.append(parameter4)
        parameters4="".join(parameters4)

        site = base_url.format(query,parameters1,parameter2,parameters3,parameters4)

        cmd = ['python', 'vinted_scraping_script.py', site, str(pieces_a_chercher), str(query)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while process.poll() is None:
            # Read the progress from the file "progress_bar_data.txt"
            with open("Assets/Data/progress_bar_data.txt", "r") as f:
                progress = float(f.read().strip())
                normalized_progress = progress / 100

                # Update the progress bar
                my_bar = progress_placeholder.progress(normalized_progress)

                # Sleep for a short duration to avoid excessive updates
                time.sleep(0.1)

        # The script_b.py execution has completed
        status_placeholder.success("Script B has finished.")

        # Trigger a rerun of the script to update the progress bar and clear the status message
        #st.experimental_rerun()
    else:
        st.warning("Veuillez remplir tous les champs.")
