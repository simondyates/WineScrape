from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

#Use selenium to scrape the robertparker.com vintages table

# Open a csv file to store the output
csv_file = open('robertparker_temp.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['href', 'rating'])

# Query the table rows
driver = webdriver.Chrome()
driver.get("https://www.robertparker.com/resources/vintage-chart")
rows = WebDriverWait(driver, 10).until(
                     EC.presence_of_all_elements_located((By.XPATH, '//table[@class="vintage-scores draggable"]//a')))

# Process each row returned
for row in rows:
    wine = row.get_attribute('href')
    # we capture the href not because we want to access the page, but instead
    # because it gives a logically-structured description of the wine that will be parseable
    print(wine) # to keep track of the (slow) progress
    writer.writerow([wine, row.text])

# Clean up
csv_file.close()
driver.close()