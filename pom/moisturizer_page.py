from playwright.sync_api import Page


class MoisturizerPage:

    def __init__(self, page: Page):
        self._page = page
        self.heading = page.get_by_role("heading", name="Moisturizers")
        self.cart_count = page.locator("#cart")

    def add_cheapest_with_ingredient(self, ingredient: str) -> None:
        cards = self._page.locator("div.text-center.col-4")
        count = cards.count()

        cheapest_price = None
        cheapest_add_button = None

        for i in range(count):
            card = cards.nth(i)
            name = card.locator("p.font-weight-bold").inner_text()
            if ingredient.lower() not in name.lower():
                continue

            price_text = card.locator("p:not(.font-weight-bold)").inner_text()
            price = int(price_text.replace("Price:", "").replace("Rs.", "").strip())

            if cheapest_price is None or price < cheapest_price:
                cheapest_price = price
                cheapest_add_button = card.get_by_role("button", name="Add")

        if cheapest_add_button is None:
            raise ValueError(f"No moisturizer found containing '{ingredient}'")

        cheapest_add_button.click()

    def go_to_cart(self) -> None:
        self.cart_count.click()
