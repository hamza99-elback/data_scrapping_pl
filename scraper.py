from typing import Any
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import mysql.connector
from time import sleep
from all_decorators import with_open_and_close_driver

class Scraper:
    def __init__(self, url):
        self.name="Scrape Data from website"
        self.url=url
        self.chrome_options=ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(options=self.chrome_options)
        
        
    def get_website(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        sleep(2)
        self.manage_popup()
        sleep(2)
        
    def manage_popup(self):
        cookies_popup= self.driver.find_element(By.XPATH,"//div[@class='ot-sdk-container']")
        if cookies_popup:
            print("popup found")
            accept_cookis_btn=self.driver.find_element(By.XPATH,"//button[@id='onetrust-accept-btn-handler']")
            accept_cookis_btn.click()
    
    def extract_data(self):
        try:
            # extract rank
            rank_list= self.driver.find_elements(By.XPATH, "//td[@class='stats-table__rank']")
            rank_values_list=[int(rank.text.rstrip('.')) for rank in rank_list]
            print(rank_values_list)
            
            # extract names
            names_list=self.driver.find_elements(By.XPATH, "//td[@class='stats-table__name']")
            names_list_values=[name.test for name in names_list]
            print(names_list_values)
            
        except Exception as e:
            print("Error when extracting data", e)
    
    @with_open_and_close_driver    
    def main(self):
        # get website
        self.get_website()
        
        # extract data
        self.extract_data()
        
