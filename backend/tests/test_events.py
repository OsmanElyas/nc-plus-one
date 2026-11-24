from datetime import datetime, timezone

import pytest

from app.auth.jwt import create_access_token


def event_payload():
    return {
        "title": "Integration-created event",
        "description": "Created by the event endpoint test.",
        "starts_at": "2025-08-15T18:00:00Z",
        "ends_at": "2025-08-15T21:00:00Z",
        "venue_id": 2,
    }


def test_len_of_events_is_correct(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()["events"] ) == 5


def test_returns_correct_event(client):
    response = client.get("/api/events/1")

    assert response.status_code == 200
    assert response.json()["title"] == "event_d"


def test_non_integer_returns_400(client):
    response = client.get("/api/events/osman")
    assert response.status_code == 400


def test_event_not_found_returns_404(client):
    response = client.get("/api/events/10000")
    assert response.status_code == 404


def test_event_organiser_can_see_all_attendees(client):
    token = create_access_token(3)
    response = client.get(
        "/api/events/5/attendees",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert {attendee["id"] for attendee in response.json()["attendees"]} == {1, 2, 3}


def test_non_organiser_cannot_see_event_attendees(client, auth_headers):
    response = client.get("/api/events/5/attendees", headers=auth_headers)

    assert response.status_code == 403


def test_attendees_for_missing_event_returns_404(client, auth_headers):
    response = client.get("/api/events/10000/attendees", headers=auth_headers)

    assert response.status_code == 404


def test_create_event_uses_authenticated_user(client, auth_headers, db_cleanup):
    payload = event_payload()
    payload["organiser_id"] = 2
    db_cleanup("DELETE FROM events WHERE title = %s", (payload["title"],))

    response = client.post("/api/events", json=payload, headers=auth_headers)

    assert response.status_code == 201
    event = response.json()["event"]
    assert event["title"] == payload["title"]
    assert event["organiser_id"] == 1
    assert event["venue_id"] == payload["venue_id"]
    assert datetime.fromisoformat(event["starts_at"]).astimezone(timezone.utc) == datetime(
        2025, 8, 15, 18, 0, tzinfo=timezone.utc
    )
    assert datetime.fromisoformat(event["ends_at"]).astimezone(timezone.utc) == datetime(
        2025, 8, 15, 21, 0, tzinfo=timezone.utc
    )


def test_create_event_requires_authentication(client):
    response = client.post("/api/events", json=event_payload())

    assert response.status_code == 401


def test_create_event_rejects_invalid_token(client):
    response = client.post(
        "/api/events",
        json=event_payload(),
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "missing_field",
    ["title", "description", "starts_at", "ends_at", "venue_id"],
)
def test_create_event_rejects_missing_fields(client, auth_headers, missing_field):
    payload = event_payload()
    payload.pop(missing_field)

    response = client.post("/api/events", json=payload, headers=auth_headers)

    assert response.status_code == 400


@pytest.mark.parametrize(
    ("field", "value"),
    [("starts_at", "not-a-date"), ("venue_id", "not-an-integer")],
)
def test_create_event_rejects_malformed_fields(client, auth_headers, field, value):
    payload = event_payload()
    payload[field] = value

    response = client.post("/api/events", json=payload, headers=auth_headers)

    assert response.status_code == 400


