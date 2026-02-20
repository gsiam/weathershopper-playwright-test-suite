from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self._page = page
        self.heading = page.get_by_role("heading", name="Checkout")
        self.items_table_rows = page.locator("table tbody tr")
        self.total = page.locator("#total")
        self.pay_button = page.locator("button.stripe-button-el")

    def get_item_names(self) -> list:
        rows = self.items_table_rows
        count = rows.count()
        return [rows.nth(i).locator("td").first.inner_text() for i in range(count)]

    def get_item_prices(self) -> list:
        rows = self.items_table_rows
        count = rows.count()
        return [int(rows.nth(i).locator("td").nth(1).inner_text()) for i in range(count)]

    def get_total_amount(self) -> int:
        text = self.total.inner_text()
        return int(text.split("Rupees")[-1].strip())

    def pay(self, email: str, card: str, expiry: str, cvc: str, zip_code: str) -> None:
        """Fill in the Stripe checkout iframe and submit payment.

        Args:
            email: Any valid email address.
            card: Card number, e.g. '4242 4242 4242 4242'.
            expiry: Expiry in 'MM / YY' format, e.g. '12 / 26'.
            cvc: Three-digit CVC.
            zip_code: Billing ZIP code.
        """
        self.pay_button.click()

        frame = self._page.frame_locator("iframe.stripe_checkout_app")
        frame.get_by_placeholder("Email").fill(email)
        frame.get_by_placeholder("Card number").fill(card)
        frame.get_by_placeholder("MM / YY").fill(expiry)
        # press_sequentially fires keyup events that Stripe's JS needs to reveal the ZIP field
        frame.get_by_placeholder("CVC").press_sequentially(cvc)
        frame.get_by_placeholder("ZIP Code").fill(zip_code)
        frame.get_by_role("button", name="Pay").click()
