import re

import pytest
from playwright.sync_api import expect

from pom.home_page import HomePage

pytestmark = pytest.mark.smoke


def test_buy_moisturizers_button_click(home_page):
    # When
    hp = HomePage(home_page)
    hp.buy_moisturizers_button.click()

    # Then
    expect(home_page).to_have_url(re.compile(r"/moisturizer$"))


def test_buy_sunscreens_button_click(home_page):
    # When
    hp = HomePage(home_page)
    hp.buy_sunscreens_button.click()

    # Then
    expect(home_page).to_have_url(re.compile(r"/sunscreen$"))
