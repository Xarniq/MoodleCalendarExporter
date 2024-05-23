"""
Author : Xarnia
Last Modified : 18/05/2024
Project : MoodleCalendarExporter
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time 
from MoodleErrors import *

import os

def wait_for_download(download_dir, timeout=30):
    """
    Wait until a file appears in the download directory or timeout is reached.
    
    Args:
        download_dir (str): The directory to monitor for file downloads.
        timeout (int): The maximum time to wait for the file to appear, in seconds.
    
    Returns:
        bool: True if the file appears before the timeout, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if any(filename.endswith('.ics') for filename in os.listdir(download_dir)):
            return True
        time.sleep(1)
    return False

class Moodle:
    
    def __init__(self,username,password,url,downloadpath):
        """
        Initialise credentials for login.

        Args:
            username (str): username
            password (str): password
            url (str) : url
            downloadpath (str) : downloadpath
        """
        self.username = username
        self.password = password
        self.url = url
        self.downloadpath = downloadpath
    
    def Login(self):
        """
        Method which logs yourself to Moodle.
        """
        url = self.url
        self.driver.get(url)
        try:
            user = self.driver.find_element(By.XPATH, '//*[@id="username"]')
            user.clear()
            user.send_keys(self.username)
            passw = self.driver.find_element(By.XPATH,'//*[@id="password"]')
            passw.clear()
            passw.send_keys(self.password)
            button = self.driver.find_element(By.XPATH,'//*[@id="loginbtn"]')
            button.click()
            print("Login Successful!")
        except LoginError as le:
            print("An error occurred during login:", le)
        except Exception as e:
            # Handle other type of exceptions
            print("An unexpected error occurred:", e)
        
    
    def GetCalendar(self):
        """
        Method which will gather the .ics.
        """
        try:
            export = self.driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/div/div[2]/div/section/div/aside/section[3]/div/div/div[2]/div/span[2]/a') 
            time.sleep(2)
            export.click()
            self.driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/section/div/div[1]/div[2]/form').click() 
            time.sleep(2)
            self.driver.find_element(By.XPATH,'//*[@id="id_events_exportevents_all"]').click() # Choosing options
            self.driver.find_element(By.XPATH,'//*[@id="id_period_timeperiod_monthnow"]').click() 
            self.driver.find_element(By.XPATH,'//*[@id="id_export"]').click() # Downloads the .ics
            if wait_for_download(self.downloadpath):
                print("Download started successfully.")
            else:
                raise CalendarNotRetrieved("Failed to retrieve calendar data.")
        except CalendarNotRetrieved as cnr:
            print("An error occurred while retrieving the calendar:", cnr)
        except Exception as e:
            # Gérer d'autres exceptions non prévues
            print("An unexpected error occurred:", e)
        finally:
            self.driver.quit()

    def Main(self):
        """
        Starts the program.
        """
        options = Options()
        options.add_argument("-headless")
        self.driver = webdriver.Firefox(options=options)
        self.Login()
        self.GetCalendar()
        time.sleep(10)
        self.driver.close()
    
sesh = Moodle("username","password","https://YourMoodle","C:/your/path/")
sesh.Main()


