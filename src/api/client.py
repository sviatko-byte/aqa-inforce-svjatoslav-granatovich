import uuid
import requests

BASE = "https://automationintesting.online"


class ApiClient:
    def __init__(self):
        self.base = BASE
        self.session = requests.Session()
        self.token = None

    # --------------------
    # AUTH
    # --------------------
    def login_admin(self, username="admin", password="password"):
        r = self.session.post(
            f"{self.base}/api/auth/login",
            json={"username": username, "password": password}
        )
        assert r.status_code == 200, f"Login failed: {r.text}"
        self.token = r.json()["token"]
        self.session.cookies.set("token", self.token)
        return self

    # --------------------
    # ROOMS
    # --------------------
    def create_room(self, payload):
        r = self.session.post(f"{self.base}/api/room", json=payload)
        assert r.status_code == 200, f"Room create error: {r.text}"
        return r.json()

    def update_room(self, roomid, payload):
        r = self.session.put(f"{self.base}/api/room/{roomid}", json=payload)
        assert r.status_code == 200, f"Room update error: {r.text}"
        return r.json()

    def delete_room(self, roomid):
        r = self.session.delete(f"{self.base}/api/room/{roomid}")
        assert r.status_code == 200, f"Delete error: {r.text}"
        return r.json()

    def get_rooms(self):
        r = self.session.get(f"{self.base}/api/room")
        assert r.status_code == 200
        return r.json()["rooms"]

    # --------------------
    # BOOKING
    # --------------------
    def create_booking(self, payload):
        r = self.session.post(f"{self.base}/api/booking", json=payload)
        assert r.status_code == 201, f"Booking error: {r.text}"
        return r.json()

    def get_report(self):
        r = self.session.get(f"{self.base}/api/report")
        assert r.status_code == 200
        return r.json()["report"]


# -------------------------
# HELPERS
# -------------------------
def unique_room_payload(price=123):
    return {
        "roomName": f"room_{uuid.uuid4().hex[:6]}",
        "type": "Family",
        "accessible": True,
        "description": "API TEST ROOM",
        "image": "https://www.mwtestconsultancy.co.uk/img/room1.jpg",
        "roomPrice": price,
        "features": ["WiFi"]
    }


def updated_room_payload(roomid, name):
    return {
        "roomid": roomid,
        "roomName": name,
        "type": "Family",
        "accessible": True,
        "image": "https://www.mwtestconsultancy.co.uk/img/room1.jpg",
        "description": "API TEST ROOM changed",
        "features": ["WiFi"],
        "roomPrice": 777,
        "featuresObject": {
            "WiFi": True,
            "TV": False,
            "Radio": False,
            "Refreshments": False,
            "Safe": False,
            "Views": False
        }
    }


def booking_payload(roomid):
    return {
        "roomid": roomid,
        "firstname": "SVIATOSLAV",
        "lastname": "HRANATOVYCH",
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-12-28",
            "checkout": "2026-12-29"
        },
        "email": "test@example.com",
        "phone": "+380685474919"
    }
