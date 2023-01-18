import requests
import csv

# shutil is part of python3 base libs
import shutil

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

    with open(csv_path, 'a') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(data.values())

def download_book_images(book_url, csv_path):
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_source =  soup.find("div",{"id":"product_gallery"}).findChildren("img")[0]["src"][6:]
    file_name = image_source.split("/")[-1]
    image_url = "http://books.toscrape.com/" + image_source
    res = requests.get(image_url, stream = True)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')
    

def fetch_category(category):
    # By default this website use index.html as a page name and then uses page-N.html
    pagination = "index.html"
    base_url = "http://books.toscrape.com/catalogue/category/books/"
    url = base_url + category + "/" + pagination
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    catalogue_url = "https://books.toscrape.com/catalogue/"
    csv_path = "./data/" + category + ".csv"

    write_csv_headers(csv_path)

    number_of_books = int(soup.find("form",{"class":"form-horizontal"}).findChildren("strong")[0].string)
    number_of_pages = int(number_of_books / 20) + 1
    if number_of_books <= 20:
        pages = ["index.html"]
    else:
        pages = []
        for i in range(number_of_pages):
            pages.append("page-" + str(i+1) + ".html")

    for pagination in pages:
        base_url = "http://books.toscrape.com/catalogue/category/books/"
        url = base_url + category + "/" + pagination
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        books = soup.findAll("article", {"class":"product_pod"})
        for book in books:
            book_ref = book.findChildren("h3")[0].findChildren("a")[0]["href"][9:]
            book_url = catalogue_url + book_ref
            scrape_book(book_url, csv_path)
            download_book_images(book_url, csv_path)

def fetch_categories():
    url = "http://books.toscrape.com"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # The first "a" element is the link to base page so we get rid of it with [1:]
    categories = soup.find("div", {"class":"side_categories"}).findChild("ul").findChildren("a")[1:]

    for category in categories:
        category_name = category["href"].split("/")[3]
        fetch_category(category_name)


fetch_categories()
