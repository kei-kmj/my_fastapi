from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "What your name ?"}


def test_read_student():
    response = client.get("/students/")
    assert response.status_code == 200
    assert response.json() == {
        "1": {"name": "john", "age": 17, "course": "advance"},
        "2": {"name": "carl", "age": 16, "course": "basic"},
    }


def test_read_student_detail():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json() == {"name": "john", "age": 17, "course": "advance"}


def test_read_student_detail_error():
    response = client.get("/students/8")
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found"}


def test_get_student_by_name_error():
    response = client.get("/get_by_name?name=jane")
    assert response.status_code == 200
    assert response.json() == {"Data": "Data not found"}


def test_create_student():
    response = client.post(
        "/students/3",
        json={"name": "tommy", "age": 18, "course": "basic"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "tommy",
        "age": 18,
        "course": "basic",
    }


def test_create_student_error():
    response = client.post(
        "/students/1",
        json={"name": "john", "age": 17, "course": "advance"},
    )
    assert response.status_code == 200
    assert response.json() == {"Error": "Student exists"}


def test_get_student():
    response = client.get("/get_by_name?name=john")
    assert response.status_code == 200
    assert response.json() == {
        "name": "john",
        "age": 17,
        "course": "advance",
    }


def test_update_student():
    response = client.put(
        "/students/1",
        json={"name": "john", "age": 17, "course": "graduate"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "john",
        "age": 17,
        "course": "graduate",
    }


def test_update_student_error():
    response = client.put(
        "/students/5",
        json={"name": "john", "age": 17, "course": "graduate"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found"}


def test_delete_student():
    response = client.delete("/delete_student/1")
    assert response.status_code == 200
    assert response.json() == {"Message": "Student deleted successfully"}


def test_delete_student_error():
    response = client.delete("/delete_student/5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found"}
