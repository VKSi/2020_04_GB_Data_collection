from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pymongo import MongoClient
from bson.objectid import ObjectId
import time

from items_grabbing import items_grabbing

if __name__ == '__main__':
    # Start page and options
    options = Options()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.mvideo.ru/')
    assert 'М.Видео' in driver.title

    # MongoDB inicialization
    client = MongoClient( 'localhost' , 27017 )
    db = client['mvideo']
    collection = db.hits

    # Main parsing
    hits = WebDriverWait(driver,20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-hits-block')))[1]  # Defines the block with 'hits'

    while True:  # The loop on sets (by 4) of items. Itterapted by finding 'disabled' class for right-direction arrow
        items = WebDriverWait(hits, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-product-tile-title')))  # Detect all (4) items

        # Grabs items' features and adds them to the base checking unique _id
        for doc in items_grabbing(items):
            oid = doc['_id']
            if collection.find_one({'_id':oid}):
                continue
            else:
                collection.insert_one(doc)

        button = hits.find_element_by_xpath(".//a[contains(@class, 'sel-hits-button-next')]")  # Proceeds to the next set
        time.sleep(2)
        if 'disabled' in button.get_attribute('class'):
            break
        else:
            button.click()

    driver.quit()