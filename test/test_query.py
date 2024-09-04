from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_query_yields_10_results():
    with TestClient(app) as client:
        response = client.get("/query?query=a large war in space")
        json_response = response.json()
        
        assert response.status_code == 200
        assert len(json_response["results"]) == 10
        assert json_response["message"] == "OK"

def test_query_yields_few_results():
    response = client.get("/query?query=hitchhiker")
    json_response = response.json()
    
    assert response.status_code == 200
    assert 1 < len(json_response["results"]) < 10
    assert json_response["message"] == "OK"

def test_query_yields_non_obvious_results():
    response = client.get("/query?query=julius cesar")
    json_response = response.json()
    assert response.status_code == 200
    assert len(json_response["results"]) > 0
    assert json_response["message"] == "OK"

    assert not any("birds" in result['content'].lower() for result in json_response['results'])
