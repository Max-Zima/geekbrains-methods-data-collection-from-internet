from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='.\chromedriver.exe',
                          options=chrome_options)

driver.get("https://mvideo.ru/")

popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-popup__block')))
action = webdriver.common.action_chains.ActionChains(driver)

action.move_to_element_with_offset(driver.find_element_by_xpath('//a[@class="header-main__logo"]'), 0, 0)
action.click()
action.perform()

novinki = driver.find_element_by_xpath('//ul[contains(@data-init-param, "Новинки")]')
driver.execute_script("arguments[0].scrollIntoView();", novinki)
time.sleep(2)

while True:
    next = driver.find_elements_by_xpath(
        "//ul[contains(@data-init-param, 'Новинки')]/../../a[@class='next-btn c-btn c-btn_scroll-horizontal "
        "c-btn_icon i-icon-fl-arrow-right']")
    if len(next) == 0:
        break
    next[0].click()
    time.sleep(8)

products = driver.find_elements_by_xpath('//ul[contains(@data-init-param, "Новинки")]//a[contains(@class, "fl-product-tile-picture")]')
print(len(products))
print('products: ', products)
