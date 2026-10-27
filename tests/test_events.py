import json 

def test_len_of_events_is_correct(client):
    response = client.get("/events")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 10

def test_returns_correct_event(client):
    response = client.get("/events/1")
   
    assert response.status_code == 200
    assert response.json()["title"] == "Leeds Tech Meetup – June Edition"


def test_non_integer_returns_400(client):
    response = client.get("/events/osman")
    assert response.status_code == 400
   

def test_event_not_found_returns_404(client):
    response = client.get("/events/10000")
    assert response.status_code == 404
