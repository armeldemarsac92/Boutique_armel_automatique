# main.py
import streamlit as st
from defines_sizes_quotas import app3
from set_vinted_scraping_parameters import app1
from set_vinted_scraping_parameters_per_collection import app2
from compare_quantities import app4
from review_app import app5
from stat_page import app6

def main():
    st.sidebar.title("Navigation")
    app_options = [
        "Sélectionnez une fonctionnalité",
        "Lancer une recherche manuelle",
        "Réglages de catégories",
        "Réglages de tailles",
        "Restocker",
        "Review",
        "Stats"
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
    elif choice == "Review":
        app5()
    elif choice == "Stats":
        app6()

if __name__ == "__main__":
    main()
