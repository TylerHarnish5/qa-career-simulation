import sqlite3


def test_order_totals_are_internally_consistent():
    connection = sqlite3.connect("store.db")

    orders = connection.execute(
        """
        SELECT id, subtotal_cents, shipping_cents, total_cents
        FROM orders
        """
    ).fetchall()

    connection.close()

    for order_id, subtotal, shipping, total in orders:
        assert total == subtotal + shipping, (
            f"Order {order_id}: "
            f"{subtotal} + {shipping} != {total}"
        )

def test_standard_shipping_fee_is_free_at_50_and_up():
    connection = sqlite3.connect("store.db")

    orders = connection.execute(
        """
        SELECT id, subtotal_cents, shipping_cents
        FROM orders
        WHERE shipping_method = 'standard'
            AND subtotal_cents >= 5000
        """
    ).fetchall()

    connection.close()

    for order_id, subtotal, shipping in orders:
        assert shipping == 0, (
            f"Order {order_id}: standard shipping should be free "
            f"for {subtotal}, but shipping was {shipping}"
        )

def test_order_subtotal_matches_order_items():
    connection = sqlite3.connect("store.db")

    mismatches = connection.execute(
        """
        SELECT
            orders.id,
            orders.subtotal_cents,
            SUM(order_items.quantity * order_items.unit_price_cents)
        FROM orders
        JOIN order_items
            ON orders.id = order_items.order_id
        GROUP BY orders.id, orders.subtotal_cents
        HAVING orders.subtotal_cents
            != SUM(order_items.quantity * order_items.unit_price_cents)
        """
    ).fetchall()

    connection.close()

    assert not mismatches, (
        f"Orders with incorrect stored subtotals: {mismatches}"
    )
