import uuid
import requests
import pytest

BASE = "https://automationintesting.online"


def login():
    r = requests.post(
        f"{BASE}/api/auth/login",
        json={"username": "admin", "password": "password"}
    )
    assert r.status_code == 200, "Login failed"
    token = r.json().get("token")
    assert token, "Token missing"
    return token


def create_unique_room(price=123):
    token = login()
    cookies = {"token": token}

    room_name = f"room_{uuid.uuid4().hex[:6]}"

    payload = {
        "roomName": room_name,
        "type": "Family",
        "accessible": True,
        "description": "API TEST ROOM",
        "image": "https://www.mwtestconsultancy.co.uk/img/room1.jpg",
        "roomPrice": price,
        "features": ["WiFi"]
    }

    r = requests.post(f"{BASE}/api/room", cookies=cookies, json=payload)
    assert r.status_code == 200, f"Room creation failed: {r.status_code}\n{r.text}"

    # confirm by reading all rooms
    r_all = requests.get(f"{BASE}/api/room")
    rooms = r_all.json()["rooms"]

    created = next((x for x in rooms if x["roomName"] == room_name), None)
    assert created, "Created room not found!"

    return created["roomid"], created["roomName"]


def test_create_and_verify_room():
    room_price = 225
    roomid, room_name = create_unique_room(price=room_price)

    r_get = requests.get(f"{BASE}/api/room")
    assert r_get.status_code == 200

    rooms = r_get.json()["rooms"]
    created = next((room for room in rooms if room["roomName"] == room_name), None)

    assert created, "Created room not found in GET /api/room"
    assert created["roomPrice"] == room_price
    assert created["type"] == "Family"

    print("Room verified:", created)


def test_book_room():
    # 1. Create a new unique free room
    roomid, room_name = create_unique_room()

    # 2. Booking request (no login required)
    booking_payload = {
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

    r = requests.post(f"{BASE}/api/booking", json=booking_payload)
    assert r.status_code == 201, f"Booking failed: {r.status_code}\n{r.text}"

    booking_id = r.json()["bookingid"]
    print("Booking created:", booking_id)

    # 3. Login for admin report
    token = login()
    cookies = {"token": token}

    r_report = requests.get(f"{BASE}/api/report", cookies=cookies)
    assert r_report.status_code == 200

    report_data = r_report.json()["report"]

    expected_title = f"SVIATOSLAV HRANATOVYCH - Room: {room_name}"
    expected_start = "2026-12-28"
    expected_end = "2026-12-29"

    # 4. Validate booking in admin report
    found = next(
        (
            b for b in report_data
            if b["title"] == expected_title
            and b["start"] == expected_start
            and b["end"] == expected_end
        ),
        None
    )
    assert found, f"Booking not found in report! Report: {report_data}"

    print("FOUND booking:", found)


def test_edit_room_and_verify_on_user_page():
    # 1. Create original room
    roomid, room_name = create_unique_room(price=123)

    # 2. Login for PUT
    token = login()
    cookies = {"token": token}

    # 3. Prepare NEW UPDATED DATA
    updated_payload = {
        "roomid": roomid,
        "roomName": room_name,
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

    # 4. PUT update request (Admin)
    r_put = requests.put(
        f"{BASE}/api/room/{roomid}",
        cookies=cookies,
        json=updated_payload
    )

    assert r_put.status_code == 200, f"PUT failed: {r_put.status_code} {r_put.text}"
    print("PUT response:", r_put.json())

    # 5. Get all rooms as USER page (/api/room)
    r_get = requests.get(f"{BASE}/api/room")
    assert r_get.status_code == 200

    rooms = r_get.json()["rooms"]

    updated = next((x for x in rooms if x["roomid"] == roomid), None)
    assert updated, "Updated room not found after PUT"

    # 6. Assertions: confirm user sees updated changes
    assert updated["description"] == "API TEST ROOM changed"
    assert updated["roomPrice"] == 777

    print("Updated room verified:", updated)


def test_delete_room_and_verify_removed():
    # 1. Create a room
    roomid, room_name = create_unique_room()

    # 2. Login for DELETE
    token = login()
    cookies = {"token": token}

    # 3. DELETE /api/room/{roomid}
    r_delete = requests.delete(f"{BASE}/api/room/{roomid}", cookies=cookies)
    assert r_delete.status_code == 200, f"Delete failed: {r_delete.status_code}\n{r_delete.text}"

    print("Delete response:", r_delete.json())

    # 4. Verify room is gone from GET /api/room
    r_get = requests.get(f"{BASE}/api/room")
    assert r_get.status_code == 200

    rooms = r_get.json()["rooms"]

    deleted = next((r for r in rooms if r["roomid"] == roomid), None)

    assert deleted is None, f"Room {roomid} still exists after delete! Rooms: {rooms}"

    print(f"Room {roomid} was successfully deleted.")