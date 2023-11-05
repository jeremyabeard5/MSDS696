# flight-price.py

# MSDS 696
# Jeremy Beard

# Objective:
# This script/project will seek to find the best flights, programmatically, from kayak.com! 
# It's possible other websites could be included in the future, but for now, kayak.com is the only one.
# This script will take a start date, and end date, a departure airport, and an arrival airport, and will return the best flights
# It will find the airline, the price, the departure time, the arrival time, the number of connections (if any), and the duration of the flight.
# This will make it easy for myself and others to find some cheap flights! And maybe even filter by airline or others.

# I want to scrape data from sites such as:
# https://www.kayak.com/flights/DEN-CVG/2023-12-23/2023-12-27/2adults?sort=bestflight_a
# https://www.kayak.com/flights/DEN-CVG/2023-12-23/2023-12-27/2adults?sort=bestflight_a&p=1
# https://www.kayak.com/flights/DEN-CVG/2023-12-23/2023-12-27/2adults?sort=price_a&p=1
# https://www.kayak.com/flights/DEN-CVG/2023-12-23/2023-12-27/2adults?sort=duration_a&p=1

# I am aiming to utilize resources such as:
# https://github.com/rafabelokurows/flight-explorer/blob/main/scrape_kayak.py#L16
# https://github.com/MeshalAlamr/flight-price-prediction/blob/main/kayak-scraper.ipynb
# https://stackoverflow.com/questions/66699301/scraping-prices-from-kayak
# 

# Importing the necessary libraries
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

format = "%Y-%m-%d"

# start the main program
if __name__ == "__main__":
    print("Hello World!")
    
    
    # chromedriver_path = 'C:/Users/Documents/chromedriver.exe'
    #chromedriver_path = 'C\:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-08_Fall\\MSDS696\\MSDS696\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
    chromedriver_path = 'C:\\Users\\jerem\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

    #driver = webdriver.Chrome(executable_path=chromedriver_path)
    
    
    #service = Service(executable_path='C\:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-08_Fall\\MSDS696\\MSDS696\\geckodriver-v0.33.0-win64\\geckodriver.exe')
    service = Service(executable_path='C:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-08_Fall\\MSDS696\\MSDS696\\chromedriver-win64-119\\chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.quit()
        
    
    #wait = WebDriverWait(driver, 10)
    #kayak = 'https://www.kayak.com/flights/DEN-CVG/2023-12-23/2023-12-27/2adults?sort=bestflight_a'
    #driver.get(kayak) 
    #wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[46]/div[3]/div/button'))).click()
    #xp_prices = '//a[@class="booking-link "]/span[@class="price option-text"]'
    #prices = wait.until(EC.presence_of_all_elements_located((By.XPATH,xp_prices)))
    #for price in prices:
    #    print(price.text)