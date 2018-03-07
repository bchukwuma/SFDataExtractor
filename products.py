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

    def __init__(self, pid, name, sku, url, imgSrc, category, description):
        self.pid = pid
        self.name = name
        self.sku = sku
        self.url = url
        self.imgSrc = imgSrc
        self.category = category
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
    # url = "https://burlesquedesign.com/collections/posters-prints"
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,"html.parser")
        products = []
        targetString = ["product_box_wrapper ", "product_box_wrapper last_product_wrapper"]
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
        name = ''
        price = ''
        description = ''
        pid = 'N/A'
        category = 'N/A'
        sku = 'N/A'

        # pid, name, sku = parse_product_details()
        # parsing title as name, name value is loaded via js after source is returned
        title = html.find("meta",  property="og:title")["content"]
        imgSrc = html.find("meta",  property="og:image")["content"]
        description = html.find("meta",  property="og:description")["content"]
        #var meta = {"product":{"id":412357787679,"vendor":"Burlesque of North America","type":"Posters \/ Prints","variants":[{"id":5339864924191,"price":3000,"name":"Tools of the Trade: Video Game Edition Variant","public_title":null,"sku":"Tools_VideoGame_VARIANT"}]},"page":{"pageType":"product","resourceType":"product","resourceId":412357787679}};


        metaVarsString = html.find_all(text='var meta')

        relatedProducts = get_related_products(html, ["product_box_wrapper ", "product_box_wrapper last_product_wrapper"])        
        productDetails = ProductDetails(pid, title, sku, productURL, imgSrc, category, description)

        return productDetails, seoKeywords, relatedProducts


def get_related_products(html, targetString):
    relatedProducts = []
    appendLast = ''
    for index, stringVal in enumerate(targetString):
        if (index > 0):
            appendLast = "coll_product_box_last"
        for div1 in html.find_all(attrs={"id" : "related-products"}):
            for div2 in div1.find_all("div", targetString[index]):
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


def get_meta_vars():
    url = "https://burlesquedesign.com/collections/posters-prints"
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,"html.parser")
        
        searchString = html.head.prettify(formatter="xml")

        print(searchString)            

if __name__ == '__main__':    
    get_meta_vars()