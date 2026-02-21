import pytest
from playwright.sync_api import expect

from pom.sunscreen_page import SunscreenPage


@pytest.mark.parametrize("spf", ["SPF-50", "SPF-30"])
def test_add_cheapest(sunscreen_page, spf):
    # Given
    sp = SunscreenPage(sunscreen_page)
    all_products = sp.get_products_with_spf(spf)
    expected_min_price = min(price for _, price in all_products)

    # When
    name, price = sp.add_cheapest_with_spf(spf)

    # Then
    assert spf.lower() in name.lower()
    assert price == expected_min_price
    expect(sp.cart_count).to_have_text("1 item(s)")
