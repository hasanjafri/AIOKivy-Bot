from selenium import webdriver
from selenium.webdriver.support.ui import Select
from config import keys
from helpers import timeme
import time

@timeme
def supreme_pick_and_fill(productType, productKeyword):
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.supremenewyork.com/shop/all/" + productType)
    driver.find_elements_by_xpath("//*[contains(text(), '"+productKeyword+"')]")[0].click()
    time.sleep(.5)

    driver.find_element_by_name('commit').click()

    # wait for checkout button element to load
    time.sleep(.5)
    checkout_element = driver.find_element_by_class_name('checkout')
    checkout_element.click()

    # fill out checkout screen fields
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys['name'])
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(keys['email'])
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys['phone_number'])
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(keys['street_address'])
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys['zip_code'])
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys['city'])
    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(keys['card_cvv'])
    driver.find_elements_by_class_name('icheckbox_minimal')[1].click()

    Select(driver.find_element_by_id('order_billing_country')).select_by_value(keys['country'])
    Select(driver.find_element_by_id('order_billing_state')).select_by_value(keys['state'])
    Select(driver.find_element_by_id('credit_card_month')).select_by_value(keys['expiry_month'])
    Select(driver.find_element_by_id('credit_card_year')).select_by_value(keys['expiry_year'])

    driver.find_element_by_id('nnaerb').send_keys(keys['card_number'])

    process_payment = driver.find_element_by_xpath('//*[@id="pay"]/input')
    process_payment.click()


