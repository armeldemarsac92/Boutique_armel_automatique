import json
import csv
import random
import subprocess
with open("../Assets/Catalogs/size_catalog.json", "r") as size_catalog:
    size_dict = json.load(size_catalog)
import pandas as pd
import ast

# This script performs the restocking of the boutique, it is the headless version of compare_qnatities.py
# and made to be executed automatically from scripts_launcher.py

# Read and parse the three files
with open('../Assets/Data/size_quotas.json', 'r') as f3:
    size_quotas = json.load(f3)


# Define the tags you're interested in
tags_of_interest = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../Assets/Data/item_quantities_per_tags_and_collections2.csv', encoding='utf-8')
# filter DataFrame to exclude rows where 'desired_number_of_items' is empty
df = df[df['desired_number_of_items'].notna()]

# Initialize an empty dictionary to store the item quantities
cloth_data = {}

# Loop through each row in the DataFrame
for _, row in df.iterrows():
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

# Read the existing query URLs and parameters from the DataFrame
query_urls = {}

if 'query' in df.columns:
    print('abc')
    for _, row in df.iterrows():
        collection = row['Title']
        parameters = {
            'query': row['query'],
            'brand_ids': row['brand_ids'],
            'category_ids': row['category_ids'],
            'color_ids': row['color_ids'],
            'desired_number_of_items': row['desired_number_of_items'],
            'url': row['url'],
            'ID': row['ID'],
            'Title': row['Title']
        }
        query_urls[collection] = parameters

# Initialize a dictionary to store the results
results = {}

session_token = random.randint(0, 10000)

# Loop through each category in the query URLs and parameters
for category, parameters in query_urls.items():
    # Initialize a dictionary to store the category results
    category_results = {}
    print('a')

    # Loop through each size in the cloth data for this category
    for size, quantity in cloth_data[category].items():
        print(size)

        # Convert brand_ids from string to list
        brand_ids = ast.literal_eval(parameters['brand_ids'])
        for brand_id in brand_ids:

            print(brand_id)

            # Multiply the desired number of items by the size quota to get the expected quantity
            expected_quantity = int(parameters['desired_number_of_items'] * size_quotas[list(cloth_data[category].keys()).index(size)])
            print(f'we expect {expected_quantity} items.')
            # Compare the effective quantity with the expected quantity
            if quantity < expected_quantity:
                category_results[size] = f'UNDERSTOCK ({quantity} < {expected_quantity})'

                # Launch the scraping script with the difference as the number of items to fetch
                pieces_a_chercher = round((expected_quantity - quantity)/len(brand_ids))
                print(f'We need to fetch {pieces_a_chercher} for {brand_id} in {size}.')

                query = parameters['query']
                brand_ids_str = f"&brand_id[]={brand_id}"
                site = parameters['url'] + "&size_id[]=" + str(size_dict[size]) + "&brand_id[]=" + str(brand_id)

                print(site)

                # Defines the parameters to pass to the scraping script
                cmd = [
                    'python',
                    '../Utilitaries/vinted_scraping_script.py',
                    site,
                    str(pieces_a_chercher),
                    str(query),
                    str(session_token),
                    str(parameters['Title']),
                    str(parameters['ID']),
                ]

                print("Launching scraping process...")
                print(parameters['ID'])
                print(parameters['Title'])
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                print("Scraping process completed.")
                print(f"stdout: {stdout}")
                print(f"stderr: {stderr}")

            elif quantity == expected_quantity:
                category_results[size] = 'OK'
                print(category_results[size])
            else:
                category_results[size] = f'OVERSTOCK ({quantity} > {expected_quantity})'
                print(category_results[size])

        # Add the category results to the overall results dictionary
        results[category] = category_results

