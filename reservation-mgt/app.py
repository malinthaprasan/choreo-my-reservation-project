import json
import ast
import os
import requests

from flask import Flask, jsonify, request
from types import SimpleNamespace

app = Flask(__name__)

# defines initial reservations
with open('data.txt') as f:
    reservations = ast.literal_eval(f.read())

# read env USER_VALIDATOR_URL

USER_VALIDATOR_URL = os.getenv('USER_VALIDATOR_URL', 'http://localhost:8080')


# route relevant to the reservation management
@app.route('/rs/reservations/<reservationId>', methods=['GET', 'PUT', 'DELETE'])
def reservation_management(reservationId):
    try:
        if request.method == "GET":
            return getReservation(reservationId)
        elif request.method == "PUT":
            return updateReservation(reservationId, request)
        elif request.method == "DELETE":
            return deleteReservation(reservationId)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# route relevant to get all reservations
@app.route('/rs/reservations', methods=['POST'])
def add_reservation():
    try:
        return addReservation(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# route relevant to the hello world
@app.route('/rs/healthCheck', methods=['GET'])
def health_check():
    return "Hello, Welcome to the simple reservation management app!"

# route relevant to get all reservations
@app.route('/rs/reservations', methods=['GET'])
def get_reservations():
    return str(json.dumps(reservations))

# gives a reservation created by the user considering the reservationId
def getReservation(reservationId):
    print("getReservation")
    for reservation in reservations:
        if reservation["reservationId"] == reservationId:
            print(type(json.dumps(reservation)))
            return str(json.dumps(reservation))
    return None

# adds a reservation to the list of reservations
def addReservation(request):
    x = json.loads(request.get_data(), object_hook=lambda d: SimpleNamespace(**d))
    # validate x.contact using user validator api
    response = requests.get(f"{USER_VALIDATOR_URL}/validate-phone?phone_number={x.contact}")
    validation_result = response.json()
    if not validation_result["valid"]:
        raise ValueError("Invalid phone number format")
    
    reservations.append({
        "reservationCreator" : x.reservationCreator,
		"reservationId" : x.reservationId,
		"contact" : x.contact,})

    print(reservations)
    return str(request.get_data())

# deletes a reservation from the list of reservations considering the reservationId
def deleteReservation(reservationId):
    for reservation in reservations:
        if reservation["reservationId"] == reservationId:
            reservations.remove(reservation)
            return str(json.dumps(reservation))
    return reservationId

# updates a reservation from the list of reservations considering the reservationId
def updateReservation(reservationId, request):
    for reservation in reservations:
        if reservation["reservationId"] == reservationId:
            reservations.remove(reservation)
            x = json.loads(request.get_data(), object_hook=lambda d: SimpleNamespace(**d))
            reservations.append({
                "reservationCreator" : x.reservationCreator,
		        "reservationId" : x.reservationId,
		        "contact" : x.contact,})
    print(reservations)
    return reservationId

if __name__ == "__main__":
    app.run(port=8085)
