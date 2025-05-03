<!--

Copyright (c) 2023, WSO2 LLC. (https://www.wso2.com/) All Rights Reserved.

WSO2 LLC. licenses this file to you under the Apache License,
Version 2.0 (the "License"); you may not use this file except
in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.

  -->
# Running the application locally.

To run the application execute below command

```sh
. exports.sh
FLASK_APP=app.py flask run --port=8085
```

# Invoking resources

## Viewing all the available resevations

```
curl -X GET http://localhost:8085/rs/reservations

[{"from_date":"2025-05-10","hotel_id":1,"hotel_name":"Ocean View Resort","id":1,"room_id":1,"room_type":"Deluxe","to_date":"2025-05-12","user_contact":"alice@example.com","user_id":1,"user_name":"Alice Johnson"},{"from_date":"2025-05-11","hotel_id":1,"hotel_name":"Ocean View Resort","id":2,"room_id":2,"room_type":"Standard","to_date":"2025-05-13","user_contact":"bob@example.com","user_id":2,"user_name":"Bob Smith"},{"from_date":"2025-05-15","hotel_id":2,"hotel_name":"Mountain Escape Lodge","id":3,"room_id":6,"room_type":"Standard","to_date":"2025-05-18","user_contact":"alice@example.com","user_id":1,"user_name":"Alice Johnson"}]

```

## Viewing a specific resevation

```
curl -X GET http://localhost:8085/rs/reservations/1234

Your reservation details: {"reservationCreator": "John Doe", "reservationId": "1234", "contact": "011-123-4567"}

```

## Adding a resevation

```
curl -X POST http://localhost:8085/rs/reservations -H "Content-Type: application/json" -d '{"from_date":"2024-07-01","to_date":"2024-07-05","hotel_id":1,"room_id":3,"user_id":1,"reservation_contact":"+94775678901"}'


Your added reservation details: b'{"reservationCreator": "John Doe", "reservationId": "111", "contact": "011-123-1111"}'
```

## Updating a resevation

```
curl -X PUT http://localhost:8085/rs/reservations/1234 -d '{"reservationCreator": "Lahiru C", "reservationId": "1234", "contact": "011-123-4588"}' 

Reservation updated: 1234
```

## Deleting a resevation

```
curl -X DELETE http://localhost:8085/rs/reservations/1234

Reservation deleted: {"reservationCreator": "John Doe", "reservationId": "1234", "contact": "011-123-4567"}

```
