import requests
import csv
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
csv_headers = [
    "product_page_url", 
    "universal_product_code", 
    "title", 
    "price_including_tax", 
    "price_excluding_tax", 
    "number_available", 
    "product_description", 
    "category", 
    "review_rating", 
    "image_url"
    ]

def get_product_data(name):
    return soup.find("th",text=name).findNext('td').contents[0]

product_page_url = url 
universal_product_code = get_product_data("UPC")
title = soup.find("div",{"class":"product_main"}).findNext("h1").contents[0]
price_including_tax = get_product_data("Price (incl. tax)") 
price_excluding_tax = get_product_data("Price (excl. tax)") 
number_available = get_product_data("Availability") 
product_description = soup.find("div",{"id":"product_description"}).findNext("p").contents[0]
category = soup.find_all("ul",{"class":"breadcrumb"})[0].findChildren("a")[2].string
review_rating = soup.find("p",{"class":"star-rating"})["class"][1]

# Image url is cached on the site we concatenate page image url to the website images base location
image_url = "http://books.toscrape.com/" + soup.find("div",{"id":"product_gallery"}).findChildren("img")[0]["src"][6:]


with open('../Chatelain_Mathis_2_data_images_012023/phase_1_data.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(csv_headers)
    ligne = [
        product_page_url, 
        universal_product_code, 
        title,
        price_including_tax,
        price_excluding_tax,
        number_available, 
        product_description, 
        category,
        review_rating,
        image_url
        ]
    writer.writerow(ligne)
