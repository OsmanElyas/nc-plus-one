import pytest


def test_profile_returns_authenticated_user(client, auth_headers):
    response = client.get("/api/user/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["user"]["id"] == 1


def test_profile_requires_valid_token(client):
    response = client.get("/api/user/me")

    assert response.status_code == 401


def test_user_events_returns_ranked_events_in_start_order(client, auth_headers):
    response = client.get("/api/user/me/events", headers=auth_headers)

    assert response.status_code == 200
    events = response.json()["events"]
    assert [event["id"] for event in events] == [3, 5]
    assert [event["title"] for event in events] == ["event_e", "event_c"]
    assert [event["event_rank"] for event in events] == [1, 2]
    assert [event["total_rsvps"] for event in events] == [2, 2]
    assert events[0]["starts_at"] < events[1]["starts_at"]


@pytest.mark.parametrize(
    "headers",
    [None, {"Authorization": "Bearer invalid-token"}],
)
def test_user_events_requires_valid_token(client, headers):
    response = client.get("/api/user/me/events", headers=headers)

    assert response.status_code == 401