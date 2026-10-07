from playwright.sync_api import Page, expect
from torch import addr

from tests.data_constants import (
    CHECKOUT_PRODUCT_1_LINK,
    CHECKOUT_PRODUCT_2_LINK,
    )

from pages.checkout_page import CheckoutPage

def test_standard_shipping_is_free_at_exactly_50(logged_in_page: Page):
    # 1. Login 
    page = logged_in_page

    # 2. Add products to cart to reach exactly $50
    page.get_by_role("link", name=CHECKOUT_PRODUCT_1_LINK).click()
    page.get_by_role("button", name="Add to cart").click()

    page.get_by_role("link", name="← Back to shop").click()

    page.get_by_role("link", name=CHECKOUT_PRODUCT_2_LINK, exact=True).click()
    page.get_by_role("button", name="Add to cart").click()

    # 3. Proceed to checkout
    page.get_by_role("link", name="Cart").click()
    page.get_by_role("link", name="Checkout").click()

    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_details(
        "Tyler B",
        "B@b",
        "123 street",
        "Union",
        "07006"
    )

    # Select standard shipping
    page.get_by_role("radio", name="Standard Free at $50+;").check()

    # Verify the test setup reached exactly $50.00
    subtotal_row = page.get_by_text("Subtotal", exact=True).locator("xpath=..").first
    expect(subtotal_row).to_contain_text("$50.00")

    # Verify Standard shipping is free at exactly $50.00
    shipping_row = page.get_by_text("Shipping", exact=True).locator("xpath=..").first
    expect(shipping_row).to_contain_text("$0.00")

