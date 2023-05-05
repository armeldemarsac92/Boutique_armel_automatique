from random import random
import requests
import json
import time
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import tag_raindrops


# read credentials.json file
with open('../Assets/Data/credentials.json') as f:
    token = json.load(f)
    api_key = token['api_key']


def main():
    # get all ids to iterate over and click on each link
    list_of_ids = get_colections_ids()
    df = get_all_items(list_of_ids)
    check_vinted_urls(df)
    tag_raindrops.add_tag_to_sold_items()
    print("Done!")


def get_colections_ids() -> list:
    url = f'https://api.raindrop.io/rest/v1/collections/childrens'
    response = requests.get(url, headers={'Authorization': api_key})
    collections = response.json()
    list_of_ids = []
    for collection in collections['items']:
        list_of_ids.append(collection['_id'])
    return list_of_ids


def get_all_items(all_collections_ids: list) -> pd.DataFrame:
    df_all_products = pd.DataFrame()
    print("Getting all items from all collections...")
    for collection_id in tqdm(all_collections_ids):
        df_intermediate = get_raindrop_collection(collection_id)
        df_all_products = pd.concat([df_all_products, df_intermediate], ignore_index=True)
    return df_all_products


def get_raindrop_collection(collection_id):
    per_page = 25  # number of items per page
    current_page = 0
    all_items = []

    # Define a function that retrieves a single page of data and appends it to the all_items list
    def get_collection_page():
        nonlocal current_page
        response = requests.get(f"https://api.raindrop.io/rest/v1/raindrops/{collection_id}",
                                params={
                                    "perPage": f"{per_page}",
                                    "page": f"{current_page}",
                                }, headers={
                                    "Authorization": f"{api_key}",
                                })
        # if responce is empty return empty dataframe

        data = response.json()
        current_page += 1
        time.sleep(0.6)
        return pd.DataFrame(data['items'])

    # Call the function repeatedly until all pages have been retrieved
    while True:
        df_page_items = get_collection_page()
        all_items.append(df_page_items)
        if len(df_page_items) < per_page:  # if the last page has less than 50 items, we reached the end of the collection
            break

    # Concatenate all dataframes into a single dataframe
    all_items_df = pd.concat(all_items, ignore_index=True)

    return all_items_df


def check_vinted_urls(df: pd.DataFrame) -> pd.DataFrame:
    # filter df to keep only vinted urls not containing a tag "vendu" in the list of tags
    df_filterd = df[df['domain'].str.contains("vinted")]
    df_filtered = df_filterd[~df_filterd['tags'].apply(lambda x: 'vendu' in x)]

    # Start a headless browser instance
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    # Iterate over the rows of the filtered df
    for index, row in tqdm(df_filtered.iterrows(), total=len(df_filtered)):
        # Load the URL
        driver.get(row['link'])
        # driver.implicitly_wait(4)  # to avoid being blocked by vinted
        try:
            # Click the "Accepter tout" button
            button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            button.click()
            driver.implicitly_wait(1)
        except NoSuchElementException:
            # Handle the exception
            pass
        try:
            # Find an element by class name (that doesn't exist)
            driver.find_element(By.CLASS_NAME, "notification__title--standalone")

            # This item is sold. adding tag "vendu" to it
            df_filtered.at[index, 'tags'] = df_filtered.at[index, 'tags'] + ['vendu']
        except NoSuchElementException:
            # Handle the exception
            pass

    # add the lines not containing vinted urls to the filtered df
    df_filtered = pd.concat([df_filtered, df[~df['domain'].str.contains("vinted")]], ignore_index=True)

    df_filtered.to_csv('../Assets/Data/data.csv', index=False)
    return df_filtered


if __name__ == '__main__':
    main()
