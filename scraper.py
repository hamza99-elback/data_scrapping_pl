from typing import Any
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
# import mysql.connector
from time import sleep
from all_decorators import with_open_and_close_driver
from driverFactory import driverFactory

import pandas as pd

driverfactory=driverFactory()
chrome_options_dict = {
    "start-maximized": True,  # Use None for options without values
    "detach": True
}
chrome=driverFactory(options=chrome_options_dict).create_driver(driver_type="chrome")
driverFactory.add_driver(new_driver={"brave":"hahohi"})
print(driverFactory.get_driver_values())

class Scraper:
    def __init__(self, url, context):
        self.name="Scrape Data from website"
        self.url=url
        self.driver=chrome
        self.context=context
        
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
            names_list_values=[name.text for name in names_list]
            print(names_list_values)
            
            # exctract stats
            stats_list=self.driver.find_elements(By.XPATH, "//td[@class='stats-table__main-stat']")
            stats_list_values=[int(name.text) for name in stats_list]
            print(stats_list_values)
            
            data={
                "rank": rank_values_list,
                "player_name": names_list_values,
                "goals": stats_list_values
            }
            return data
        except Exception as e:
            print("Error when extracting data", e)
            
    
    def export_data_to_excel(self, data):
        try:
            df= pd.DataFrame(data=data)
            df.to_excel("players_data.xlsx", index=False)
            print("Data Exported successfuly")
        except Exception as e:
            print(f"error in export data to excel: {e}")
    
    @with_open_and_close_driver    
    def main(self):
        # get website
        self.get_website()
        
        # extract data
        data = self.extract_data()
        
        # export data
        # self.export_data_to_excel(data=data)
        self.context.data=data
        
