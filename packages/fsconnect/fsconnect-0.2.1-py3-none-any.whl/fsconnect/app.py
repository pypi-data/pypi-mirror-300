from flask import Flask
from fsconnect.api import api_blueprint

app = Flask(__name__)

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def index():
    return "Welcome to the FSConnect API!"

if __name__ == '__main__':
    app.run(debug=True)
