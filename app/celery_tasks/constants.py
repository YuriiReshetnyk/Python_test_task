"""
Constants for celery_tasks app.
"""

USER_API_URL = "https://random-data-api.com/api/v2/users"
CREDIT_CARD_API_URL = "https://random-data-api.com/api/v2/credit_cards"
ADDRESS_API_URL = "https://random-data-api.com/api/v2/addresses"

USER_ATTRIBUTES = ['uid', 'password', 'first_name', 'last_name',
                   'username', 'email', 'avatar',
                   'gender', 'phone_number',
                   'social_insurance_number', 'date_of_birth']

CREDIT_CARD_ATTRIBUTES = ['credit_card_number', 'credit_card_expiry_date',
                          'credit_card_type']

ADDRESS_ATTRIBUTES = ["city", "street_name", "street_address",
                      "secondary_address", "building_number",
                      "mail_box", "community", "zip_code", "zip",
                      "postcode", "time_zone", "street_suffix",
                      "city_suffix", "city_prefix", "state",
                      "state_abbr", "country", "country_code",
                      "latitude", "longitude", "full_address"]

FAKE_USER_API_RETURN = {
    "id": 184,
    "uid": "54636893-7ed7-4d4b-8c3a-4f1f88e4910b",
    "password": "DEhkcCx8Vr",
    "first_name": "Edgardo",
    "last_name": "Conn",
    "username": "edgardo.conn",
    "email": "edgardo.conn@email.com",
    "avatar": "https://robohash.org/aliquamvoluptatumratione."
              "png?size=300x300&set=set1",
    "gender": "Agender",
    "phone_number": "+359 165.336.1768 x5911",
    "social_insurance_number": "780359923",
    "date_of_birth": "1980-01-31",
    "employment": {
        "title": "Senior Manufacturing Engineer",
        "key_skill": "Teamwork"
    },
    "address": {
        "city": "Satterfieldhaven",
        "street_name": "Von Summit",
        "street_address": "18021 Bergnaum Court",
        "zip_code": "49926",
        "state": "Hawaii",
        "country": "United States",
        "coordinates": {
            "lat": -57.6889603089354,
            "lng": 55.9607034923273
        }
    },
    "credit_card": {
        "cc_number": "4998629252843"
    },
    "subscription": {
        "plan": "Diamond",
        "status": "Pending",
        "payment_method": "Cash",
        "term": "Annual"
    }
}

FAKE_ADDRESS_API_RETURN = {
    "id": 5110,
    "uid": "e25a66f8-4b64-4de6-8c0b-e9f634896690",
    "city": "Marquardttown",
    "street_name": "Keeling Branch",
    "street_address": "75647 Jenkins Radial",
    "secondary_address": "Apt. 291",
    "building_number": "579",
    "mail_box": "PO Box 618",
    "community": "Pine Court",
    "zip_code": "31197-2097",
    "zip": "93590-8760",
    "postcode": "86072-9914",
    "time_zone": "America/Sao_Paulo",
    "street_suffix": "Loop",
    "city_suffix": "haven",
    "city_prefix": "West",
    "state": "Idaho",
    "state_abbr": "WV",
    "country": "Tuvalu",
    "country_code": "KG",
    "latitude": -60.9501613675435,
    "longitude": 124.0559075561,
    "full_address": "839 Orlando Expressway, South June, WY 53391"
}

FAKE_CREDIT_CARD_API_RETURN = {
    "id": 1161,
    "uid": "d41327f9-2672-41fd-807d-f94e9a10313b",
    "credit_card_number": "1211-1221-1234-2201",
    "credit_card_expiry_date": "2027-10-27",
    "credit_card_type": "solo"
}
