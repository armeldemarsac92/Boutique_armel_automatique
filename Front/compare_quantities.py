def app4():
    import json
    import os
    import subprocess
    import streamlit as st
    import time
    with open ("../Assets/Catalogs/size_catalog.json", "r") as size_catalog:
        size_dict=json.load(size_catalog)

    st.title("Restockage de la boutique")

    #collects and prepares the collection data
    get_items = ("Python","../Utilitaries/get_collections_and_item_data_from_raindrop.py")
    sum_up = ("Python","../Utilitaries/sums_up_sizes_available_per_collection.py")
    subprocess.Popen(get_items, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.Popen(sum_up, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # Create an empty placeholder element for the collection progress bar
    progress_placeholder_2 = st.empty()
    st.divider
    # Create an empty placeholder element for the size progress bar
    progress_placeholder = st.empty()

    # Create an empty placeholder element for the status message
    status_placeholder = st.empty()

    # Read and parse the three files
    with open('../Assets/Data/item_quantites_per_cat_and_size_summed_up.json', 'r') as f1, open(
            '../Assets/Data/query_urls.json', 'r') as f2, open('../Assets/Data/size_quotas.json', 'r') as f3:
        cloth_data = json.load(f1)
        desired_data = json.load(f2)
        size_quotas = json.load(f3)

    # Initialize a dictionary to store the results
    results = {}

    #initiate i to track the progress of the collection fetching
    i=0


    if st.button("lancer le restockage"):
        # Loop through each category in the desired data
        for category, category_data in desired_data['data'].items():
            # Initialize a dictionary to store the category results
            category_results = {}


            # Loop through each size in the cloth data for this category
            for size, quantity in cloth_data[category].items():
                # Multiply the desired number of items by the size quota to get the expected quantity
                expected_quantity = int(category_data['desired_number_of_items'] * size_quotas[list(cloth_data[category].keys()).index(size)])

                # Compare the effective quantity with the expected quantity
                if quantity < expected_quantity:
                    category_results[size] = f'UNDERSTOCK ({quantity} < {expected_quantity})'

                    # Launch the scraping script with the difference as the number of items to fetch
                    pieces_a_chercher = expected_quantity - quantity
                    query = category_data['query']
                    site = category_data['url']+"&size_id[]="+str(size_dict[size])

                    #defines the parameters to pass to the scraping script
                    cmd = ['python', '../Utilitaries/vinted_scraping_script.py', site, str(pieces_a_chercher), str(query)]

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
                            progress_placeholder.progress(normalized_progress, f"Avancement du restockage pour la {size}")

                            # Sleep for a short duration to avoid excessive updates
                            time.sleep(0.1)

                    # The script_b.py execution has completed
                    status_placeholder.success(f"La recherche des {pieces_a_chercher} {category} en {size} est terminée")
                    i+=1
                    normalized_progress_2 = i/len(size_dict)
                    progress_placeholder_2.progress(normalized_progress_2, f"Avancement du restockage pour {category}")

                    print(pieces_a_chercher,query,site)
                elif quantity == expected_quantity:
                    category_results[size] = 'OK'
                else:
                    category_results[size] = f'OVERTOCK ({quantity} > {expected_quantity})'

            # Add the category results to the overall results dictionary
            results[category] = category_results

        # Print the results
        print(json.dumps(results, indent=4))