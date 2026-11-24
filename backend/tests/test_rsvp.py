def test_create_rsvp_requires_authentication(client):
    response = client.post("/events/1/rsvp")

    assert response.status_code == 401

def test_create_rsvp_rejects_invalid_token(client):
    response = client.post(
        "/events/1/rsvp",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401

def test_create_rsvp(client, auth_headers, db_cleanup):
    db_cleanup(
        "DELETE FROM rsvps WHERE attendee_id = %s AND event_id = %s",
        (1, 1),
    )
    response = client.post("/events/1/rsvp", headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["rsvp"]["attendee_id"] == 1
    assert response.json()["rsvp"]["event_id"] == 1

def test_create_duplicate_rsvp_returns_409(client, auth_headers, db_cleanup):
    db_cleanup(
        "DELETE FROM rsvps WHERE attendee_id = %s AND event_id = %s",
        (1, 4),
    )
    first_response = client.post("/events/4/rsvp", headers=auth_headers)
    second_response = client.post("/events/4/rsvp", headers=auth_headers)

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_create_rsvp_for_missing_event_returns_404(client, auth_headers):
    response = client.post("/events/99999/rsvp", headers=auth_headers)

    assert response.status_code == 404

def test_delete_rsvp_returns_204_and_then_409(client, auth_headers, db_cleanup):
    db_cleanup(
        "DELETE FROM rsvps WHERE attendee_id = %s AND event_id = %s",
        (1, 2),
    )
    create_response = client.post("/events/2/rsvp", headers=auth_headers)
    assert create_response.status_code == 201

    delete_response = client.delete("/events/2/rsvp/me", headers=auth_headers)
    repeated_delete_response = client.delete(
        "/events/2/rsvp/me",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204
    assert repeated_delete_response.status_code == 404

def test_delete_rsvp_for_event_you_are_not_in_returns_404(client, auth_headers):
    

    delete_response = client.delete("/events/1/rsvp/me", headers=auth_headers)
    assert delete_response.status_code == 404
   