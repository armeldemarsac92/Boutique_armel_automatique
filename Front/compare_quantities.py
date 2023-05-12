def app4():
    import json
    import csv
    import random
    import subprocess
    import streamlit as st
    import time
    with open ("../Assets/Catalogs/size_catalog.json", "r") as size_catalog:
        size_dict=json.load(size_catalog)

    st.title("Restockage de la boutique")

    #collects and prepares the collection data
    get_items = ("Python","../Utilitaries/get_collections_and_item_data_from_raindrop.py")
    subprocess.Popen(get_items, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # Create an empty placeholder element for the collection progress bar
    progress_placeholder_2 = st.empty()
    status_placeholder_2 = st.empty()
    st.divider()
    # Create an empty placeholder element for the size progress bar
    progress_placeholder = st.empty()

    # Create an empty placeholder element for the status message
    status_placeholder = st.empty()

    # Read and parse the three files
    with open('../Assets/Data/query_urls.json', 'r') as f2, open('../Assets/Data/size_quotas.json', 'r') as f3:
        desired_data = json.load(f2)
        size_quotas = json.load(f3)

    # Define the tags you're interested in
    tags_of_interest = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

    # Initialize an empty dictionary to store your data
    cloth_data = {}

    # Open your CSV file
    with open('../Assets/Data/item_quantities_per_tags_and_collections.csv', 'r', encoding='utf-8') as f:
        # Use the csv library to read the file
        reader = csv.DictReader(f)

        # Loop through each row in the file
        for row in reader:
            # Extract the title
            title = row["Title"]

            # Initialize a new dictionary to store the quantities of the tags of interest
            quantities = {}

            # Loop through the tags of interest
            for tag in tags_of_interest:
                # If the tag is in the row, add its quantity to the new dictionary
                if tag in row:
                    quantities[tag] = int(row[tag])

            # Add the new dictionary to the item quantities dictionary
            cloth_data[title] = quantities

    print(cloth_data)

    # Initialize a dictionary to store the results
    results = {}

    session_token = random.randint(0,10000)


    if st.button("lancer le restockage"):
        # Loop through each category in the desired data
        for category, category_data in desired_data['data'].items():
            # Initialize a dictionary to store the category results
            category_results = {}

            #initiate i to track the progress of the collection fetching
            i=0

            #defines the number of sizes to iterate through, used for the progress bar
            def count_tailles_inferieures(cloth_data, desired_data, size_quotas):
                tailles_inferieures = 0
                for size, quantity in cloth_data[category].items():
                    expected_quantity = int(category_data['desired_number_of_items'] * size_quotas[list(cloth_data[category].keys()).index(size)])
                    if quantity < expected_quantity:
                        tailles_inferieures += 1

                return tailles_inferieures

            tailles_inferieures = count_tailles_inferieures(cloth_data, desired_data, size_quotas)

            # Loop through each size in the cloth data for this category
            for size, quantity in cloth_data[category].items():
                # Multiply the desired number of items by the size quota to get the expected quantity
                expected_quantity = int(category_data['desired_number_of_items'] * size_quotas[list(cloth_data[category].keys()).index(size)])

                print(cloth_data[category])
                # Compare the effective quantity with the expected quantity
                if quantity < expected_quantity:
                    category_results[size] = f'UNDERSTOCK ({quantity} < {expected_quantity})'

                    # Launch the scraping script with the difference as the number of items to fetch
                    pieces_a_chercher = expected_quantity - quantity
                    query = category_data['query']
                    site = category_data['url']+"&size_id[]="+str(size_dict[size])

                    #defines the parameters to pass to the scraping script
                    cmd = ['python', '../Utilitaries/vinted_scraping_script.py', site, str(pieces_a_chercher), str(query), str(session_token)]

                    #displays an informational message
                    status_placeholder.info(f"Lancement de la recherche de {pieces_a_chercher} {category} en {size}...")

                    #launches the scrapping process
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    while process.poll() is None:
                        # Read the progress from the file "progress_bar_data.txt"
                        with open("../Assets/Data/progress_bar_data.txt", "r") as f:
                            progress = float(f.read().strip())
                            normalized_progress = progress / 100

                            # Update the progress bar
                            progress_placeholder.progress(normalized_progress, f"Avancement du restockage pour la {size} : {progress}%.")

                            # Sleep for a short duration to avoid excessive updates
                            time.sleep(0.1)

                    # The script_b.py execution has completed
                    status_placeholder_2.success(f"La recherche des {pieces_a_chercher} {category} en {size} est terminée")

                    #updates the progress of the collection fetching
                    i+=1
                    normalized_progress_2 = i/tailles_inferieures
                    progress_placeholder_2.progress(normalized_progress_2, f"Avancement du restockage pour {category} : {i}/{tailles_inferieures} tailles.")

                elif quantity == expected_quantity:
                    category_results[size] = 'OK'
                else:
                    category_results[size] = f'OVERSTOCK ({quantity} > {expected_quantity})'

            # Add the category results to the overall results dictionary
            results[category] = category_results

        # The script_b.py execution has completed
        status_placeholder = st.empty()
        status_placeholder_2.success(f"Le restockage est terminé, bien joué !")
        st.balloons()


