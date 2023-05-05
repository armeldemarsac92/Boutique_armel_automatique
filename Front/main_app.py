import streamlit as st
from defines_sizes_quotas import app3
from set_vinted_scraping_parameters import app1
from set_vinted_scraping_parameters_per_collection import app2
from compare_quantities import app4


def main():
    st.set_page_config(page_title='Multi-Page App', layout='wide')

    st.sidebar.title("Navigation")
    app_options = [
        "Sélectionnez une fonctionnalité",
        "Lancer une recherche manuelle",
        "Réglages de catégories",
        "Réglages de tailles",
        "Restocker"
        # ... add other apps as needed
    ]
    choice = st.sidebar.selectbox("Choose an app", app_options)

    if choice == "Réglages de tailles":
        app3()
    elif choice == "Lancer une recherche manuelle":
        app1()
    elif choice == "Réglages de catégories":
        app2()
    elif choice == "Restocker":
        app4()
    # ... add other app options as needed

if __name__ == "__main__":
    main()
