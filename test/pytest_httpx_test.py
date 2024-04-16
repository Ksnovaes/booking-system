import httpx
import pytest
from pytest_httpx import HTTPXMock

form_data = {
        "name": "Kaua",
        "email": "kaua@example.com",
        "number": "61-99999-9999",
        "in_date": "2012-04-23",
        "out_date": "2013-04-23"
    }

form_data2 = {
        "user": "Kaua",
        "email": "kaua@example.com",
        "password": "123456",
        "confirm_password": "123456"
    }

def test_form_post_route(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "success"}, method="POST")

    with httpx.Client() as client:
        response = client.post("http://127.0.0.1:7777", data=form_data)
        assert response.status_code == 200
        assert response.json() == {
            "status": "success"
        }

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    
def test_form_get_route(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=form_data, method="GET")

    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:7777")
        assert response.status_code == 200
        assert response.json() == form_data
    
    
    requests = httpx_mock.get_requests()
    assert len(requests) == 1


def test_redirect_to_create_account(httpx_mock: HTTPXMock):
    with open("templates/result.html", "r", encoding="UTF-8") as file:
        expected_html = file.read()
    
    httpx_mock.add_response(content=expected_html)

    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:7777/result")
        assert response.status_code == 200

    with httpx.Client() as client:
        client.get("http://127.0.0.1:7777/result")
        button_click_script = "document.querySelector('.verify').click();"
        client.execute_script = (button_click_script)
    
    httpx_mock.get_requests()

def test_account_post_route(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "success"}, method="POST")
    
    with httpx.Client() as client:
        response = client.post("http://127.0.0.1:7777/account", data=form_data2)
        assert response.status_code == 200
        assert response.json() == {
            "status": "success"
        }

    requests = httpx_mock.get_requests()
    assert len(requests) == 1

def test_account_get_route(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=form_data2, method="GET")

    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:7777/success")
        assert response.status_code == 200
        assert response.json() == form_data2
    
    httpx_mock.get_requests()





