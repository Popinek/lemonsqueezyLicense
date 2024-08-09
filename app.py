from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

LEMON_SQUEEZY_API_KEY = os.getenv('LEMON_SQUEEZY_API_KEY')


def validate_license_key(activation_key):
    headers = {
        'Authorization': f'Bearer {LEMON_SQUEEZY_API_KEY}',
        'Accept': 'application/json',
    }
    response = requests.get(f'https://api.lemonsqueezy.com/v1/licenses/{activation_key}', headers=headers)
    if response.status_code == 200:
        license_data = response.json()
        return license_data['data']['attributes']['status'] == 'active'
    return False


@app.route('/validate', methods=['POST'])
def validate():
    if not request.is_json:
        return jsonify({'valid': False, 'message': 'Request must be JSON'}), 400

    data = request.get_json()
    activation_key = data.get('activation_key')

    if not activation_key:
        return jsonify({'valid': False, 'message': 'Activation key is required'}), 400

    if validate_license_key(activation_key):
        return jsonify({'valid': True, 'message': 'License key is valid'})
    else:
        return jsonify({'valid': False, 'message': 'Invalid or inactive license key'}), 400


if __name__ == '__main__':
    app.run(port=5000)
