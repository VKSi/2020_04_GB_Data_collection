from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pprint import pprint
from pymongo import MongoClient
import time
"""
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NewPassword172
"""

def enter(driver, login, password):
    """
    Carry out the loging to the post box

    Args:
        driver (webdriver):  the initial webdriver
        login (str): post-box login
        password (str): post-box password

    Returns:
        webdriver: new driver for the post-box page
    """
    elem = driver.find_element_by_name('Login')
    elem.send_keys(login)
    elem = driver.find_element_by_name('Password')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    return driver

def paginator(driver):
    """
    Turns the pages in the mailbox

    Args:
        driver (webdriver):  the current webdriver

    Returns:
        webdriver: new driver for the next page or None from the last page
    """
    try:
        forward_page_arrow = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@title = 'Следующая страница']")))
        # forward_page_arrow = driver.find_element_by_xpath("//a[@title = 'Следующая страница']")
        forward_page_arrow.click()
    except:
        forward_page_arrow = None

    return forward_page_arrow

def message_features_grabber_base(messages_boxes):
    """
    Grabs the base information for each mail from mail-box page

    Args:
        messages_boxes (webdriver):  the list of messages boxex on the current page

    Returns:
        list: data with base features of mails from the input list (from mail-box page only)
    """
    data = []
    for message in messages_boxes:
        link = message.find_element_by_class_name('messageline__link').get_attribute('href')
        sender = message.find_element_by_class_name('messageline__from').text
        subject = message.find_element_by_class_name('messageline__subject').text
        date = message.find_element_by_class_name('messageline__date').text
        id = str(link).split('/')[-1]
        data.append({'_id':id, 'sender':sender, 'subject':subject, 'date':date, 'link':link})
    return data

def message_features_grabber_advanced(driver, link):
    """
    Grabs the advanced information for the given mail

    Args:
        driver (webdriver):  the current webdriver
        link (str): link to the page with pointed message

    Returns:
        string: advanced info on mail date
        string: the mail body
    """
    driver.get(link)
    date = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'readmsg__mail-date')))
    body = driver.find_element_by_id('readmsg__body')

    return date.text, body.text

if __name__ == '__main__':
    # Start page and options
    options = Options()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://m.mail.ru/login')
    assert 'Вход — Почта Mail.Ru' in driver.title

    # MongoDB inicialization
    client = MongoClient( 'localhost' , 27017 )
    db = client['mail_ru']
    collection = db.mails

    # Mail box credentials
    login = 'study.ai_172'
    password = 'NewPassword172'

    # Main parsing (base information)
    driver = enter(driver, login, password)  # Login to the mail box
    while True:  # The paginator's loop
        messages_boxes = driver.find_elements_by_class_name('messageline')  # Finds all messages bloks
        collection.insert_many(message_features_grabber_base(messages_boxes))  # Collect the base features
        if not paginator(driver):
            break

    # Advanced information update
    for document in collection.find({}):
        id = document.get('_id')
        link = document.get('link')
        document['date'], document['body'] = message_features_grabber_advanced(driver, link)
        collection.update_one({'_id':id}, {'$set': document})

    driver.quit()
