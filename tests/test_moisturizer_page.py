import pytest
from playwright.sync_api import expect

from pom.moisturizer_page import MoisturizerPage


@pytest.mark.parametrize("ingredient", ["aloe", "almond"])
def test_add_cheapest(moisturizer_page, ingredient):
    page = moisturizer_page
    mp = MoisturizerPage(page)

    # When
    mp.add_cheapest_with_ingredient(ingredient)

    # Then
    expect(mp.cart_count).to_have_text("1 item(s)")
