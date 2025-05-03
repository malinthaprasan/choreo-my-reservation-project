import json
import ast
import os
import requests

from flask import Flask, jsonify, request
from types import SimpleNamespace

# db.py — for global connection pool setup
from mysql.connector import pooling

hostname = os.getenv("CHOREO_QB_DB_CONNECTION_HOSTNAME")
port = os.getenv("CHOREO_QB_DB_CONNECTION_PORT")
username = os.getenv("CHOREO_QB_DB_CONNECTION_USERNAME")
password = os.getenv("CHOREO_QB_DB_CONNECTION_PASSWORD")
databasename = os.getenv("CHOREO_QB_DB_CONNECTION_DATABASENAME")


dbconfig = {
    "host": hostname,
    "port": port,
    "user": username,
    "password": password,
    "database": databasename,
    "ssl_disabled": False,
    "ssl_verify_identity": False  # <-- do not verify hostname
}

cnx_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

app = Flask(__name__)

print("=== start env variables ==")
for key, value in os.environ.items():
    print(f"{key}={value}")
print("=== end env variables ====")

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

@app.route('/rs/hotels', methods=['GET'])
def list_all_hotels():
    try:
        conn = cnx_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM hotel")
        hotels = cursor.fetchall()
        cursor.close()

        # Format response according to schema
        hotel_list = [{"id": hotel[0], "name": hotel[1]} for hotel in hotels]
        return jsonify(hotel_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
