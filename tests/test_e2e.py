import re
from datetime import date

import pytest
from playwright.sync_api import expect

from pom.cart_page import CartPage
from pom.moisturizer_page import MoisturizerPage
from pom.sunscreen_page import SunscreenPage

pytestmark = [pytest.mark.e2e, pytest.mark.flaky(reruns=1)]

EMAIL = "test@example.com"
CARD = "4242 4242 4242 4242"
EXPIRY = date.today().replace(year=date.today().year + 2).strftime("%m / %y")
CVC = "123"
ZIP = "12345"


def test_moisturizer_purchase(page):
    # Given
    page.goto("/moisturizer")
    mp = MoisturizerPage(page)

    # When
    mp.add_cheapest_with_ingredient("aloe")
    mp.add_cheapest_with_ingredient("almond")
    mp.go_to_cart()
    CartPage(page).pay(EMAIL, CARD, EXPIRY, CVC, ZIP)

    # Then
    expect(page).to_have_url(re.compile(r"/confirmation$"))


def test_sunscreen_purchase(page):
    # Given
    page.goto("/sunscreen")
    sp = SunscreenPage(page)

    # When
    sp.add_cheapest_with_spf("SPF-50")
    sp.add_cheapest_with_spf("SPF-30")
    sp.go_to_cart()
    CartPage(page).pay(EMAIL, CARD, EXPIRY, CVC, ZIP)

    # Then
    expect(page).to_have_url(re.compile(r"/confirmation$"))
