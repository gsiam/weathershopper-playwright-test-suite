import pytest
from playwright.sync_api import expect

from pom.cart_page import CartPage


@pytest.fixture
def cart_page(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("cart_page", ["cart_with_moisturizers", "cart_with_sunscreens"], indirect=True)
def test_items_displayed(cart_page):
    # Given
    cart = CartPage(cart_page)

    # Then
    expect(cart.heading).to_be_visible()
    assert cart.items_table_rows.count() == 2


@pytest.mark.parametrize("cart_page", ["cart_with_moisturizers", "cart_with_sunscreens"], indirect=True)
def test_total_matches_sum(cart_page):
    # Given
    cart = CartPage(cart_page)

    # Then
    assert cart.get_total_amount() == sum(cart.get_item_prices())
