from unittest.mock import MagicMock, patch

from app import app, cart_lines

from flask import session

from tests.data_constants import (
    TEST_PRODUCT_ID
)

def test_cart_lines_calculates_line_total_and_subtotal():
    # Fake product returned by the database
    fake_product = {
        "id": TEST_PRODUCT_ID,
        "price_cents": 1600
    }

    # Fake database behavior
    fake_db = MagicMock()
    fake_db.execute.return_value.fetchall.return_value = [fake_product]

    with app.test_request_context():

        # Pretend the user's cart contains 2 of product 5
        session["cart"] = {
            str(TEST_PRODUCT_ID): 2
        }

        # Temporarily replace get_db() with our fake database
        with patch("app.get_db", return_value=fake_db):
            lines, subtotal = cart_lines()

    assert len(lines) == 1
    assert lines[0]["quantity"] == 2
    assert lines[0]["line_total"] == 3200
    assert subtotal == 3200

def test_cart_lines_empty_cart():
    with app.test_request_context():
        session["cart"] = {}

        lines, subtotal = cart_lines()

    assert lines == []
    assert subtotal == 0