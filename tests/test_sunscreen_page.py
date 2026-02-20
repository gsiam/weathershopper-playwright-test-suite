import pytest
from playwright.sync_api import expect

from pom.sunscreen_page import SunscreenPage


@pytest.mark.parametrize("spf", ["SPF-50", "SPF-30"])
def test_add_cheapest(sunscreen_page, spf):
    page = sunscreen_page
    sp = SunscreenPage(page)

    # When
    sp.add_cheapest_with_spf(spf)

    # Then
    expect(sp.cart_count).to_have_text("1 item(s)")
