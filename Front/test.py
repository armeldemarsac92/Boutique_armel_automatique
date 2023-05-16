import json

with open('../Assets/Data/query_urls.json', 'r') as f2:
    desired_data = json.load(f2)

# Sort the inner dictionary by key
desired_data = dict(sorted(desired_data['data'].items()))

print(desired_data)

import pandas as pd

# Define the tags you're interested in
tags_of_interest = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

# Load the data
df = pd.read_csv('../Assets/Data/item_quantities_per_tags_and_collections.csv', encoding='utf-8')

# Filter the dataframe to only include the columns of interest
df = df[['ID', 'Title', 'Parent_ID'] + tags_of_interest]

# Only keep rows that are child collections (those with a non-null Parent_ID)
df = df[df['Parent_ID'].notna()]

# Set 'Title' and 'ID' as the index
df.set_index(['Title', 'ID'], inplace=True)

# Convert the dataframe to a dictionary
cloth_data = df.to_dict('index')

# Create a new dictionary with keys sorted in alphabetical order
cloth_data = dict(sorted(cloth_data.items()))


print(cloth_data)