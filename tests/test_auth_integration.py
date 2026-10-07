import requests

import re #for the deimal quanitity becoming 1 test

from tests.data_constants import (
    BASE_URL,
    TEST_USERNAME,
    TEST_PASSWORD,
    TEST_PRODUCT_ID,
    TEST_PRODUCT_NAME,
)

def test_orders_requires_authentication(live_server):
    response = requests.get(
        f"{BASE_URL}/orders",
        allow_redirects=False
    )

    print("Status:", response.status_code)
    print("Location:", response.headers.get("Location"))

    assert response.status_code in (301, 302, 303, 307, 308)
    assert response.headers.get("Location") == "/login"


def test_invalid_login_does_not_authenticate(live_server):
    session = requests.Session()

    login_response = session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": "incorrect_password"
        }
    )

    orders_response = session.get(
        f"{BASE_URL}/orders",
        allow_redirects=False
    )
    
    print("Login status:", login_response.status_code)
    print("Orders status:", orders_response.status_code)
    print("Orders redirect:", orders_response.headers.get("Location"))

    assert orders_response.status_code in (301, 302, 303, 307, 308)
    assert orders_response.headers.get("Location") == "/login"


def test_valid_login_authenticates_session(live_server):
    session = requests.Session()

    # Submit invalid login form data
    login_response = session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
    )

    # Attempt to access the protected /orders route after invalid login
    orders_response = session.get(
        f"{BASE_URL}/orders",
        allow_redirects=False
    )
    
    print("Login status:", login_response.status_code)
    print("Orders status:", orders_response.status_code)

    assert orders_response.status_code == 200


def test_add_products_to_cart(live_server):
    session = requests.Session()

    # Log in
    session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
    )

    # Add product ID (5 currently), quantity 1
    add_response = session.post(
        f"{BASE_URL}/cart/add/{TEST_PRODUCT_ID}",
        data={
            "quantity": "1"
        },
        allow_redirects=False
    )

    print("Add-to-cart status:", add_response.status_code)
    print("Redirect:", add_response.headers.get("Location"))

    # Now request the cart using the same session
    cart_response = session.get(
        f"{BASE_URL}/cart"
    )

    print("Cart status:", cart_response.status_code)

    assert cart_response.status_code == 200
    assert TEST_PRODUCT_NAME in cart_response.text


def test_cart_rejects_zero_quantity(live_server):
    session = requests.Session()

    # Log in
    session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
    )

    # Add product ID (5 currently), quantity 1
    add_response = session.post(
        f"{BASE_URL}/cart/add/{TEST_PRODUCT_ID}",
        data={
            "quantity": "0"
        },
        allow_redirects=False
    )

    print("Add-to-cart status:", add_response.status_code)
    print("Redirect:", add_response.headers.get("Location"))

    # Now request the cart using the same session
    cart_response = session.get(
        f"{BASE_URL}/cart"
    )

    print("Cart status:", cart_response.status_code)

    assert cart_response.status_code == 200
    assert TEST_PRODUCT_NAME not in cart_response.text


def test_decimal_quantity_does_not_become_one(live_server):
    session = requests.Session()

    # Log in
    session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
    )

    # Add product ID (5 currently), quantity 1
    session.post(
        f"{BASE_URL}/cart/add/{TEST_PRODUCT_ID}",
        data={
            "quantity": "5.00"
        },
    )

    # Now request the cart using the same session
    cart_response = session.get(
        f"{BASE_URL}/cart"
    )

    match = re.search(
        rf'action="/cart/update/{TEST_PRODUCT_ID}".*?value="(\d+)"',
        cart_response.text
    )

    assert match is not None
    assert match.group(1) != "1"