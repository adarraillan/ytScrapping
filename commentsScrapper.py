

import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def commentToto():
    with Chrome() as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.youtube.com/watch?v=kffacxfA7G4")

        for item in range(1): #by increasing the highest range you can get more content
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            print(comment.text)

