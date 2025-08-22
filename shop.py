from flask import Flask
import os
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Get database path from environment or use default
database_path = os.environ.get('DATABASE_PATH', '/var/lib/shop/data/shop.db')

# Ensure database directory exists
db_dir = os.path.dirname(database_path)
Path(db_dir).mkdir(parents=True, exist_ok=True)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # Use port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)