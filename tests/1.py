# Clicks 'All Authors' then 'Agatha Christie' then 'The Mysterious Affair at Styles'
# application

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):

        driver = self.driver
        driver.maximize_window()
        user = "testuser2"
        pwd = "test123"
        driver.get("http://127.0.0.1:8000/admin")
        time.sleep(3)
        elem = driver.find_element(By.ID,"id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID,"id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)
        # find 'All Authors' and click it – note this is all one Python statement
        driver.find_element(By.XPATH, "//a[contains(., 'All Authors')]").click()
        # find 'Agatha Christie' and click it – note this is all one Python statement
        driver.find_element(By.XPATH, "//a[contains(., 'Agatha Christie')]").click()
        # find 'The Mysterious Affair at Styles' and click it – note this is all one Python statement
        driver.find_element(By.XPATH, "//a[contains(., 'The Mysterious Affair at Styles')]").click()

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

