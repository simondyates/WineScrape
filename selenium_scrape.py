from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import re

def scrape_parker():
#Use selenium to scrape the robertparker.com vintages table
    driver = webdriver.Chrome()
    driver.get("https://www.robertparker.com/resources/vintage-chart")

    rows = WebDriverWait(driver, 10).until(
                           EC.presence_of_all_elements_located((By.XPATH, '//table[@class="vintage-scores draggable"]//a')))
    wine_list = []
    for row in rows:
        wine = row.get_attribute('title')
        print(wine)
        wine_list.append([wine , row.text])

    wine_df = pd.DataFrame(wine_list, columns=['identifier', 'rating'])
    wine_df.to_csv('parkervintages.csv', index=False)
    driver.close()

# If we haven't already, run the web scraping function above
if not Path('parkervintages.csv').exists():
    scrape_parker()

# Use regex to parse the two fields
wine_df = pd.read_csv('parkervintages.csv')
wine_df['identifier'] = wine_df['identifier'].apply(str.replace, args=('\n', ' '))

def parse_identifier(s):
    re.search('(....) ()')