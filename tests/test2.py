from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BrowserStack credentials
bs_username = "your_browserstack_username"
bs_access_key = "your_browserstack_access_key"

# BrowserStack URL
bs_url = "https://"+bs_username+":"+bs_access_key+"@hub-cloud.browserstack.com/wd/hub"

# Desired capabilities for BrowserStack
desired_cap = {
    'os' : 'Windows',
    'os_version' : '10',
    'browser' : 'Chrome',
    'browser_version' : '80',
    'name' : "Flipkart.com test"
}

# Initialize WebDriver
driver = webdriver.Remote(
    command_executor=bs_url,
    desired_capabilities=desired_cap
)

# Load Flipkart home page
driver.get("https://www.flipkart.com")

# Search for the product
search_box = driver.find_element_by_name("q")
search_box.send_keys("Samsung Galaxy S10")
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "_2kHMtA"))
)

# Click on "Mobiles" in categories
driver.find_element_by_link_text("Mobiles").click()

# Apply filters
driver.find_element_by_xpath("//div[text()='Samsung']").click()
driver.find_element_by_xpath("//div[text()='Flipkart Assured']").click()

# Sort the entries
driver.find_element_by_xpath("//div[text()='Price -- High to Low']").click()

# Read the set of results that show up on page 1
product_elements = driver.find_elements_by_class_name("_2kHMtA")
products = []

for product_element in product_elements:
    product_name = product_element.find_element_by_class_name("_4rR01T").text
    display_price = product_element.find_element_by_class_name("_30jeq3._1_WHN1").text
    product_link = product_element.find_element_by_tag_name("a").get_attribute("href")

    product = {
        "Product Name": product_name,
        "Display Price": display_price,
        "Link to Product Details Page": product_link
    }

    products.append(product)

# Print the list of products
for product in products:
    print(product)

# Close the WebDriver
driver.quit()
