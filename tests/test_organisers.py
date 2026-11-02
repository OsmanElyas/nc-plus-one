import pytest

from app.auth.jwt import create_access_token


def test_get_organiser_stats(client, auth_headers):
    response = client.get("/organisers/2/stats", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["stats"] == {
        "organiser_id": 2,
        "name": "user_a",
        "total_events": 2,
        "avg_attendance": 0.5,
        "best_attended_count": 1,
        "organiser_rank": 1,
    }


def test_organiser_rank_is_global(client, auth_headers):
    response = client.get("/organisers/1/stats", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["stats"]["organiser_rank"] == 3


@pytest.mark.parametrize("token", [None, "invalid-token"])
def test_get_organiser_stats_requires_valid_token(client, token):
    headers = {} if token is None else {"Authorization": f"Bearer {token}"}
    response = client.get("/organisers/2/stats", headers=headers)

    assert response.status_code == 401


def test_get_missing_organiser_stats_returns_404(client, auth_headers):
    response = client.get("/organisers/99999/stats", headers=auth_headers)

    assert response.status_code == 404