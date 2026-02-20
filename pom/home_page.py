from playwright.sync_api import Page


class HomePage:
    SUMMER_THRESHOLD = 34
    WINTER_THRESHOLD = 19

    def __init__(self, page: Page):
        self.temperature = page.locator("#temperature")
        self.buy_moisturizers_button = page.get_by_role(
            "button", name="Buy moisturizers"
        )
        self.buy_sunscreens_button = page.get_by_role("button", name="Buy sunscreens")

    def get_temperature(self) -> int:
        return int(self.temperature.inner_text().strip())
