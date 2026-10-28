import json 

def test_len_of_events_is_correct(client, auth_headers):
    response = client.get("/events", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["events"]) == 5

def test_returns_correct_event(client, auth_headers):
    response = client.get("/events/1", headers=auth_headers)
   
    assert response.status_code == 200
    assert response.json()["title"] == "event_d"


def test_non_integer_returns_400(client, auth_headers):
    response = client.get("/events/osman", headers=auth_headers)
    assert response.status_code == 400
   

def test_event_not_found_returns_404(client, auth_headers):
    response = client.get("/events/10000", headers=auth_headers)
    assert response.status_code == 404
