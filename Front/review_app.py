def app5():
    import streamlit as st
    import pandas as pd
    import json

    def display_item(df, item_index):
        csv_row_number = item_index + 2  # Adjust for 0-based indexing and header row
        st.write(f"CSV row number: {csv_row_number}")
        st.write(f"Item title: {df.loc[item_index, 'item_title']}")

        # Parse the list of image URLs from the 'item_picture' column
        image_urls = json.loads(df.loc[item_index, 'item_picture'].replace("'", "\""))

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
                    cols[col].write(
                        f'<img src="{unique_image_urls[index]}" style="width: 100%; height: auto; object-fit: contain;">',
                        unsafe_allow_html=True)
        st.write(f"Item price: {df.loc[item_index, 'item_price']}")

        like_button = st.button(f"Like {df.loc[item_index, 'item_title']}")
        dislike_button = st.button(f"Dislike {df.loc[item_index, 'item_title']}")

        if like_button:
            df.loc[item_index, 'status'] = 'validated'


        if dislike_button:
            df.loc[item_index, 'status'] = 'rejected'


        return False

    st.title('Review Items')

    # Replace 'your_file_path.csv' with the actual file path of your CSV file
    file_path = '../Assets/Data/item_data_scrapped_from_vinted.csv'

    # Load the existing CSV file or create a new DataFrame
    df = pd.read_csv(file_path)

    pending_items = df[df['status'] == 'pending']
    validated_items = df[df['status'] == 'validated']
    rejected_items = df[df['status'] == 'rejected']

    st.write(f"Pending items: {len(pending_items)}")
    st.write(f"Validated items: {len(validated_items)}")
    st.write(f"Rejected items: {len(rejected_items)}")

    if 'current_item_index' not in st.session_state:
        st.session_state.current_item_index = 0

    pending_item_indexes = pending_items.index.tolist()

    if pending_item_indexes:
        current_item_index = pending_item_indexes[st.session_state.current_item_index]
        if display_item(df, current_item_index):
            st.session_state.current_item_index += 1
            if st.session_state.current_item_index >= len(pending_item_indexes):
                st.session_state.current_item_index = 0

        # Save the DataFrame after every interaction
        df.to_csv(file_path, index=False)
