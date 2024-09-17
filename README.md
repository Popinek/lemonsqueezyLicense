# License Key Management System With LemonSqueezy For Python Apps

This project manages license keys using the Lemon Squeezy API, allowing for key activation and validation via a command-line tool and a Flask-based web server.

## Features

- **Command-Line Interface**:
  - Prompt for a license key.
  - Activate a license key using Lemon Squeezy API.
  - Validate the license key & HWID.
  - Save and load the license key from a file.

- **Flask Web Server**:
  - Provides an API to validate license keys via a POST request.

## Requirements

- Python 3.x
- `requests` library
- `Flask` library
- `sqlite3` library

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Popinek/lemonsqueezyLicense.git
   cd lemonsqueezyLicense
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Create a `.env` file in the root directory and add your URL:
   ```
   URL=https://example.com/validate
   ```

## Usage

### Command-Line Interface

1. **Run the Script**:
   ```bash
   python client.py
   ```

   - The script will prompt for a license key.
   - It will attempt to activate and validate the key.
   - HWID validation is performed after successful license activation.
   - If successful, it will save the key and run the main script functionality.

2. **License Key Activation**:
   - Enter your license key when prompted.
   - Type `'quit'` to exit the program.

3. **Main Script**:
   - Replace the placeholder `main_script` function with your actual application logic.

### Flask Web Server

1. **Run the Flask Application**:
   ```bash
   python app.py
   ```

   - By default, the Flask server will run on port 5000.

2. **Validate License Key via API**:
   - Send a POST request to `http://127.0.0.1:5000/validate` with JSON payload:
     ```json
     {
       "activation_key": "your_license_key_here"
     }
     ```
   - Response will be in JSON format indicating whether the license key is valid or not.
   - If HWID mismatch occurs, access is denied.

## API Endpoint

- **POST /validate**

  **Request Body**:
  ```json
  {
    "activation_key": "string"
  }
  ```

  **Response**:
  ```json
    {
      "status": "success",
      "message": "License key and HWID matches!"
    }
  ```
  or

  ```json
    {
      "status": "success",
      "message": "License key and HWID added successfully"
    }
  ```
  
  or

  ```json
    {
      "status": "error",
      "message": "HWID mismatch"
    }
  ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the GitHub repository.