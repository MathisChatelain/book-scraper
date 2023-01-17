import requests
import csv
from bs4 import BeautifulSoup

def write_csv_headers(csv_path):
    headers = [
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
    with open(csv_path, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(headers)

def get_product_data(fsoup,name):
    return fsoup.find("th",text=name).findNext('td').contents[0]

def scrape_book(book_url, csv_path):
    book_page = requests.get(book_url)
    book_soup = BeautifulSoup(book_page.content, 'html.parser')

    # using dicts here add readability
    data = {
        "product_page_url": book_url,
        "universal_product_code": get_product_data(book_soup, "UPC"),
        "title": book_soup.find("div",{"class":"product_main"}).findNext("h1").contents[0],
        "price_including_tax": get_product_data(book_soup, "Price (incl. tax)"),
        "price_excluding_tax": get_product_data(book_soup, "Price (excl. tax)"),
        "number_available": get_product_data(book_soup, "Availability"),
        "product_description": book_soup.find("div",{"id":"product_description"}).findNext("p").contents[0],
        "category": book_soup.find_all("ul",{"class":"breadcrumb"})[0].findChildren("a")[2].string,
        "review_rating": book_soup.find("p",{"class":"star-rating"})["class"][1],
        "image_url": "http://books.toscrape.com/" + book_soup.find("div",{"id":"product_gallery"}).findChildren("img")[0]["src"][6:]
    }
    # changed csv open mode from write to append in phase 2
    with open(csv_path, 'a') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        # we use our dict keys as headers and our values as data and initialise headers if the csv is empty
        writer.writerow(data.values())


category = "historical-fiction_4"
# By default this website use index.html as a page name and then uses page-N.html
page = "index.html"
base_url = "http://books.toscrape.com/catalogue/category/books/"
url = base_url + category + "/" + page
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
phase_2_csv_path = '../Chatelain_Mathis_2_data_images_012023/phase_2_data.csv'
catalogue_url = "https://books.toscrape.com/catalogue/"

write_csv_headers(phase_2_csv_path)

books = soup.findAll("article", {"class":"product_pod"})
for book in books:
    book_ref = book.findChildren("h3")[0].findChildren("a")[0]["href"][9:]
    book_url = catalogue_url + book_ref
    scrape_book(book_url, phase_2_csv_path)
