import subprocess
import sys
import time

import pytest
import requests
from playwright.sync_api import Page

from tests.data_constants import (
    BASE_URL,
    TEST_USERNAME,
    TEST_PASSWORD,
)

from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def live_server():
    def server_is_ready():
        try:
            response = requests.get(
                f"{BASE_URL}/login",
                timeout=2
            )
            return response.status_code < 500
        except requests.RequestException:
            return False

    # If a healthy server is already running, use it.
    if server_is_ready():
        yield
        return

    # Otherwise start Flask ourselves.
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "flask",
            "--app",
            "app",
            "run",
            "--host",
            "127.0.0.1",
            "--port",
            "5000",
            "--no-reload",
        ]
    )

    # Wait for Flask to become responsive.
    for _ in range(50):
        if server_is_ready():
            break

        if process.poll() is not None:
            raise RuntimeError(
                "Flask server exited before becoming ready."
            )

        time.sleep(0.2)
    else:
        process.terminate()
        raise RuntimeError("Flask server did not start.")

    yield

    process.terminate()
    process.wait(timeout=5)


@pytest.fixture
def logged_in_page(live_server, page: Page):
    page.goto(f"{BASE_URL}/login")

    login_page = LoginPage(page)
    login_page.login(TEST_USERNAME, TEST_PASSWORD)

    return page