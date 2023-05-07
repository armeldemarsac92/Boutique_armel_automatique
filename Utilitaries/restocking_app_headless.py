import json
import random
import subprocess
with open ("../Assets/Catalogs/size_catalog.json", "r") as size_catalog:
    size_dict=json.load(size_catalog)

#this script performs the restocking of the boutique, it is the headless version of compare_qnatities.py and made to be executed automatically from scripts_launcher.py

# Read and parse the three files
with open('../Assets/Data/item_quantites_per_cat_and_size_summed_up.json', 'r') as f1, open(
        '../Assets/Data/query_urls.json', 'r') as f2, open('../Assets/Data/size_quotas.json', 'r') as f3:
    cloth_data = json.load(f1)
    desired_data = json.load(f2)
    size_quotas = json.load(f3)

# Initialize a dictionary to store the results
results = {}

session_token = random.randint(0,10000)



# Loop through each category in the desired data
for category, category_data in desired_data['data'].items():
    # Initialize a dictionary to store the category results
    category_results = {}

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

            print("Launching scraping process...")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print("Scraping process completed.")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")


        elif quantity == expected_quantity:
            category_results[size] = 'OK'
        else:
            category_results[size] = f'OVERSTOCK ({quantity} > {expected_quantity})'

    # Add the category results to the overall results dictionary
    results[category] = category_results



