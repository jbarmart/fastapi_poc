from typing import Optional

from fastapi import HTTPException, Header
from fastapi.testclient import TestClient

from main import app, get_db_session, verify_token

testing_db = ["DB for testing"]


def get_testing_db():
    print("GETTING TESTING DB")
    return testing_db


def override_verify_token(token: Optional[str] = Header(None)):
    print("CHECKING TOKEN")
    if token != "your-override-token":
        raise HTTPException(status_code=403, detail="Invalid token or token missing")
    return token


app.dependency_overrides[get_db_session] = get_testing_db
app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)


def test_pass_item_should_add_to_database():
    header = {"token": "your-override-token"}
    response = client.get(
        "/add-item/?item=sugar", headers=header,
    )
    assert response.status_code == 200
    assert response.text == '{"message":"added item sugar"}'
    assert header["token"] == "your-override-token"


def test_error_item_should_add_to_database():
    header = {"token": "your-expected-token"}
    response = client.get(
        "/add-item/?item=sugar", headers=header,
    )
    assert response.status_code == 403
