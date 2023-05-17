def app5():
    import streamlit as st
    import pandas as pd
    import json
    import subprocess

    def display_item(item, item_index):
        st.write(f"Item title: {item['item_title']}")


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
        st.write(f"Item price: {item['item_price']}")

        with st.form("item_actions"):
            like_button = st.form_submit_button(f"Like {item['item_title']}")
            dislike_button = st.form_submit_button(f"Dislike {item['item_title']}")
            add_button = st.form_submit_button("Add Items")

            if like_button:
                df.loc[item_index, 'status'] = 'validated'
                df.to_csv(file_path, index=False)
                return True
            if dislike_button:
                df.loc[item_index, 'status'] = 'rejected'
                df.to_csv(file_path, index=False)
                return True

            if add_button:
                # Call the external Python script
                subprocess.call(["python", "../Utilitaries/add_validated_items_to_raindrop.py"])

        return False


    st.title('Review Items')

    # Replace 'your_file_path.csv' with the actual file path of your CSV file
    file_path = '../Assets/Data/item_data_scrapped_from_vinted2.csv'

    # Load the existing CSV file or create a new DataFrame
    df = pd.read_csv(file_path)

    pending_items = df[df['status'] == 'pending']

    if 'current_item_index' not in st.session_state:
        st.session_state.current_item_index = 0

    pending_item_indexes = pending_items.index.tolist()

    if pending_item_indexes:
        current_item_index = pending_item_indexes[st.session_state.current_item_index]
        if display_item(pending_items.loc[current_item_index], current_item_index):
            st.session_state.current_item_index += 1
            if st.session_state.current_item_index >= len(pending_item_indexes):
                st.session_state.current_item_index = 0

    else:
        st.write("No pending items.")

    # Save the final DataFrame to the CSV file
    df.to_csv(file_path, index=False)
