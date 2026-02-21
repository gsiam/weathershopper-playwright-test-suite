import pytest
from playwright.sync_api import expect

from pom.moisturizer_page import MoisturizerPage


@pytest.mark.parametrize("ingredient", ["aloe", "almond"])
def test_add_cheapest(moisturizer_page, ingredient):
    # Given
    mp = MoisturizerPage(moisturizer_page)
    all_products = mp.get_products_with_ingredient(ingredient)
    expected_min_price = min(price for _, price in all_products)

    # When
    name, price = mp.add_cheapest_with_ingredient(ingredient)

    # Then
    assert ingredient.lower() in name.lower()
    assert price == expected_min_price
    expect(mp.cart_count).to_have_text("1 item(s)")
