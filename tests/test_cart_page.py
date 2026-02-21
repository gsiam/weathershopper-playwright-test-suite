import pytest
from playwright.sync_api import expect

from pom.cart_page import CartPage


@pytest.fixture
def cart_page(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "cart_page,keywords",
    [
        ("cart_with_moisturizers", ["aloe", "almond"]),
        ("cart_with_sunscreens", ["spf-50", "spf-30"]),
    ],
    indirect=["cart_page"],
)
def test_items_displayed(cart_page, keywords):
    # Given
    cart = CartPage(cart_page)

    # Then
    expect(cart.heading).to_be_visible()
    item_names = cart.get_item_names()
    assert len(item_names) == 2
    for keyword in keywords:
        assert any(keyword in name.lower() for name in item_names)


@pytest.mark.parametrize(
    "cart_page", ["cart_with_moisturizers", "cart_with_sunscreens"], indirect=True
)
def test_total_matches_sum(cart_page):
    # Given
    cart = CartPage(cart_page)

    # Then
    assert cart.get_total_amount() == sum(cart.get_item_prices())
