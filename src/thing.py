from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Runs Chrome in headless mode.
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

# Set path to chromedriver if not in PATH

BASE_URL = "https://www.amazon.co.uk/"
suffixes = ["DJI-Vlogging-Stabilization-Tracking-Photography/dp/B0CG19FGQ5/", "DJI-Standard-Waterproof-Stabilization-Touchscreens/dp/B07FW4CZZL/", "JYJZPB-EN-EL14-EN-EL14A-Battery-Charger/dp/B0CQZPQJ2R", "Movo-VXR10-Universal-Shotgun-Camera-Black/dp/B0723D3FVL", "Apple-iPad-11-inch-Display-All-Day/dp/B0DZ77X9FQ", "SanDisk-128GB-Extreme-RescuePRO-Deluxe/dp/B09X7FXHVJ"]
products = []

def obtain_info(link):
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    title_tag = soup.find('span', id='productTitle')
    price_tag = soup.find('span', class_='aok-offscreen')
    img_tag = soup.find('div', id='imgTagWrapperId').find('img')

    if title_tag:
        product_title = title_tag.get_text(strip=True)
        print("Product Title:", product_title)
    else:
        print("Product title not found.")

    if price_tag:
        price = price_tag.get_text(strip=True)
        print("Price:", price)
    else:
        print("Price not found.")

    img_src = img_tag.get('src')
    driver.quit()

    create_product(product_title, img_src, price, link)

def create_product(title, image, price, link):
    product = {
        "title": title,
        "image": image,
        "price": price[1:],
        "link": link
    }

    products.append(product)

for suffix in suffixes:
    url = BASE_URL + suffix 
    obtain_info(url)

json_output = json.dumps(products, indent=2)
with open("/Users/dmd/Scripts/output/products.json", "w") as f:
    f.write(json_output)
