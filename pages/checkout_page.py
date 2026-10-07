from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_shipping_details(
        self,
        name,
        email,
        address,
        city,
        postal_code
    ):
        self.page.get_by_role(
            "textbox",
            name="Recipient name"
        ).fill(name)

        self.page.get_by_role(
            "textbox",
            name="Email address"
        ).fill(email)

        self.page.get_by_role(
            "textbox",
            name="Street address"
        ).fill(address)

        self.page.get_by_role(
            "textbox",
            name="City"
        ).fill(city)

        self.page.get_by_role(
            "textbox",
            name="Postal code"
        ).fill(postal_code)

    def select_standard_shipping(self):
        self.page.get_by_role(
            "radio",
            name="Standard Free at $50+;"
        ).check()