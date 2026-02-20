import pytest

from pom.moisturizer_page import MoisturizerPage
from pom.sunscreen_page import SunscreenPage


@pytest.fixture
def home_page(page):
    page.goto("/")
    yield page


@pytest.fixture
def moisturizer_page(page):
    page.goto("/moisturizer")
    yield page


@pytest.fixture
def sunscreen_page(page):
    page.goto("/sunscreen")
    yield page


@pytest.fixture
def cart_with_moisturizers(page):
    page.goto("/moisturizer")
    mp = MoisturizerPage(page)
    mp.add_cheapest_with_ingredient("aloe")
    mp.add_cheapest_with_ingredient("almond")
    mp.go_to_cart()
    yield page


@pytest.fixture
def cart_with_sunscreens(page):
    page.goto("/sunscreen")
    sp = SunscreenPage(page)
    sp.add_cheapest_with_spf("SPF-50")
    sp.add_cheapest_with_spf("SPF-30")
    sp.go_to_cart()
    yield page
