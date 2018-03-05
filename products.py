from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json

class Product(object):

    def __init__(self, url, imgSrc, title, price):
        self.url = url
        self.imgSrc = imgSrc
        self.title = title
        self.price = price
    
    def jsonify(self):
        return json.dumps(vars(self), sort_keys=False, indent=2, separators=(',', ': '))

class ProductDetails(object):

    def __init__(self, url, imgSrc, title, description):
        self.url = url
        self.imgSrc = imgSrc
        self.title = title
        self.description = description
        self.sizeDetails = []

    def addSizeDetails(self, size, price):
        self.sizeDetails.append(size, price);

    def jsonify(self):
        return json.dumps(vars(self), sort_keys=False, indent=2, separators=(',', ': '))

class ProductSizeDetail(object):
    def __init__(self, size, price ):
        self.size = size
        self.price = price
    
    def jsonify(self):
        return json.dumps(vars(self), sort_keys=False, indent=2, separators=(',', ': '))


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of html/xml, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url,stream=True)) as resp:

            if ( is_good_response(resp) ):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be html, false otherwise
    """
    content_type = resp.headers['Content-Type']
    return (resp.status_code == 200
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def build_product():
    newProduct = Product('www.car.com', 'www.car.com/car.jpg', 'Mustang', '$80')
    print(newProduct.url, newProduct.imgSrc, newProduct.title, newProduct.price)
    productList = []

    productList.append(newProduct)
    print(productList)
    return productList

def get_products(url):
    if '/collections/' not in url:
        raise Exception('Category Lookup failure. Bad URL..') 
    # url = "https://burlesquedesign.com/collections/posters-prints"
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,"html.parser")
        products = []

        seoFind = html.findAll("meta",  attrs={'name':'keywords'})
        seoKeywords = seoFind[0]["content"]
        
        for div in html.find_all("div", class_=["product_box_wrapper ", "coll_product_box_last"]):
            
            for a in div.find_all('a'):
                if '/products' in a['href']:
                    productURL = 'https://burlesquedesign.com{}'.format(a['href'])

            for li in div.find_all('li', class_="coll_product_box "):
                for img in li.find_all('img'):
                    imgSrc = img['src']

                for spanTitle in li.find_all('span', class_="coll_product_details_title"):
                    title = spanTitle.text

                for spanMoney in li.find_all('span', class_="money"):
                    price = spanMoney.text
            product = Product(productURL, imgSrc, title, price)
            products.append(product)
        return products, seoKeywords

def get_product(url):
    if '/products/' not in url:
        raise Exception('Product Lookup failure. Bad URL..') 
    # url = "https://burlesquedesign.com/collections/posters-prints"
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,"html.parser")
        relatedProducts = []
        seoFind = html.findAll("meta",  attrs={'name':'keywords'})
        seoKeywords = seoFind[0]["content"]

        productURL = url
        imgSrc = ''
        title = ''
        price = ''
        description = ''

        title = html.find("meta",  property="og:title")["content"]
        imgSrc = html.find("meta",  property="og:image")["content"]
        description = html.find("meta",  property="og:description")["content"]

        productDetails = ProductDetails(productURL, imgSrc, title, description)
        print(vars(productDetails))

        # for div in html.find_all("div", class_=["product_details_container"]):            
            # for i, li in enumerate(div.find_all('li', class_="custom_option")):
            #     productDetails.addSizeDetails(li.innerHtml, li["data-price"])
            #     print(li["contents"], li["data-price"])
        return productDetails, seoKeywords

if __name__ == '__main__':    
    get_products("https://burlesquedesign.com/collections/posters-prints")