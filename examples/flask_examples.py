from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token

from python_errors.secure_flask import secure_endpoint
from python_errors.config import setup_security
from dotenv import load_dotenv

import os


load_dotenv()

app = Flask(__name__)
setup_security(app=app, delete_logs_on_start=True, rate_limit=True, jwt_secret_key=os.getenv("JWT_TOKEN"))


@app.route("/process-dict", methods=["POST"])
@secure_endpoint(method="POST", required_type='dict[str: dict[str: str]]')
def process_dict():
    """
    Endpoint to process a dictionary received as JSON input.
    """
    input_data = request.get_json()

    # Return the processed dictionary
    return jsonify({"data": input_data}), 200


@app.route('/example-get', methods=['GET'])
@secure_endpoint(method="GET", required_type="dict[str: str]", rate_limit="1/second")
def example_get():
    # Access validated input data
    input_data = request.args.to_dict(flat=True)
    return jsonify({"message": "Success", "data": input_data}), 200


@app.route('/secure-data', methods=['GET'])
@secure_endpoint(method="GET", require_jwt=True)
def secure_data():
    return jsonify({"message": "This is a secure endpoint!"}), 200


@app.route('/login', methods=["POST"])
@secure_endpoint(method="POST")
def login():
    # Generate a JWT token
    access_token = create_access_token(identity="123")
    return jsonify({"token": access_token}), 200



if __name__ == "__main__":
    app.run(debug=True)
