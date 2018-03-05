from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from  products import get_products
from  products import get_product
import json

app = Flask(__name__)

Bootstrap(app)
# @ signifies a decorator - way to wrap a function and modifying its behavior

@app.route('/')
def index():
    return render_template("home.html")

@app.route("/extract", methods=['POST'])
def extract():
    url=request.form['url']
    if 'burlesquedesign.com/' in url:
        if 'collections/' in url:
            productsList, seo = get_products(url)
            sliceVal = len('collections/') 
            category = url[url.index('collections/')+sliceVal:]
            return render_template("category.html", category=category, productsList=productsList, url=url, seo=seo)
        elif 'products/' in url:
            productDetails, seo = get_product(url)
            return render_template("product.html", productDetails=productDetails, url=url, seo=seo)
        else:
            return render_template("error.html")
    else:
            return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)