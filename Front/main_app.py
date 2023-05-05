import streamlit as st
from defines_sizes_quotas import app3
from set_vinted_scraping_parameters import app1
from set_vinted_scraping_parameters_per_collection import app2


def main():
    st.set_page_config(page_title='Multi-Page App', layout='wide')

    st.sidebar.title("Navigation")
    app_options = [
        "Select an app",
        "App 1",
        "App 2",
        "App 3",
        # ... add other apps as needed
    ]
    choice = st.sidebar.selectbox("Choose an app", app_options)

    if choice == "App 1":
        app1()
    elif choice == "App 2":
        app2()
    elif choice == "App 3":
        app3()
    # ... add other app options as needed

if __name__ == "__main__":
    main()
