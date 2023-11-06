from typing import Any
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep
from all_decorators import with_open_and_close_driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions


class driverFactory:
    drivers={}
    
    def __init__(self, options=None):
        chrome_options = ChromeOptions()

        # Check if additional options were provided
        if options:
            for option_name, option_value in options.items():
                chrome_options.add_argument(f"--{option_name}={option_value}")

        driverFactory.drivers={
            "chrome": webdriver.Chrome(options=chrome_options),
            "firefox": "webdriver.Firefox()",
            "edge": "webdriver.Edge()"
        }
    @staticmethod
    def create_driver(driver_type):
        """Create a webdriver based on driver type

        Args:
            driver (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        try:
            return driverFactory.drivers[driver_type]
        except Exception as e:
            print(f"error: {e}")
            
    
    @staticmethod
    def add_driver(new_driver):
        """add new driver type to the dict of drivers

        Args:
            new_driver (_type_): _description_
        """
        key=list(new_driver.keys())[0]
        driverFactory.drivers[key]=new_driver[key]
        
    @staticmethod
    def get_driver_values():
        return driverFactory.drivers