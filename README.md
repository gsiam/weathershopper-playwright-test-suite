# Weather Shopper — Test Automation

Automated test suite for [Weather Shopper](http://weathershopper.pythonanywhere.com).

## Stack

- [Playwright](https://playwright.dev/python/) — browser automation
- [pytest](https://docs.pytest.org/) + [pytest-playwright](https://playwright.dev/python/docs/test-runners) — test runner and fixtures
- [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures) — retry support for known environmental flakiness
- Python 3.10

## Structure

```text
pom/                        # Page Object Models
  home_page.py
  moisturizer_page.py
  sunscreen_page.py
  cart_page.py
tests/
  test_home_page.py         # temperature-driven routing
  test_moisturizer_page.py  # product page interactions
  test_sunscreen_page.py
  test_cart_page.py         # cart state and totals
  test_e2e.py               # full purchase flows
conftest.py                 # shared fixtures
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Running tests

```bash
# All tests
pytest -v

# Product and cart tests only (no payment)
pytest -m "not e2e" -v

# E2e tests only
pytest -m e2e -v
```

## Design decisions

**Product filtering is dynamic.** Rather than hardcoding expected product names,
the suite selects by ingredient or SPF substring at runtime. This validates the
business rule (cheapest aloe, cheapest SPF-50, etc.) rather than a fixed product
position, which changes on every page load.

**Homepage routing is covered with a lightweight smoke test.** The site randomises
the temperature on each load (1–18 °C or 35–49 °C). A single test reads the
rendered temperature, clicks the correct buy button, and asserts the URL. This
validates the routing rule without running a full purchase. Because the temperature
is random, only one branch is exercised per run; both paths are covered
deterministically by the direct purchase tests.

**E2E tests use `pytest.mark.flaky(reruns=1)`.** The site's payment screen fails
5% of the time by design, simulating real-world payment processor unreliability.
The `flaky` marker retries once on failure, reducing the false alarm rate from 5%
to 0.25%. Two consecutive failures are treated as a genuine regression.
