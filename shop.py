from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, Text
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'created_at': self.created_at.isoformat()
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_email: Mapped[str] = mapped_column(String(120), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_email': self.customer_email,
            'customer_name': self.customer_name,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

# Routes
@app.route('/test')
def test():
    return jsonify({"message": "Shop test endpoint working!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

# Product routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Name and price are required'}), 400
    
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=float(data['price']),
        stock=int(data.get('stock', 0))
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201

# Order routes
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    required_fields = ['customer_email', 'customer_name', 'total_amount']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Customer email, name, and total amount are required'}), 400
    
    order = Order(
        customer_email=data['customer_email'],
        customer_name=data['customer_name'],
        total_amount=float(data['total_amount']),
        status=data.get('status', 'pending')
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify(order.to_dict()), 201

@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    order.status = data['status']
    db.session.commit()
    
    return jsonify(order.to_dict())

# Initialize database
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    
    # Add some sample products if none exist
    if Product.query.count() == 0:
        sample_products = [
            Product(name="T-Shirt", description="Comfortable cotton t-shirt", price=19.99, stock=50),
            Product(name="Mug", description="Coffee mug with logo", price=9.99, stock=25),
            Product(name="Sticker Pack", description="Pack of 5 vinyl stickers", price=4.99, stock=100)
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()
        print("Sample products added to database")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    # Run in development mode
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)