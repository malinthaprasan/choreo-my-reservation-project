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
    return getAllReservations()


@app.route('/rs/hotels', methods=['GET'])
def list_all_hotels():
    return getAllHotels()

@app.route('/rs/hotels/<hotelId>', methods=['GET'])
def get_hotel_by_id(hotelId):
    return getHotelById(hotelId)

def getHotelById(hotelId):
    try:
        conn = cnx_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM hotel WHERE id = %s", (hotelId,))
        hotel = cursor.fetchone()
        cursor.close()
        conn.close()
        if hotel is None:
            return jsonify({"error": "Hotel not found"}), 404

        # Format response according to schema
        hotel_data = {"id": hotel[0], "name": hotel[1]}
        return jsonify(hotel_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getAllHotels():
    try:
        conn = cnx_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM hotel")
        hotels = cursor.fetchall()
        cursor.close()
        conn.close()
        # Format response according to schema
        hotel_list = [{"id": hotel[0], "name": hotel[1]} for hotel in hotels]
        return jsonify(hotel_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getAllReservations():
    try:
        conn = cnx_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                hrr.id,
                hrr.from_date,
                hrr.to_date,
                h.id as hotel_id,
                h.name as hotel_name,
                hr.id as room_id,
                hr.type as room_type,
                u.id as user_id,
                u.name as user_name,
                u.contact as user_contact
            FROM hotel_room_reservation hrr
            JOIN hotel h ON hrr.hotel_id = h.id
            JOIN hotel_room hr ON hrr.room_id = hr.id
            JOIN qb_user u ON hrr.user_id = u.id
        """)
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert date objects to string format before JSON serialization
        formatted_reservations = []
        for res in reservations:
            formatted_res = {
                'id': res[0],
                'from_date': res[1].strftime('%Y-%m-%d'),
                'to_date': res[2].strftime('%Y-%m-%d'), 
                'hotel_id': res[3],
                'hotel_name': res[4],
                'room_id': res[5],
                'room_type': res[6],
                'user_id': res[7],
                'user_name': res[8],
                'user_contact': res[9]
            }
            formatted_reservations.append(formatted_res)
        return jsonify(formatted_reservations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# gives a reservation created by the user considering the reservationId
def getReservation(reservationId):
    try:
        conn = cnx_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                hrr.id,
                hrr.from_date,
                hrr.to_date,
                h.id as hotel_id,
                h.name as hotel_name,
                hr.id as room_id,
                hr.type as room_type,
                u.id as user_id,
                u.name as user_name,
                u.contact as user_contact,
                hrr.contact as reservation_contact
            FROM hotel_room_reservation hrr
            JOIN hotel h ON hrr.hotel_id = h.id
            JOIN hotel_room hr ON hrr.room_id = hr.id
            JOIN qb_user u ON hrr.user_id = u.id
            WHERE hrr.id = %s
        """, (reservationId,))
        reservation = cursor.fetchone()
        cursor.close()
        conn.close()
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404
            
        formatted_res = {
            'id': reservation[0],
            'from_date': reservation[1].strftime('%Y-%m-%d'),
            'to_date': reservation[2].strftime('%Y-%m-%d'),
            'hotel_id': reservation[3], 
            'hotel_name': reservation[4],
            'room_id': reservation[5],
            'room_type': reservation[6],
            'user_id': reservation[7],
            'user_name': reservation[8],
            'user_contact': reservation[9],
            'reservation_contact': reservation[10]
        }
        return jsonify(formatted_res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# adds a reservation to the list of reservations
def addReservation(request):
    x = json.loads(request.get_data(), object_hook=lambda d: SimpleNamespace(**d))
    # validate x.contact using user validator api
    response = requests.get(f"{USER_VALIDATOR_URL}/validate-phone?phone_number={x.reservation_contact}")
    validation_result = response.json()
    if not validation_result["valid"]:
        raise ValueError("Invalid phone number format")
    
    conn = cnx_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hotel_room_reservation 
        (from_date, to_date, hotel_id, room_id, user_id, contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (x.from_date, x.to_date, x.hotel_id, x.room_id, x.user_id, x.reservation_contact))
    reservation_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return getReservation(reservation_id)

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
