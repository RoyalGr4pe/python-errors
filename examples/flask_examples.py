from flask import Flask, jsonify, request

from python_errors.secure_flask import secure_post_endpoint
from python_errors.config import setup_errors

setup_errors(delete_logs_on_start=True)

app = Flask(__name__)

@app.route("/process-dict", methods=["POST"])
@secure_post_endpoint(required_type='dict[str: dict[str: str]]')
def process_dict():
    """
    Endpoint to process a dictionary received as JSON input.
    """
    input_data = request.get_json()  # No need to validate, it's handled by the decorator

    # Return the processed dictionary
    return jsonify({"processed_data": input_data}), 200


if __name__ == "__main__":
    app.run(debug=True)
