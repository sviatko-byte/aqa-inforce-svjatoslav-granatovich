from client import unique_room_payload, updated_room_payload, booking_payload


def test_create_and_verify_room(admin_client):
    payload = unique_room_payload(price=225)
    admin_client.create_room(payload)

    rooms = admin_client.get_rooms()
    created = next((r for r in rooms if r["roomName"] == payload["roomName"]), None)

    assert created, "Room not found"
    assert created["roomPrice"] == 225
    assert created["type"] == "Family"


def test_book_room(admin_client, api_client):
    # Create unique room via admin
    payload = unique_room_payload()
    admin_client.create_room(payload)

    rooms = admin_client.get_rooms()
    room = next(r for r in rooms if r["roomName"] == payload["roomName"])

    # Book room as public client
    booking = api_client.create_booking(booking_payload(room["roomid"]))
    booking_id = booking["bookingid"]

    # Verify it appears in admin report
    report = admin_client.get_report()
    expected_title = f"SVIATOSLAV HRANATOVYCH - Room: {room['roomName']}"

    found = next((b for b in report if b["title"] == expected_title), None)
    assert found, f"Booking {booking_id} not found in admin report"


def test_edit_room_and_verify(admin_client):
    # Create
    payload = unique_room_payload()
    admin_client.create_room(payload)

    room = next(r for r in admin_client.get_rooms()
                if r["roomName"] == payload["roomName"])

    # Update
    updated = updated_room_payload(roomid=room["roomid"], name=room["roomName"])
    admin_client.update_room(room["roomid"], updated)

    # Verify
    rooms = admin_client.get_rooms()
    updated_room = next(r for r in rooms if r["roomid"] == room["roomid"])

    assert updated_room["description"] == "API TEST ROOM changed"
    assert updated_room["roomPrice"] == 777


def test_delete_room_and_verify_removed(admin_client):
    payload = unique_room_payload()
    admin_client.create_room(payload)

    room = next(r for r in admin_client.get_rooms()
                if r["roomName"] == payload["roomName"])

    admin_client.delete_room(room["roomid"])

    rooms_after = admin_client.get_rooms()
    assert not any(r["roomid"] == room["roomid"] for r in rooms_after)
