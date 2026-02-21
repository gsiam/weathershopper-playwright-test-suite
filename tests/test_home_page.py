import re

import pytest
from playwright.sync_api import expect

from pom.home_page import HomePage

pytestmark = pytest.mark.smoke


def test_buy_button_click(home_page):
    # Given
    hp = HomePage(home_page)
    temp = hp.get_temperature()
    button = hp.buy_moisturizers_button if temp < HomePage.WINTER_THRESHOLD else hp.buy_sunscreens_button
    expected_url = re.compile(r"/moisturizer$" if temp < HomePage.WINTER_THRESHOLD else r"/sunscreen$")

    # When
    button.click()

    # Then
    expect(home_page).to_have_url(expected_url)
