"""Test server behavior."""


def test_get_status_message(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Harper"}
