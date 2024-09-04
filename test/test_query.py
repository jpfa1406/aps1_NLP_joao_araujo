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
    with TestClient(app) as client:
        response = client.get("/query?query=hitchhiker")
        json_response = response.json()
        
        assert response.status_code == 200
        assert 1 < len(json_response["results"]) < 10
        assert json_response["message"] == "OK"

def test_query_yields_non_obvious_results():
    with TestClient(app) as client:
        response = client.get("/query?query=julius cesar")
        json_response = response.json()

        assert response.status_code == 200
        found_valid_book = False  # Flag to check if we found at least one valid book

        for result in json_response["results"]:
            genres = [genre.strip().lower() for genre in result["Genere"].split(',')]  # Split and clean genres
            
            # Check if "history" or "time travel" is NOT in the genres
            if "history" not in genres and "time travel" not in genres:
                found_valid_book = True
                print(f"Valid book found: {result['title']}")
                break  # Exit the loop once we find a valid book

        # Assert that we found at least one book without "history" or "time travel"
        assert found_valid_book, "No books without 'history' or 'time travel' found."
