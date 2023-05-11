import dateutil.utils
import pandas as pd
import time
import sys
import logging
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


#defines the web browser's options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_argument("--headless") #hides the browser tabs
chrome_options.add_argument("log-level=2") #hides the headless error messages from the console
chrome_options.add_argument(("--disable-gpu"))
logging.getLogger('tensorflow').disabled = True

# Define the function to open the item link in a new tab
def open_in_new_tab(link):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

#Loads the progress bar to track the progress of 'i'
progress_file = "../Assets/Data/progress_bar_data.txt"
i=0
page=1
with open(progress_file, "w") as f:
    f.write("0")  # Initialize the progress to 0

#gets the search parameters from the parent script
url = sys.argv[1]
pieces_a_chercher = int(sys.argv[2])
query = sys.argv[3]
session_token = sys.argv[4]
category = sys.argv[5]

#opens the web browser and searches
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
try:
    # Define the wait instance, waits for the cookie accept button to load then clicks on it
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
except TimeoutException:
    print("Pas de cookie notice")
    pass


# Halts for the page to load
time.sleep(5)

# Load existing item data from CSV file to a DataFrame
file_path = '../Assets/Data/test_data.csv'
existing_data = pd.read_csv(file_path)

# Defines the data list and loads every item's individual link on the Vinted search page
data = []
items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')
if len(items)<pieces_a_chercher:
    pieces_a_chercher=len(items)

# Starts the scrapping process
while i < pieces_a_chercher:



    # For every item's link located on the search result page...
    for item in items:

        # breaks the while loop above if the number of items 'i' meets the specified number of items 'pieces_a_rechercher'
        if i >= pieces_a_chercher:
            print(f"{i} pièces ont été collectées, fin du processus.")
            break
        # Open said link in a new tab
        try:
            # Check if the item is a duplicate
            item_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if item_link in existing_data['item_link'].values:
                continue  # Skip this item if it's a duplicate
            open_in_new_tab(item_link)  # Open the item link in a new tab


            try:
                #defines the images links to fetch and stores them in the img_links list
                try :
                    img_links =[]
                    imgs = driver.find_elements(By.CSS_SELECTOR, "div div div div div div [class='web_ui__Image__image web_ui__Image__cover web_ui__Image__scaled']")
                    for img in imgs:
                        img_link = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        img_links.append(img_link)
                except Exception as e:
                    print(f"Erreur dans la collecte des images : {e}")

                item_title = driver.find_element(By.CSS_SELECTOR, "div div div div div div div div div div[itemprop='name'] h2").text

                item_brand = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[itemprop='brand'] a span"))).text

                try:
                    item_color = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,  "div div div div div div div div[data-testid='item-attributes-color'] div[class='details-list__item-value']"))).text
                except:
                    item_color = "pas de couleur"

                item_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__heading.web_ui__Text__left"))).text

                item_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div[itemprop='description']"))).text

                try:
                    item_size = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div[itemprop='size']"))).text
                except:
                    item_size = "pas de taille"

                item_views = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text

                item_location = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-details-location'] div[class='details-list__item-value']"))).text

                item_date_added = driver.find_element(By.CSS_SELECTOR, "div div div div div div [data-testid='item-details-uploaded_date'] div[class='details-list__item-value'] div span").get_attribute('title')

                try:
                    item_followers = driver.find_element(By.CSS_SELECTOR, "div div div div div div div [data-testid='item-details-interested_count'] div[class='details-list__item-value']").text
                except NoSuchElementException:
                    item_followers = "0 membre intéressé"

                # Appends the list "data" defined before the while loop with the item's data
                data.append({
                    'item_title': item_title,
                    'item_picture': img_links,
                    'item_link': item_link,
                    'item_brand': item_brand,
                    'item_color': item_color,
                    'item_price': item_price,
                    'item_description': item_description,
                    'item_size': item_size,
                    'item_initial_views': str(item_views),
                    'item_location': item_location,
                    'item_date_added': item_date_added,
                    'item_initial_followers': str(item_followers),
                    'query': query,
                    'session_token': session_token,
                    'date_scrapped': dt.today().strftime("%d/%m/%Y"),
                    'status': 'pending',
                    'raindrop_id': '',
                    'raindrop_last_update': '',
                    'raindrop_collection': category,
                    'raindrop_sort': '',
                    'raindrop_collection_id': ''
                })

                # Update the progress bar by writing to the progress_file.txt
                i += 1
                progress = (i / pieces_a_chercher) * 100
                try:
                    with open(progress_file, "w") as f:
                        f.write(str(round(progress)))  # Write the progress to the file
                        print(progress)
                except Exception as e:
                    print(f"La bar de chargement a planté :{e}")
                    pass


                driver.close()  # Close the current tab
                driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab

            except Exception as e:

                print(f"La collecte des informations sur la page a échoué, message d'erreur: {e}. Lien suivant.")
                continue

        except Exception as e:
            print(
                f"Le navigateur n'a pas réussi à ouvrir le lien dans un nouvel onglet, message d'erreur: {e}. Lien suivant.")
            continue

    #the page has been entirely scraped but we need more data...
    if i < pieces_a_chercher:

        page+=1
        url=url+f"&page={page}"
        driver.get(url)
        time.sleep(7)
        items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')
        print("Page suivante...")

    else:
        break



# Create a pandas dataframe to store the item data
df = pd.DataFrame(data)

# Append the dataframe to an existing CSV file or create a new file if it doesn't exist
file_path = '../Assets/Data/test_data.csv'
df.to_csv(file_path, mode='a', header=False, index=False)

# Close the webdriver
driver.quit()

#progress_bar.close()  # Close the progress bar

