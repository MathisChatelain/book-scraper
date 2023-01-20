import requests
import csv
import shutil
import os

from bs4 import BeautifulSoup

class BookScraper:


    def fetch_categories(self):
        soup = BeautifulSoup(requests.get("http://books.toscrape.com").content, 'html.parser')

        # [1:] filters out the link to home page 
        links_to_categories = soup.find("div", {"class":"side_categories"}).findChild("ul").findChildren("a")[1:]

        for link in links_to_categories:
            category_name = link["href"].split("/")[3]
            self.fetch_category(category_name)

    def fetch_category(self, category):
        base_url = "http://books.toscrape.com/catalogue/category/books/"
        catalogue_url = "https://books.toscrape.com/catalogue/"

        path = f"./data/{category}/"
        csv_path = f"./data/{category}/{category}_data.csv"
        os.makedirs(path)
        self.write_csv_headers(csv_path)

        category_url = f"{base_url}{category}/index.html"
        soup = BeautifulSoup(requests.get(category_url).content, 'html.parser')

        for pagination in self.get_category_pages(soup):
            url = f"{base_url}{category}/{pagination}"
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')

            for book in soup.findAll("article", {"class":"product_pod"}):
                book_url = f"{catalogue_url}{book.findChildren('h3')[0].findChildren('a')[0]['href'][9:]}"
                self.scrape_book(book_url, csv_path)
                self.download_book_image(book_url, path)

    def write_csv_headers(self, csv_path):
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

    def get_category_pages(self, soup):
        number_of_books = int(soup.find("form",{"class":"form-horizontal"}).findChildren("strong")[0].string)
        number_of_pages = int(number_of_books / 20)
        pages = ["index.html"]
        for i in range(number_of_pages):
            pages.append(f"page-{str(i+2)}.html")
        return pages

    def scrape_book(self, book_url, csv_path):
        book_soup = BeautifulSoup(requests.get(book_url).content, 'html.parser')

        data = {
            "product_page_url": book_url,
            "universal_product_code": self.get_product_data(book_soup, "UPC"),
            "title": book_soup.find("div",{"class":"product_main"}).findNext("h1").contents[0],
            "price_including_tax": self.get_product_data(book_soup, "Price (incl. tax)"),
            "price_excluding_tax": self.get_product_data(book_soup, "Price (excl. tax)"),
            "number_available": self.get_product_data(book_soup, "Availability"),
            "product_description": book_soup.find("div",{"id":"product_description"}).findNext("p").contents[0],
            "category": book_soup.find_all("ul",{"class":"breadcrumb"})[0].findChildren("a")[2].string,
            "review_rating": book_soup.find("p",{"class":"star-rating"})["class"][1],
            "image_url": f"http://books.toscrape.com/{book_soup.find('div',{'id':'product_gallery'}).findChildren('img')[0]['src'][6:]}"
        }

        with open(csv_path, 'a') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(data.values())

    def get_product_data(self, soup, name):
        return soup.find("th",text=name).findNext('td').contents[0]

    def download_book_image(self, book_url, path):
        soup = BeautifulSoup(requests.get(book_url).content, 'html.parser')
        
        image_source =  soup.find("div",{"id":"product_gallery"}).findChildren("img")[0]["src"][6:]
        image_url = f"http://books.toscrape.com/{image_source}"
        res = requests.get(image_url, stream = True)

        file_name = image_source.split("/")[-1]
        
        if res.status_code == 200:
            with open(f"{path}{file_name}",'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print("Image sucessfully Downloaded: ",file_name)
        else:
            print("Image Couldn't be retrieved")

    

   

    