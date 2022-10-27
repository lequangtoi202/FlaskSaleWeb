from flask import render_template, request

from saleapp import app, dao


@app.route("/")
def index():
    categories = dao.load_categories()
    products = dao.load_products(category_id=request.args.get('category_id'), kw=request.args.get('kw'))
    return render_template("index.html", categories=categories, products=products)


@app.route('/products/<int:product_id>')
def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template("details.html", product=p)


if __name__ == '__main__':
    app.run(debug=True)

