from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from contextlib import closing
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

    def __init__(self, pid, name, price, url, imgSrc, category, description):
        self.pid = pid
        self.name = name
        self.price = price
        self.url = url
        self.imgSrc = imgSrc
        self.category = category
        self.description = description
        self.variantDetails = []

    def addVariantDetails(self, vid, variant, price):
        keys = ['vid', 'variant', 'price']
        values = [vid, variant, price]
        self.variantDetails.append(dict(zip(keys, values)));
        

    def get_default_variantDetails(self):
        if (self.variantDetails[0] is None):
            keys = ['vid', 'variant', 'price']
            values = ["n/a$", "n/a$", "n/a$"]
            self.variantDetails.append(zip(keys, values));            
            return  self.variantDetails[0]
        else:
            return  self.variantDetails[0]

    def jsonify(self):
        return json.dumps(vars(self), sort_keys=False, indent=2, separators=(',', ': '))


def simple_get(url):
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
    content_type = resp.headers['Content-Type']
    return (resp.status_code == 200
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
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

    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,"html.parser")
        products = []
        appendLast = ''
        targetString = ["product_box_wrapper ", "product_box_wrapper last_product_wrapper"]
        seoFind = html.findAll("meta",  attrs={'name':'keywords'})
        seoKeywords = seoFind[0]["content"]

        for index, stringVal in enumerate(targetString):
            if (index > 0):
                appendLast = "coll_product_box_last"
            for div in html.find_all("div", stringVal):
                for a in div.find_all('a'):
                    if '/products' in a['href']:
                        productURL = 'https://burlesquedesign.com{}'.format(a['href'])

                for li in div.find_all('li', class_="coll_product_box {}".format(appendLast)):
                    for img in li.find_all('img'):
                        imgSrc = img['src']

                    for spanTitle in li.find_all('span', class_="coll_product_details_title"):
                        title = spanTitle.text

                    for spanMoney in li.find_all('span', class_="money"):
                        price = spanMoney.text
                product = Product(productURL, imgSrc, title, price)
                products.append(product)
        return products, seoKeywords
    else:
         raise Exception('Category Lookup failure. No response from URL..') 

def get_product(url):
    if '/products/' not in url:
        raise Exception('Product Lookup failure. Bad URL..') 

    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,"html.parser")
        relatedProducts = []
        seoFind = html.findAll("meta",  attrs={'name':'keywords'})
        seoKeywords = seoFind[0]["content"]

        productURL = url
        imgSrc = ''
        name = ''
        price = ''
        description = ''
        category = 'N/A'
        variantDetails = []

        title = html.find("meta",  property="og:title")["content"]
        imgSrc = html.find("meta",  property="og:image")["content"]
        description = html.find("meta",  property="og:description")["content"]

        productDetails = ProductDetails('', title, '', productURL, imgSrc, category, description)

        for div in html.find_all("div", class_="variant_dropdown"):
            for li in div.find_all('li', class_="custom_option"):
                if not productDetails.pid:
                    productDetails.pid = li["data-option"]
                if not productDetails.price:
                    productDetails.price = li["data-price"]
                productDetails.addVariantDetails( li["data-option"], li.contents[0].strip(), li['data-price'])

        relatedProducts = get_related_products(html, ["product_box_wrapper ", "product_box_wrapper last_product_wrapper"])
        return productDetails, seoKeywords, relatedProducts


def get_related_products(html, targetString):
    relatedProducts = []
    appendLast = ''
    for index, stringVal in enumerate(targetString):
        if (index > 0):
            appendLast = "coll_product_box_last"
        for div1 in html.find_all(attrs={"id" : "related-products"}):
            for div2 in div1.find_all("div", stringVal):
                relatedProductURL = ''
                relatedImgSrc = ''
                relatedTitle = ''
                relatedPrice = ''

                a =  div2.find('a')
                if '/products' in a['href']:
                    relatedProductURL = 'https://burlesquedesign.com{}'.format(a['href'])
            
                for li in div2.find_all('li', class_="coll_product_box {}".format(appendLast)):
                    for img in li.find_all('img'):
                        relatedImgSrc = img['src']

                    for spanTitle in li.find_all('span', class_="coll_product_details_title"):
                        relatedTitle = spanTitle.text

                    for spanMoney in li.find_all('span', class_="coll_product_details_price"):
                        relatedPrice = spanMoney.text
                product = Product(relatedProductURL, relatedImgSrc, relatedTitle, relatedPrice)
                relatedProducts.append(product)
    return relatedProducts