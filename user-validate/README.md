# Sri Lankan Phone Number Validation API

This project provides a REST API for validating whether a given phone number is in the correct Sri Lankan format. It uses Flask for the web server and offers a simple OpenAPI specification for API documentation and integration purposes.

## Features

- Validate Sri Lankan phone numbers through a REST API.
- GET request endpoint to easily validate phone numbers.
- JSON responses indicating validation results.
- OpenAPI (Swagger) documentation for API specification.

## Requirements

- Python 3.x
- Flask
- A web browser or API testing tool (e.g., Postman, curl)

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Create a virtual environment:

python -m venv venv


4. Activate the virtual environment:

- On Windows:

  ```
  .\venv\Scripts\activate
  ```

- On Unix or MacOS:

  ```
  source venv/bin/activate
  ```

5. Install the required dependencies:

pip install -r requirements.txt

## Running the API

1. Start the Flask application:

python phone_number_api.py

2. The API is now running on `http://localhost:5000`.

## Using the API

To validate a Sri Lankan phone number, make a GET request to the `/validate` endpoint with the `phone_number` query parameter.

Example using curl:

curl "http://localhost:5000/validate?phone_number=+947XXXXXXXX"

Response:

```json
{
  "valid": true,
  "message": "Valid Sri Lankan phone number."
}