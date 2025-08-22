from flask import Flask
import os
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Get database path from environment or use default
database_path = os.environ.get('DATABASE_PATH', '/var/lib/private/shop/data/shop.db')

# Ensure database directory exists (with error handling)
try:
    db_dir = os.path.dirname(database_path)
    Path(db_dir).mkdir(parents=True, exist_ok=True)
    print(f"Database directory ensured: {db_dir}")
except Exception as e:
    print(f"Error creating database directory: {e}")
    # Fallback to a writable location
    database_path = '/tmp/shop.db'
    print(f"Using fallback database path: {database_path}")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set instance path from environment or use default
instance_path = os.environ.get('FLASK_INSTANCE_PATH', '/tmp/instance')
app.instance_path = instance_path
print(f"Using instance path: {instance_path}")

# Initialize SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    print(f"Database: {database_path}")
    print(f"Instance path: {instance_path}")
    app.run(host='0.0.0.0', port=port)