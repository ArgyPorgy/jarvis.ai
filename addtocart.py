from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def add_to_wishlist(product):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Add this line to bypass bot detection
    chrome_options.add_argument("webdriver.chrome.driver=C:\\test-corpusX\\chromedriver.exe")  # Specify the path to chromedriver.exe

    web = webdriver.Chrome(options=chrome_options)
    web.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Farcus-www.amazon.in%2Fgp%2Fcss%2Fhomepage.html%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
    time.sleep(1)

    # cookies_accept_button = WebDriverWait(web, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[@id='sp-cc-accept']"))
    # )
    # cookies_accept_button.clic

    login = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))
    )
    login.send_keys("7602101368")

    submit = WebDriverWait(web, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='continue']"))
    )
    submit.click()

    password = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
    )
    password.send_keys("Arghya1234")

    sign_in_button = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='signInSubmit']"))
    )
    sign_in_button.click()

    # top_picks = WebDriverWait(web, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//h2[@class='a-size-large a-spacing-base' and text()='Top picks for you']"))
    # )
    # top_picks.click()

    search_input = WebDriverWait(web, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='nav-search-keywords' or @id='twotabsearchtextbox']"))
    )
    search_input.send_keys(product)

    go = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Go']"))
    )
    go.click()
    # time.sleep(50) 

    products = WebDriverWait(web, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 's-image'))
    )

    # Click on the first product
    if products:
        first_product = products[1]
        first_product.click()
    else:
        print("No products found with the specified class.")

    web.switch_to.window(web.window_handles[1])   
    # time.sleep(50) 

    add_to_cart_button = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="add-to-wishlist-button-submit" and @name="submit.add-to-registry.wishlist"]'))
    )

    # web.execute_script("document.documentElement.scrollTop = 10000;")

    if add_to_cart_button:
        add_to_cart_button.click()
        print("Add to Cart button clicked successfully.")
        time.sleep(5)
    else:
        print("Timeout waiting for Add to Cart button.")

    # Close the webdriver
    web.quit()

# Call the function

