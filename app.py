from flask import Flask, request, jsonify  # Import necessary modules from Flask and requests libraries
import requests  # Import the requests library for making HTTP requests
import os  # Import the os module to access environment variables

# Initialize a Flask application
app = Flask(__name__)

# Retrieve the Lemon Squeezy API key from the environment variables
LEMON_SQUEEZY_API_KEY = os.getenv('LEMON_SQUEEZY_API_KEY')


# Function to validate the license key by checking its status through the Lemon Squeezy API
def validate_license_key(activation_key):
    headers = {
        'Authorization': f'Bearer {LEMON_SQUEEZY_API_KEY}',  # Set the Authorization header with the API key
        'Accept': 'application/json',  # Specify that the response should be in JSON format
    }
    # Send a GET request to the Lemon Squeezy API to check the status of the license key
    response = requests.get(f'https://api.lemonsqueezy.com/v1/licenses/{activation_key}', headers=headers)

    # If the request is successful (status code 200)
    if response.status_code == 200:
        license_data = response.json()  # Parse the JSON response
        # Return True if the license key status is 'active', otherwise return False
        return license_data['data']['attributes']['status'] == 'active'

    # Return False if the request failed (status code is not 200)
    return False


# Flask route to handle license key validation requests
@app.route('/validate', methods=['POST'])
def validate():
    # Check if the incoming request contains JSON data
    if not request.is_json:
        return jsonify({'valid': False, 'message': 'Request must be JSON'}), 400  # Return an error if not JSON

    data = request.get_json()  # Parse the incoming JSON data
    activation_key = data.get('activation_key')  # Extract the 'activation_key' from the JSON data

    # If no activation key is provided, return an error
    if not activation_key:
        return jsonify({'valid': False, 'message': 'Activation key is required'}), 400

    # Validate the license key; if valid, return a success message
    if validate_license_key(activation_key):
        return jsonify({'valid': True, 'message': 'License key is valid'})
    else:
        # If the license key is invalid or inactive, return an error message
        return jsonify({'valid': False, 'message': 'Invalid or inactive license key'}), 400


# Run the Flask application on port 5000 when the script is executed
if __name__ == '__main__':
    app.run(port=5000)
