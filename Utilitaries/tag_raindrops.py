import pandas as pd
import requests
import json
import time
from tqdm import tqdm
import ast

# read credentials.json file
with open('../Assets/Data/credentials.json') as f:
    api_key = json.load(f)['api_key']


def add_tag_to_sold_items():
    df = pd.read_csv('data.csv')
    df_items_to_tag = df[df['tags'].apply(lambda x: 'vendu' in x)]
    headers = {"Authorization": f"{api_key}", "Content-Type": "application/json"}

    for index, row in tqdm(df_items_to_tag.iterrows(), total=len(df_items_to_tag)):
        api_url = 'https://api.raindrop.io/rest/v1/raindrop/' + str(row['_id'])
        data = {"tags": ast.literal_eval(row['tags'])}
        response = requests.put(api_url, headers=headers, json=data)
        if response.status_code != 200:
            print("failed to update for id " + str(row['_id']))
        time.sleep(1)  # to avoid saturating the api


if __name__ == '__main__':
    add_tag_to_sold_items()
