import csv
import time

import requests

API_URL = 'https://api.raindrop.io/rest/v1/raindrop'
API_TOKEN = '06c08b65-8b7a-46f6-b5ce-f8daa8659e34'

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

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

        collection_dict[title] = id


    def clean_data(price_str):
        """Remove currency symbol and convert comma to dot."""
        cleaned_data = price_str.replace('€', '').replace(',', '.').strip()
        return cleaned_data

    def get_price_tag(price):
        """Categorize price into a range and return the corresponding tag."""
        if price <= 15:
            return 'moins de 15€ 😍'
        elif 16 <= price <= 49:
            return 'de 16 à 49€ 😏'
        elif 50 <= price <= 99:
            return 'de 50 à 99€ 🫣'
        elif 100 <= price <= 150:
            return 'de 100 à 150€ 😳'
        elif price > 150:
            return 'plus de 150€ 🥵'
        else:
            return ''

# Predefined tags list
tags_list = ['Taille 44 🇮🇹', 'Gris', 'Lumineux ⬜️', 'Militaire 🪖', 'de 16 à 49€ 😏', 'Texturé', 'Uni', 'Taille S',
             'Taille M', 'Taille XS', 'Bleu', 'Sombre ⬛️', 'Formel', 'Casual ✌🏻', 'carreaux', 'motifs', 'Beige',
             'de 50 à 99€ 🫣', 'Vert', 'plus de 150€ 🥵', 'Croisé', 'Taille XL', 'Taille 36 🇬🇧', 'Taille 50 🇮🇹',
             'Taille 40 🇬🇧', 'Lot', 'Taille 48 🇮🇹', 'de 100 à 150€ 😳', 'Taille 44 🇬🇧', 'Taille 54 🇮🇹', 'Taille L',
             'Marron', 'Velour', 'Mat', 'Rayures', 'Taille 38 🇬🇧', 'Taille 52 🇮🇹', 'Taille 42 🇬🇧', 'Camel',
             'Taille 46 🇮🇹', 'Taille XXXL', 'King size', 'moins de 15€ 😍', 'Taille 47 🇮🇹', 'Taille 37 🇬🇧', 'Rouge',
             'Blanc', 'Denim', 'Taille 40 🇮🇹', 'Taille 56 🇮🇹', 'Taille XXL', 'Taille 58 🇮🇹', 'Noir', 'Brillant',
             'Pointure 42 🇫🇷', 'Pointure 44 🇫🇷', 'Pointure 41 🇫🇷', 'Pointure 38 🇫🇷', 'Pointure 40 🇫🇷',
             'Pointure 45 🇫🇷', 'Pointure 39 🇫🇷', 'Pointure 43 🇫🇷', 'Multicolore', 'uni', 'Orange', 'Jaune', 'Rose',
             'Pointure 49 🇫🇷', 'W32 🇺🇸', 'L34 🇺🇸', 'W31 🇺🇸', 'L30 🇺🇸', 'W29 🇺🇸', 'W34 🇺🇸', 'L32 🇺🇸', 'W30 🇺🇸','W33 🇺🇸', 'W36 🇺🇸', 'W40 🇺🇸', 'L29 🇺🇸', 'W35 🇺🇸', 'Taille 42 🇫🇷', 'Texte', 'Violet']

formal_categories = ['Vestes, blazers et costumes', 'Chemises','Mocassins', 'Derbies et Richelieu', 'Chaussures à boucles', 'Bottines et boots', 'Velours côtelé', 'Pantalons taille haute', 'Chinos',
                     'Foulards, cravates et écharpes', 'Bretelles']

casual_categories = ['Veste de travail', 'Sur-chemises et vareuses',
                     'Manteaux, pardessus & vestes', 'Gilets & doudounes ss manches', 'Blousons', 'Manteaux & vestes',
                     'Tee shirts et marinières', 'Sweat shirts', 'Pulls', 'Polos', 'Chemises', 'Sneakers',
                     'Chaussures bateau','Bottines et boots',
                     'Chaussures', 'Velours côtelé', 'Pantalons taille haute', 'Jeans', 'Chinos', 'Ceintures & maroquinerie']

keywords_tags = {
    # French keywords
    'militaire': 'Militaire 🪖',
    'camouflage': 'Militaire 🪖',
    'armée': 'Militaire 🪖',
    'kaki': 'Militaire 🪖',
    'treillis': 'Militaire 🪖',
    'uniforme': 'Militaire 🪖',
    'para': 'Militaire 🪖',
    'commando': 'Militaire 🪖',
    'béret': 'Militaire 🪖',
    # Italian keywords
    'militare': 'Militaire 🪖',
    'camuffamento': 'Militaire 🪖',
    'esercito': 'Militaire 🪖',
    'kaki': 'Militaire 🪖',
    'tuta': 'Militaire 🪖',
    'uniforme': 'Militaire 🪖',
    'paracadutista': 'Militaire 🪖',
    'commando': 'Militaire 🪖',
    'berretto': 'Militaire 🪖',
    # English keywords
    'military': 'Militaire 🪖',
    'camouflage': 'Militaire 🪖',
    'army': 'Militaire 🪖',
    'khaki': 'Militaire 🪖',
    'uniform': 'Militaire 🪖',
    'paratrooper': 'Militaire 🪖',
    'commando': 'Militaire 🪖',
    'beret': 'Militaire 🪖',
    #other keywords
    'rayé': 'Rayures',
    'texturé': 'Texturé',
    'velour': 'Mat',
    'daim': 'Mat',
    'vellusto': 'Mat',
    'cotelé':'Mat',
    'cotelé':'Texturé',
    'a coste':'Texturé',
    'a coste':'Texturé',
    'righe':'Rayé',
    'rayures': 'Rayures',
    'carreaux': 'Carreaux'
}


light_colors = ["Blanc", "Crème", "Beige", "Abricot", "Orange", "Corail", "Rose", "Rose fushia", "Lila", "Bleu clair", "Turquoise", "Menthe", "Moutarde", "Jaune", "Argent"]
dark_colors = ["Noir", "Gris", "Rouge", "Bordeaux", "Violet", "Bleu", "Marine", "Vert", "Vert foncé", "Kaki", "Marron", "Doré"]
multicolor = ["Multicolore"]


# Prepare an empty dictionary to store the new data
data = {
    'item_link': [],
    'raindrop_id': [],
    'raindrop_last_update': [],
    'raindrop_collection_id': []
}
i=0
# Read the CSV file
with open('../Assets/Data/test_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:

        if i >= 1000 :
            break
        # Only process rows with status 'validated'
        if row['status'] == 'pending':
            # Prepare tags for the API request
            colors = [color.strip().lower() for color in row['item_color'].split(',')]
            size = "Taille " + row['item_size'].split('\n')[0]  # Format size to 'Taille X'
            tags = [row['item_brand'].lower(), size] + colors

            # Check if color, size, or brand tags exist, if not create new ones
            for tag in tags:
                if tag not in tags_list:
                    tags_list.append(tag)

            # Check if "48" is in the description and add the corresponding tag
            if "48" in row['item_description']:
                tags.append("Taille 48 🇮🇹")

            # Check if the item's category is formal or casual
            if any(category in row['raindrop_collection'] for category in formal_categories):
                tags.append('Formel')
            if any(category in row['raindrop_collection'] for category in casual_categories):
                tags.append('Casual ✌🏻')

            # Check for keywords
            for keyword, tag in keywords_tags.items():
                if keyword in row['item_description']:
                    tags.append(tag)
            # Check for keywords in title
            for keyword, tag in keywords_tags.items():
                if keyword in row['item_title']:
                    tags.append(tag)

            #Check for the color tone
            if any(color in row['item_color'] for color in light_colors):
                tags.append('Lumineux ⬜️')
            if any(color in row['item_color'] for color in dark_colors):
                tags.append('Sombre ⬛️')
            if any(color in row['item_color'] for color in multicolor):
                tags.append('Multicolore')
            if len(['item_color']) == 1 and not 'multicolore':
                tags.append('Uni')
            if len(['item_color'])>1:
                tags.append('Motifs')
            if 'Rayures' in tags :
                tags.append('Motifs')
            if 'Carreaux' in tags :
                tags.append('Motifs')
            if 'jean' in row['item_description']:
                tags.append('Denim')
                tags.remove('Formel')
            if 'jean' in row['item_title']:
                tags.append('Denim')
                tags.remove('Formel')
            if 'Taille XL' in tags:
                tags.append('King size')
            if 'Taille XXL' in tags:
                tags.append('King size')




            price = float(clean_data(row['item_price']))
            price_tag = get_price_tag(price)
            tags.append(price_tag)

            # Prepare the data for the API request
            data_for_request = {
                'collection': {'$id': row['raindrop_collection_id']},
                'title': row['item_title'],
                'link': row['item_link'],
                'tags': tags,
                'description': row['item_description'],
                'cover': row['item_picture'][0],

            }

            # Make the API request to create a new Raindrop
            response = requests.post(API_URL, headers=headers, json=data_for_request)

            if response.status_code == 200:
                try:
                    response_json = response.json()

                    # Save the new Raindrop ID and other data
                    data['item_link'].append(response_json['item']['link'])
                    data['raindrop_id'].append(response_json['item']['_id'])
                    data['raindrop_last_update'].append(response_json['item']['lastUpdate'])
                    print(response.content)
                    i+=1
                except ValueError:
                    print("JSON decoding failed. Raw response content:")
                    print(response.content)
                    time.sleep(0.5)
            else:
                print(f"Request failed with status code {response.status_code}. Raw response content:")
                print(response.content)

# Start by reading the CSV file into a list of dictionaries
with open('../Assets/Data/test_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Update the appropriate rows
for row in rows:
    for i in range(len(data['item_link'])):
        if row['item_link'] == data['item_link'][i]:
            row['raindrop_id'] = data['raindrop_id'][i]
            row['raindrop_last_update'] = data['raindrop_last_update'][i]

# Write the list of dictionaries back out to the file
with open('../Assets/Data/test_data.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['item_title', 'item_picture', 'item_link', 'item_brand', 'item_color', 'item_price',
                  'item_description', 'item_size', 'item_initial_views', 'item_current_views', 'item_location',
                  'item_date_added', 'item_initial_followers', 'item_current_followers', 'query', 'session_token',
                  'date_scrapped', 'status', 'raindrop_id', 'raindrop_last_update', 'raindrop_collection',
                  'raindrop_sort', 'raindrop_collection_id', 'item_date_sold']

    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)


