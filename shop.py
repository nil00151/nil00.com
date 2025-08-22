from flask import Flask
import os

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello World! Shop is running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/shop')
def shop():
    return "Welcome to the shop!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask shop on port {port}")
    app.run(host='0.0.0.0', port=port)