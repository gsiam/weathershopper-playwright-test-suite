from playwright.sync_api import Page

from pom.product import Product


class SunscreenPage:

    def __init__(self, page: Page):
        self._page = page
        self.heading = page.get_by_role("heading", name="Sunscreens")
        self.cart_count = page.locator("#cart")

    def _collect_products(self, spf: str) -> list:
        cards = self._page.locator("div.text-center.col-4")
        count = cards.count()
        if count == 0:
            raise RuntimeError(
                "No product cards found — page may not have loaded or locator is wrong"
            )
        result = []
        for i in range(count):
            card = cards.nth(i)
            name = card.locator("p.font-weight-bold").inner_text()
            if spf.lower() not in name.lower():
                continue
            price_text = card.locator("p:not(.font-weight-bold)").inner_text()
            price = int(price_text.replace("Price:", "").replace("Rs.", "").strip())
            result.append((name, price, card.get_by_role("button", name="Add")))
        return result

    def get_products_with_spf(self, spf: str) -> list[Product]:
        return [Product(name, price) for name, price, _ in self._collect_products(spf)]

    def add_cheapest_with_spf(self, spf: str) -> Product:
        products = self._collect_products(spf)
        if not products:
            raise ValueError(f"No sunscreen found with SPF rating '{spf}'")
        name, price, button = min(products, key=lambda p: p[1])
        button.click()
        return Product(name, price)

    def go_to_cart(self) -> None:
        self.cart_count.click()
