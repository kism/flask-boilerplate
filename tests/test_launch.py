"""Test launching the app."""

import json

from mycoolapp import create_app

# def test_config():
#     assert not create_app().testing
#     assert create_app({"TESTING": True}).testing


def test_hello(client):
    response = client.get("/hello/")
    # response_dict = response.json
    # print("AAAAAAAAAAAAAAAAAAA")
    # print(data)
    # print("AAAAAAAAAAAAAAAAAAA")

    print(response.json)
    print(type(response.json))

    assert response.json['msg'] == "Hello, World!"
