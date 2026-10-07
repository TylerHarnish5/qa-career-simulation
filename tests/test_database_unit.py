from unittest.mock import MagicMock

from flask import g

from app import app, close_db


def test_close_db_closes_existing_connection():
    fake_connection = MagicMock()

    with app.app_context():
        g.db = fake_connection

        close_db(None)

        fake_connection.close.assert_called_once()