import pytest
from app import shipping_cost


@pytest.mark.parametrize(
    "subtotal, method, expected",
    [
        (4999, "standard", 600),
        (5000, "standard", 0),
        (5001, "standard", 0),
        (4999, "express", 1500),
        (5000, "express", 1500),
    ],
)
def test_shipping_cost(subtotal, method, expected):
    assert shipping_cost(subtotal, method) == expected