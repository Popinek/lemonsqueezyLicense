import requests
import os

# URLs for Lemon Squeezy API
ACTIVATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/activate'
VALIDATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/validate'

# Set your Lemon Squeezy API key here
LEMON_SQUEEZY_API_KEY = 'YOUR_LEMON_SQUEEZY_API_KEY'


def prompt_for_license_key():
    return input("Please enter your license key (or type 'quit' to exit): ")


def activate_license_key(license_key):
    headers = {
        'Authorization': f'Bearer {LEMON_SQUEEZY_API_KEY}',
        'Accept': 'application/json'
    }
    data = {
        'license_key': license_key,
        'instance_name': 'MyAppInstance',  # Customize this as needed
    }
    try:
        response = requests.post(ACTIVATE_URL, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()

        # Check for 'status': 'active' in the response
        if result.get('license_key', {}).get('status') == 'active':
            print("License key activated successfully.")
            save_activation_key(license_key)  # Save the key upon successful activation
            return True
        else:
            print("Failed to activate license key. Response:", result)
            return False
    except requests.RequestException as e:

        print(f"An error occurred during activation")
        return False


def validate_license_key():
    activation_key = load_activation_key()
    if not activation_key:
        print("No license key found. Please activate the key.")
        return False

    headers = {
        'Authorization': f'Bearer {LEMON_SQUEEZY_API_KEY}',
        'Accept': 'application/json'
    }
    data = {
        'license_key': activation_key
    }

    try:
        response = requests.post(VALIDATE_URL, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()

        if result.get('valid'):
            return True
        else:
            print(result.get('error', 'Unknown error occurred'))
            return False
    except requests.RequestException as e:
        print(f"An error occurred during validation")
        return False


def save_activation_key(activation_key):
    with open("license_key.txt", "w") as file:
        file.write(activation_key)


def load_activation_key():
    if os.path.exists("license_key.txt"):
        with open("license_key.txt", "r") as file:
            return file.read().strip()
    return None


def main_script():
    # Your main script functionality here
    print("Running the main script...")


def main():
    activation_key = load_activation_key()

    if activation_key:
        print("License key found. Validating...")
        if not validate_license_key():
            print("Your license key is invalid, expired, or canceled. Please buy a subscription.")
            return
    else:
        while True:
            license_key = prompt_for_license_key()
            save_activation_key(license_key)
            if license_key.lower() == 'quit':
                print("Exiting the program.")
                return

            if activate_license_key(license_key) or validate_license_key():
                break

    # Once a valid key is provided and validated, run the main script
    main_script()


if __name__ == "__main__":
    main()
