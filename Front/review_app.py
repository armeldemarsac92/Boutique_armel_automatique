import streamlit as st
import pandas as pd
import json

def display_item(item):
    st.write(f"Item title: {item['item_title']}")
    st.write(f"Item price: {item['item_price']}")

    # Parse the list of image URLs from the 'item_picture' column
    image_urls = json.loads(item['item_picture'].replace("'", "\""))

    # Remove duplicate image URLs
    unique_image_urls = list(set(image_urls))

    # Display images in a grid with a maximum of 3 columns per row
    max_columns = 3
    row_count = -(-len(unique_image_urls) // max_columns)  # Ceiling division

    for row in range(row_count):
        cols = st.columns(max_columns)
        for col in range(max_columns):
            index = row * max_columns + col
            if index < len(unique_image_urls):
                cols[col].write(f'<img src="{unique_image_urls[index]}" style="width: 100%; height: auto; object-fit: contain;">', unsafe_allow_html=True)

    with st.form("item_actions"):
        like_button = st.form_submit_button(f"Like {item['item_title']}")
        dislike_button = st.form_submit_button(f"Dislike {item['item_title']}")

        if like_button:
            item['status'] = 'validated'
            return True
        if dislike_button:
            item['status'] = 'rejected'
            return True

    return False


st.title('Review Items')

# Replace 'your_file_path.csv' with the actual file path of your CSV file
file_path = '../Assets/Data/item_data_scrapped_from_vinted2.csv'

# Load the existing CSV file or create a new DataFrame
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=['item_title', 'item_price', 'item_picture', 'status'])

pending_items = df[df['status'] == 'pending']

if 'current_item_index' not in st.session_state:
    st.session_state.current_item_index = 0

if not pending_items.empty:
    if display_item(pending_items.iloc[st.session_state.current_item_index]):
        st.session_state.current_item_index += 1
        if st.session_state.current_item_index >= len(pending_items):
            st.session_state.current_item_index = 0

        # Check if 5 items have been processed
        if st.session_state.current_item_index % 5 == 0:
            # Save the DataFrame to the CSV file
            df.to_csv(file_path, index=False)
else:
    st.write("No pending items.")

# Save the final DataFrame to the CSV file
df.to_csv(file_path, index=False)
