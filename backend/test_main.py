from fastapi.testclient import TestClient
from main import app

import os

# Set TESTING_MODE to True before running the tests
os.environ["TESTING_MODE"] = "true"

client = TestClient(app)


def test_calc_good_result():
    # case:  3 10 5 + *  -> 45
    data = '["3", "10", "5", "+", "*"]'
    response = client.post("/calc/", content=data)
    assert response.status_code == 200
    assert float(response.text) == 45

    # with order changed
    # case:  10 5 + 3 *  -> 45
    data = '["10", "5", "+", "3", "*"]'
    response = client.post("/calc/", content=data)
    assert response.status_code == 200
    assert float(response.text) == 45


def test_calc_not_enough_operands():
    # case:  3 *  -> Not enough operands for operation
    data = '["3", "*"]'
    response = client.post("/calc/", content=data)
    assert response.text[1: -1] == "Not enough operands for operation"


def test_calc_invalid_items():
    # case:  3a -> Invalid item (check if you have negative integers)
    data = '["3a"]'
    response = client.post("/calc/", content=data)
    assert response.text[1: -1] == "Invalid item (check if you have negative integers)"


def test_calc_invalid_expression():
    # case:  3 4 -> Invalid expression
    data = '["3", "4"]'
    response = client.post("/calc/", content=data)
    assert response.text[1: -1] == "Invalid expression"

    # case:  empty formula string -> Invalid expression
    data = '[]'
    response = client.post("/calc/", content=data)
    assert response.text[1: -1] == "Invalid expression"