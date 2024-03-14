import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability('sessionName', 'BStack Sample Test')
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.flipkart.com")

    # Search for the product
    search_box = driver.find_element("name", "q")
    search_box.send_keys("Samsung Galaxy S10")
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_2kHMtA"))
    )

    driver.find_element("link text", "Mobiles").click()

    samsung_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/section[3]/div[2]/div/div/div/label"))
    )
    samsung_filter.click()

    flip_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/section[4]/label/div[2]/div/img"))
    )
    flip_filter.click()


    highlow_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div[3]/div[4]"))
    )
    highlow_filter.click()
    # driver.find_element("xpath", "//div[text()='Price -- High to Low']").click()


    driver.implicitly_wait(5)
    product_elements = driver.find_elements(By.CLASS_NAME, "_2kHMtA")
    products = []

    for product_element in product_elements:
        product_name = product_element.find_element(By.CLASS_NAME, "_4rR01T").text
        display_price = product_element.find_element(By.CLASS_NAME, "_30jeq3._1_WHN1").text
        product_link = product_element.find_element(By.TAG_NAME, "a").get_attribute("href")

        product = {
            "Product Name": product_name,
            "Display Price": display_price,
            "Link to Product Details Page": product_link
        }

        products.append(product)

    # Print the list of products
    for product in products:
        print(product)
except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()
