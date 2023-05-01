from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.vinted.fr")
driver.implicitly_wait(30)
driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()

# Define the wait instance
wait = WebDriverWait(driver, 10)

# Use the wait instance to wait for the element to be clickable and click on it
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'web_ui__InputBar__value')))
element.click()

# Send keys to the element
element.send_keys("veste barbour")
element.send_keys(Keys.RETURN)

# Define the function to open the item link in a new tab
def open_in_new_tab(link):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)

# Scrape the data of each item and store it in a list
data = []

while True:
    driver.implicitly_wait(10)
    items = driver.find_elements(By.CLASS_NAME, 'web_ui__ItemBox__image-container')
    for item in items:
        item_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        open_in_new_tab(item_link)  # Open the item link in a new tab
        try:
            item_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div div[itemprop='name'] h2"))).text
            item_brand = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[itemprop='brand']"))).text
            item_color = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,  "div div div div div div div div[data-testid='item-attributes-color'] div[class='details-list__item-value']"))).text
            item_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".web_ui__Text__text.web_ui__Text__heading.web_ui__Text__left"))).text
            item_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div[itemprop='description']"))).text
            item_size = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div div[itemprop='size']"))).text
            item_views = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-details-view_count'] div[class='details-list__item-value']"))).text
            item_location = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div[data-testid='item-details-location'] div[class='details-list__item-value']"))).text
            item_date_added = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div [data-testid='item-details-uploaded_date'] div[class='details-list__item-value']"))).text
            item_followers = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div div div div div div div div [data-testid='item-details-interested_count'] div[class='details-list__item-value']"))).text

            data.append({
                'item_title': item_title,
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
            })

            driver.close()  # Close the current tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab
        except TimeoutException:

            pass

            driver.close()  # Close the current tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab

    try:
        next_page_button = driver.find_element(By.CLASS_NAME, ('button[data-testid="pagination-next"]'))
        next_page_button.click()  # Click the "Next" button to go to the next page
    except:
        break  # If there is no "Next" button, we have reached the end of the results

# Create a pandas dataframe to store the item data
df = pd.DataFrame(data)

# Save the dataframe as a CSV file
df.to_csv('item_data.csv', index=False)

# Close the webdriver
driver.quit()

