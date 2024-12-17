# Clicks 'Menu' then 'Add to Cart' 'Back to Menu' then 'Home'
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
        time.sleep(1)
        # find 'About' and click it
        driver.find_element(By.XPATH, "//a[contains(., 'Menu')]").click()
        time.sleep(1)
        # find 'Add to Cart' and click it
        driver.find_element(By.XPATH, "//a[contains(., 'Add to Cart')]").click()
        time.sleep(1)
        # find 'Back to Menu' and click it
        driver.find_element(By.XPATH, "//a[contains(., 'Back to Menu')]").click()
        time.sleep(1)
        # find 'Home' and click it
        driver.find_element(By.XPATH, "//a[contains(., 'Home')]").click()

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

