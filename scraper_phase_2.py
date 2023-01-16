import requests
import csv
from bs4 import BeautifulSoup

# Phase 2

category = "historical-fiction_4"
# By default this website use index.html as a page name and then uses page-N.html
page = "index.html"
base_url = "http://books.toscrape.com/catalogue/category/books/"
url = base_url + category + "/" + page
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
phase_2_csv_path = '../Chatelain_Mathis_2_data_images_012023/phase_2_data.csv'

def get_product_data(name):
    return soup.find("th",text=name).findNext('td').contents[0]

def scrape_book(book_url, csv_path):
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # using dicts here add readability
    data = {
        "product_page_url": book_url,
        "universal_product_code": get_product_data("UPC"),
        "title": soup.find("div",{"class":"product_main"}).findNext("h1").contents[0],
        "price_including_tax": get_product_data("Price (incl. tax)"),
        "price_excluding_tax": get_product_data("Price (excl. tax)"),
        "number_available": get_product_data("Availability"),
        "product_description": soup.find("div",{"id":"product_description"}).findNext("p").contents[0],
        "category": soup.find_all("ul",{"class":"breadcrumb"})[0].findChildren("a")[2].string,
        "review_rating": soup.find("p",{"class":"star-rating"})["class"][1],
        "image_url": "http://books.toscrape.com/" + soup.find("div",{"id":"product_gallery"}).findChildren("img")[0]["src"][6:]
    }

    with open(csv_path, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        # we use our dict keys as headers and our values as data
        # TODO change this to allow multiple lines
        writer.writerow(data.keys())
        writer.writerow(data.values())
