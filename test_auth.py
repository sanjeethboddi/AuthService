from fastapi.testclient import TestClient

from main import app


class FakePasswordHasher():
    def hash_password(self, plain_password):
        return plain_password

    def verify_password(self, plain_password, hashed_password):
        return plain_password == hashed_password

class fake_db_collection:
    def find_one(self, query):
        return {"_id": "test", "hashed_password": "test"}
    def insert_one(self, query):
        return {"_id": "test", "hashed_password": "test"}

app.password_hasher = FakePasswordHasher()
app.database = {}
app.database['auth'] = fake_db_collection()



client = TestClient(app)

def test_signup():
    response = client.post("/signup", json={"username":"test", "password":"test"})
    assert response.status_code == 201

def test_login():
    response = client.post("/login", data={"username":"test", "password":"test"})
    assert response.status_code == 200

def test_verify():
    response = client.post("/verify", json={"token":"test"})
    