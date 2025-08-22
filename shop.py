from flask import Flask, jsonify
import os

app = Flask(__name__)

# API routes
@app.route('/api/products')
def api_products():
    return jsonify([{"id": 1, "name": "Product 1", "price": 10.99}])

@app.route('/api/cart', methods=['GET', 'POST'])
def api_cart():
    return jsonify({"items": []})

# Shop pages
@app.route('/shop')
def shop():
    return "Shop page - use your template here"

@app.route('/shop/product/<id>')
def product_detail(id):
    return f"Product {id} detail page"

@app.route('/cart')
def cart():
    return "Shopping cart page"

@app.route('/checkout')
def checkout():
    return "Checkout page"

# Health check
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Shop API running on port {port}")
    app.run(host='0.0.0.0', port=port)