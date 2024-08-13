import requests  # Import the requests library to handle HTTP requests
import os  # Import the os module to interact with the operating system, such as reading environment variables

# TODO
# add security for activation keys


# URLs for interacting with the Lemon Squeezy API
ACTIVATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/activate'  # URL for activating a license
VALIDATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/validate'  # URL for validating a license


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
        'instance_name': 'MyAppInstance',  # Customize this name as needed for your application
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

        # Check if the license key is valid
        if result.get('valid'):
            return True
        else:
            # If the validation fails, print the error message for debugging purposes
            print(result.get('error', 'Unknown error occurred'))
            return False
    except requests.RequestException:
        # Handle any exceptions that occur during the request
        print(f"An error occurred during validation")
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


# The main function that runs your script's main functionality
def main_script():
    # Place your script's primary functionality here
    print("Running the main script...")


# The main function that orchestrates the license activation and validation process
def main():
    activation_key = load_activation_key()  # Load the activation key from the file

    if activation_key:
        print("License key found. Validating...")
        if not validate_license_key():  # Validate the loaded license key
            print("Your license key is invalid, expired, or canceled. Please buy a subscription.")
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
                break  # Exit the loop if the license key is valid

    # If the license key is valid, run the main script
    main_script()


# Check if this script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()  # Call the main function to start the program
