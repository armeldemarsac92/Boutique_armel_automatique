import pandas as pd
import json



# Read the 'collections.csv' file using pandas
def read_collections_csv(file_name="collections.csv"):
    return pd.read_csv(file_name)

# Filter the DataFrame for the specific tags and print the raindrop quantities
def check_tag_quantities(df, tags):
    # Extract collection information
    collection_info = df[["ID", "Title", "Parent_ID", "Count"]]

    # Print raindrop quantities for each tag in each collection
    for index, row in collection_info.iterrows():
        print(f"Collection: {row['Title']} (ID: {row['ID']})")
        for tag in tags:
            print(f"  - {tag}: {df.at[index, tag]} raindrops")
        print()

def main():
    # Read the CSV file
    df = read_collections_csv()

    # Define the tags to check
    tags = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

    store_tag_quantities(df, tags)

    # Check and print the raindrop quantities for the specified tags
    check_tag_quantities(df, tags)

# Filter the DataFrame for the specific tags and store the raindrop quantities in a JSON file
def store_tag_quantities(df, tags, file_name="tag_quantities.json"):
    quantities = {}

    for tag in tags:
        tag_quantities = {}

        for index, row in df.iterrows():
            if row[tag] > 0:
                collection_id = row["ID"]
                collection_title = row["Title"]
                tag_quantities[collection_title] = row[tag]

        quantities[tag] = tag_quantities

    with open(file_name, "w") as file:
        json.dump(quantities, file)

    print(f"Tag quantities stored in {file_name}")



if __name__ == "__main__":
    main()


