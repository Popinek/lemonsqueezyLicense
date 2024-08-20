import requests  # Import the requests library to handle HTTP requests
import os  # Import the os module to interact with the operating system, such as reading environment variables
import hashlib




# URLs for interacting with the Lemon Squeezy API
ACTIVATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/activate'  # URL for activating a license
VALIDATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/validate'  # URL for validating a license


# Function to Generate a simple HWID based on the machine's MAC address.
def get_hwid():
    hwid = hashlib.md5(os.popen('getmac').read().encode('utf-8')).hexdigest()
    return hwid


# Function to prompt the user for a license key
def prompt_for_license_key():
    return input("Please enter your license key (or type 'quit' to exit): ")


# Function to activate the provided license key using the Lemon Squeezy API
def activate_license_key(license_key):
    headers = {
        'Accept': 'application/json'  # Request that the response is returned in JSON format
    }
    data = {
        'license_key': license_key,  # Include the provided license key in the request data
        'instance_name': 'PythonAppLemonSqueezy',  # Customize this name as needed for your application
    }
    try:
        # Send a POST request to the Lemon Squeezy API to activate the license key
        response = requests.post(ACTIVATE_URL, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for any HTTP status codes that indicate a request failure
        result = response.json()  # Parse the JSON response

        # Check if the license key was successfully activated by verifying its status
        if result.get('license_key', {}).get('status') == 'active':
            print("License key activated successfully.")
            save_activation_key(license_key)  # Save the license key to a file upon successful activation
            return True
        else:
            # If the activation fails, print the response for debugging purposes
            print("Failed to activate license key. Response:", result)
            return False
    except requests.HTTPError as e:
        if response.status_code == 400 and "true" in response.text:
            print("This license key has already been activated.")
            save_activation_key(license_key)  # Save the key since it's valid but already activated
            return True  # Consider this a success
        else:
            # Handle other types of HTTP errors
            return False
    except requests.RequestException:
        # Handle any exceptions that occur during the request
        print(f"An error occurred during activation")
        return False


# Function to validate the license key by checking its status with the Lemon Squeezy API
def validate_license_key():
    activation_key = load_activation_key()  # Load the saved activation key from a file
    if not activation_key:
        print("No license key found. Please activate the key.")
        return False

    headers = {
        'Accept': 'application/json'  # Request that the response is returned in JSON format
    }
    data = {
        'license_key': activation_key  # Include the saved license key in the request data
    }

    try:
        # Send a POST request to the Lemon Squeezy API to validate the license key
        response = requests.post(VALIDATE_URL, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for any HTTP status codes that indicate a request failure
        result = response.json()  # Parse the JSON response

        # Check if the license key is valid and not expired or disabled
        status = result.get('license_key', {}).get('status')

        if status == 'active':
            print(f"Your license key is {status}.")
            return True
        elif status in ['inactive', 'expired', 'disabled']:
            print(f"Your license key is {status}. Please contact support or renew your subscription.")
            return False
        else:
            print(result.get('error', 'Unknown error occurred'))
            return False
    except requests.RequestException:
        # Handle any exceptions that occur during the request
        print("Your license key is invalid. Please contact support or renew your subscription.")
        return False


# Function to save the activation key to a file
def save_activation_key(activation_key):
    with open("license_key.txt", "w") as file:  # Open the file in write mode
        file.write(activation_key)  # Write the activation key to the file


# Function to load the activation key from the file
def load_activation_key():
    if os.path.exists("license_key.txt"):  # Check if the file exists
        with open("license_key.txt", "r") as file:  # Open the file in read mode
            return file.read().strip()  # Read and return the contents of the file, removing any leading/trailing whitespace
    return None  # Return None if the file does not exist


# Function check if License key match HWID
def validate_hwid():
    hwid = get_hwid()
    license_key = load_activation_key()

    data = {
        'license_key': license_key,
        'hwid': hwid
    }
    try:
        response = requests.post('http://127.0.0.1:5000/validate', json=data)
        result = response.json()

        if response.status_code == 200:
            print(result['message'])
            return True  # Proceed if HWID matches
        elif response.status_code == 404:  # Handle case where license key doesn't exist in the DB
            print("License key not found in the database. Adding it now...")
            response = requests.post('http://127.0.0.1:5000/validate', json=data)
            result = response.json()
            if response.status_code == 200:
                print(result['message'])
                return True  # Proceed after adding the license key and HWID
            else:
                print(f"Error: {result['message']}")
                return False
        else:
            print(f"Error: {result['message']}")
            return False  # Deny access if HWID doesn't match or another error occurs
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to server: {e}")
        return False  # Deny access if there's an error connecting to the server



# The main function that runs your script's main functionality
def main_script():
    # Place your script's primary functionality here
    print("Running the main script...")


# The main function that orchestrates the license activation and validation process
def main():
    activation_key = load_activation_key()  # Load the activation key from the file

    if activation_key:
        print("License key found. Validating...")

        if validate_license_key():  # Validate the loaded license key
            if validate_hwid():  # Run HWID validation and check if it was successful
                main_script()  # Only run the main script if HWID validation succeeds
            else:
                print("Access denied due to HWID mismatch.")  # Notify user of denial
                return  # Exit the program if HWID does not match
        else:
            return  # Exit the program if the license key is invalid

    else:
        # Prompt the user for a license key until a valid one is provided or the user quits
        while True:
            license_key = prompt_for_license_key()  # Prompt the user to enter a license key
            save_activation_key(license_key)  # Save the entered license key to the file
            if license_key.lower() == 'quit':  # Exit the program if the user types 'quit'
                print("Exiting the program.")
                return

            if activate_license_key(license_key) or validate_license_key():  # Activate or validate the license key
                if validate_hwid():  # Run HWID validation and check if it was successful
                    main_script()  # Only run the main script if HWID validation succeeds
                else:
                    print("Access denied due to HWID mismatch.")  # Notify user of denial
                break  # Exit the loop if the license key is valid and HWID matches




# Check if this script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()  # Call the main function to start the program
