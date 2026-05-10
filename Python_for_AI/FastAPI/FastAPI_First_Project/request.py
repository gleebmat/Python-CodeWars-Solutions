import requests
import json
import uuid


def send_test_event():
    url = "http://localhost:8000/events/"

    event_data = {
        "event_id": str(uuid.uuid4()),
        "event_type": "test_event",
        "event_data": {"message": "Can you explain how to use FastAPI?"},
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url=url, data=json.dumps(event_data), headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Full Response Headers: {response.headers}")

    if __name__ == "__main__":
        send_test_event()
