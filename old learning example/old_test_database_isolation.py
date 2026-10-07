#
# THIS IS JUST PROOF OF CONCEPT (isolation).
# DOES NOT FURTHER THE APPLICATION.
#

import sqlite3
import pytest


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_store.db"

    connection = sqlite3.connect(db_path)

    connection.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            shipping_method TEXT,
            shipping_cents INTEGER,
            subtotal_cents INTEGER,
            total_cents INTEGER
        )
        """
    )

    connection.execute(
        """
        INSERT INTO orders (
            id,
            shipping_method,
            shipping_cents,
            subtotal_cents,
            total_cents
        )
        VALUES (1, 'standard', 0, 5000, 5000)
        """
    )

    connection.commit()

    yield connection

    connection.close()


def test_standard_shipping_is_free_at_50(test_db):
    order = test_db.execute(
        """
        SELECT subtotal_cents, shipping_cents, total_cents
        FROM orders
        WHERE id = 1
        """
    ).fetchone()

    subtotal, shipping, total = order

    assert subtotal == 5000
    assert shipping == 0
    assert total == 5000

def test_detects_invalid_standard_shipping_charge(test_db):
    test_db.execute(
        """
        INSERT INTO orders (
            id,
            shipping_method,
            shipping_cents,
            subtotal_cents,
            total_cents
        )
        VALUES (2, 'standard', 600, 5000, 5600)
        """
    )

    test_db.commit()

    invalid_orders = test_db.execute(
        """
        SELECT id, subtotal_cents, shipping_cents
        FROM orders
        WHERE shipping_method = 'standard'
          AND subtotal_cents >= 5000
          AND shipping_cents != 0
        """
    ).fetchall()

    assert len(invalid_orders) == 1
    assert invalid_orders[0][0] == 2