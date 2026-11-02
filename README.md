# Weather Shopper — Test Automation

Automated test suite for [Weather Shopper](http://weathershopper.pythonanywhere.com).

## Stack

- [Playwright](https://playwright.dev/python/) — browser automation
- [pytest](https://docs.pytest.org/) + [pytest-playwright](https://playwright.dev/python/docs/test-runners) — test runner and fixtures
- [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures) — retry support for known environmental flakiness
- Python 3.14.10 (pinned in `.python-version`)

## Structure

```text
pom/                        # Page Object Models
  home_page.py
  moisturizer_page.py
  sunscreen_page.py
  cart_page.py
tests/
  test_home_page.py         # homepage navigation smoke tests
  test_moisturizer_page.py  # product page interactions
  test_sunscreen_page.py
  test_cart_page.py         # cart state and totals
  test_e2e.py               # full purchase flows
conftest.py                 # shared fixtures
```

## Setup

```bash
pyenv install 3.14.10 --skip-existing
python -V  # should print Python 3.14.10
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Running tests

```bash
# All tests
pytest -v

# Smoke tests
pytest -m smoke -v

# Product and cart tests only (no payment)
pytest -m "not e2e" -v

# E2E tests only
pytest -m e2e -v
```

## Docker (recommended for evaluation)

```bash
# Build
docker build -t weathershopper-tests .

# All tests
docker run --rm weathershopper-tests -v

# Smoke tests
docker run --rm weathershopper-tests -m smoke -v

# Product and cart tests only (no payment)
docker run --rm weathershopper-tests -m "not e2e" -v

# E2E tests only
docker run --rm weathershopper-tests -m e2e -v
```

## Design decisions

**Product filtering is dynamic.** Rather than hardcoding expected product names,
the suite selects by ingredient or SPF substring at runtime. This validates the
business rule (cheapest aloe, cheapest SPF-50, etc.) and guards against two
sources of brittleness: product position changes on every page load, and full
product names may change at any time due to content updates.

**Homepage routing is covered by two smoke tests.** One test per buy button, each
asserting the expected navigation URL. Both buttons are always present regardless
of temperature, so both paths are verified on every run.

**E2E tests use `pytest.mark.flaky(reruns=1)`.** The site's payment screen fails
5% of the time by design, simulating real-world payment processor unreliability.
The `flaky` marker retries once on failure, reducing the false alarm rate from 5%
to 0.25%. Two consecutive failures are treated as a genuine regression.

**Chromium only.** The app has no browser-specific behaviour, so a single engine covers the functional risk. Cross-browser coverage (Firefox, WebKit) could be added via `--browser` parameterisation with no test changes required.
