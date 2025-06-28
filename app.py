from flask import Flask
import os
from flask_cors import CORS
from routes.nft_routes import nft_routes

app = Flask(__name__)

CORS(app, origins="*")


app.register_blueprint(nft_routes)

if __name__ == "__main__":
    print("🚀 Flask API running at http://localhost:5000")
    app.run(debug=True)
