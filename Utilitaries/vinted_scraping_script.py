import pandas as pd
import time
import sys
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import logging
logging.getLogger('tensorflow').disabled = True


#defines the web browser's options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_argument("--headless") #hides the browser tabs
chrome_options.add_argument("log-level=2") #hides the headless error messages from the console

url = sys.argv[1]
pieces_a_chercher = int(sys.argv[2])
query=sys.argv[3]

#opens the web browser and searches
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Define the wait instance, waits for the cookie accept button to load then clicks on it
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
element.click()

# Define the function to open the item link in a new tab
def open_in_new_tab(link):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

#Loads the progress bar to track the progress of 'i'
progress_file = "../Assets/Data/progress_bar_data.txt"
step=0

with open(progress_file, "w") as f:
    f.write("0")  # Initialize the progress to 0




# Defines the data list and loads every item's individual link
data = []
items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')

# Halts for the page to load
time.sleep(5)
i=0


progress_bar = tqdm(total=pieces_a_chercher)  # Initialize the progress bar
# Starts the scrapping process
while i < pieces_a_chercher:


    # For every item's link located on the search result page...
    for item in items:

        # breaks the while loop above if the number of items 'i' meets the specified number of items 'pieces_a_rechercher'
        if i >= pieces_a_chercher:
            break
        # Open said link in a new tab
        try:
            item_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            open_in_new_tab(item_link)  # Open the item link in a new tab


            try:
                #defines the images links to fetch and stores them in the img_links list
                img_links =[]
                imgs = driver.find_elements(By.CSS_SELECTOR, "div div div div div div [class='web_ui__Image__image web_ui__Image__cover web_ui__Image__scaled']")
                for img in imgs:
                    img_link = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    img_links.append(img_link)

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
                    item_followers = "AUCUN MEMBRE INTERESSE"

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
                    'item_views': item_views,
                    'item_location': item_location,
                    'item_date_added': item_date_added,
                    'item_followers': item_followers,
                    'query': query,
                })
                i+=1
                # Update the progress
                step += 1
                progress = (step / pieces_a_chercher) * 100
                with open(progress_file, "w") as f:
                    f.write(str(progress))  # Write the progress to the file

                progress_bar.update(1)  # Update the progress bar


                driver.close()  # Close the current tab

                driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab

            except Exception as e:

                #print(f"Exception encountered: {e}")
                continue
        except Exception as e:
                #print(f"Second exception encountered: {e}")
                continue
    if 90 < i < pieces_a_chercher:
            driver.close()  # Close the current tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab

            driver.get(url)
            time.sleep(7)
            items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')
    else:
        break



# Create a pandas dataframe to store the item data
df = pd.DataFrame(data)

# Save the dataframe as a CSV file
df.to_csv('item_data.csv', index=False)

# Close the webdriver
driver.quit()

#progress_bar.close()  # Close the progress bar

