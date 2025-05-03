from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/validate-user', methods=['GET'])
def validate_user():
    # Extract phone number from query parameters
    username = request.args.get('username', '')

    # Regular expression to match Sri Lankan phone numbers
    pattern = r'^0\d{9}$'
    if re.match(pattern, username):
        result = {"valid": True, "message": "Valid Sri Lankan phone number."}
    else:
        result = {"valid": False, "message": "Invalid Sri Lankan phone number."}
    
    return jsonify(result)

@app.route('/validate-phone', methods=['GET'])
def validate_phone_number():
    # Extract phone number from query parameters
    phone_number = request.args.get('phone_number')
    if not phone_number:
        return jsonify({"valid": False, "message": "Phone number not provided"})

    # Regular expression to match Sri Lankan phone numbers
    pattern = r'^94\d{9}$'
    if re.match(pattern, phone_number):
        result = {"valid": True, "message": "Valid Sri Lankan phone number."}
    else:
        result = {"valid": False, "message": "Invalid Sri Lankan phone number."}
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8080)
