from playwright.sync_api import Page

from tests.data_constants import (
    SEARCH_TERM,
    EXPECTED_SEARCH_PRODUCT,
)

def test_product_description_search(logged_in_page: Page):
    # 1. Open the application
    page = logged_in_page

    # 2. Search using a word found only in the product description
    page.get_by_label("Search products").fill(SEARCH_TERM)
    page.get_by_role("button", name="Apply").click()

    # 3. Verify the correct product appears
    assert page.get_by_text(EXPECTED_SEARCH_PRODUCT).is_visible()