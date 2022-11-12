import os
from bs4 import BeautifulSoup
import pandas as pandas
import requests

ZILLOW_LINK = os.environ.get("ZILLOW_LINK")

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

response = requests.get(ZILLOW_LINK, headers=headers)
response.raise_for_status()

map_page = response.text

soup = BeautifulSoup(map_page, "html.parser")

property_address_elements = soup.select("div.property-card-data address", attr={"data-test": "property-card-addr"})
property_addresses = [element.getText().split("|")[1].strip() for element in property_address_elements]

property_link_elements = soup.select("div.property-card-data a", attrs={"data-test": "property-card-link"})
property_links = [element["href"] for element in property_link_elements]

property_price_elements = soup.find_all(name="span", attrs={"data-test": "property-card-price"})
property_prices = [element.getText().split("+")[0] for element in property_price_elements]

df = pandas.DataFrame({"address": property_addresses, "price": property_prices, "link": property_links})
df.to_csv("properties.csv", index=False)
