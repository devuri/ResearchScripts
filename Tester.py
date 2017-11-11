#Simple Python Script for Selenium Testing Purposes

from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()
driver.get("https://www.google.com")
sleep(5)
driver.quit()