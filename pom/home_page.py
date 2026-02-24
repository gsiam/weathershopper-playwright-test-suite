from playwright.sync_api import Page


class HomePage:

    def __init__(self, page: Page):
        self.buy_moisturizers_button = page.get_by_role(
            "button", name="Buy moisturizers"
        )
        self.buy_sunscreens_button = page.get_by_role("button", name="Buy sunscreens")
