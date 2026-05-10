# AdNabu Shopify Test Automation Framework

A **Python + Selenium WebDriver** end-to-end test automation framework for the [AdNabu Shopify Store](https://adnabu-store-assignment1.myshopify.com), built with **pytest**, **Page Object Model (POM)**, and **data-driven testing** principles.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Test Coverage](#test-coverage)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Reports](#test-reports)
- [Framework Design](#framework-design)

---

## Project Overview

This framework automates functional test scenarios for an e-commerce Shopify store, covering two core feature areas:

- **Product Search** — exact, partial, case-insensitive, invalid, and edge case inputs
- **Add to Cart** — quantity updates, price calculations, sold-out handling, and cart persistence

The framework follows a clean separation of concerns: page objects handle UI interactions, test classes handle assertions, JSON files supply test data, and utility classes provide reusable driver and Selenium helpers.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Browser Automation | Selenium WebDriver 4.x |
| Test Runner | pytest |
| Design Pattern | Page Object Model (POM) |
| Test Data | JSON (data-driven) |
| Driver Management | WebDriver Manager |
| Reporting | pytest-html |
| Supported Browsers | Chrome, Firefox |

---

## Project Structure

```
AdNabuTestStore/
│
├── pages/                        # Page Object classes
│   ├── login_page.py             # Login page interactions
│   ├── product_search_page.py    # Search bar, results, and validation
│   └── add_to_cart_page.py       # Product page and cart drawer interactions
│
├── tests/                        # Test classes
│   ├── test_product_search.py    # Product search test scenarios
│   └── test_add_to_cart.py       # Add to cart test scenarios
│
├── test_data/                    # External test data (JSON)
│   ├── product_search.json       # Search inputs (positive, negative, edge cases)
│   └── add_to_cart.json          # Cart test product names
│
├── utils/                        # Shared utilities
│   ├── selenium_utils.py         # Reusable Selenium wrapper methods
│   ├── driver_factory.py         # Browser driver instantiation
│   └── data_loader.py            # JSON test data loader
│
├── reports/                      # Auto-generated HTML test reports
│   └── report.html
│
├── config.ini                    # App URL, browser, and credentials config
├── conftest.py                   # pytest fixtures (driver setup, login, config)
├── pytest.ini                    # pytest configuration and addopts
└── requirements.txt              # Python dependencies
```

---

## Test Coverage

📄 **Detailed Test Case Document:** [docs/AdNabu_Test_Cases.xlsx](docs/AdNabu_Test_Cases.xlsx)

### Product Search — `test_product_search.py`

| # | Test Case | Type |
|---|---|---|
| 1 | Search with exact product name | Positive |
| 2 | Search with partial product keyword | Positive |
| 3 | Search with mixed-case product name | Positive |
| 4 | Search for a non-existing product | Negative |
| 5 | Search using only numbers | Negative |
| 6 | Search with combination of letters, numbers, and special characters | Negative |
| 7 | Search with XSS script input | Edge Case |
| 8 | Search with very long character input | Edge Case |

### Add to Cart — `test_add_to_cart.py`

| # | Test Case | Type |
|---|---|---|
| 1 | Increase quantity — item total and subtotal reflect correctly | Positive |
| 2 | Increase quantity — item total equals unit price × quantity | Positive |
| 3 | Decrease quantity — item total and subtotal reflect correctly | Positive |
| 4 | Add out-of-stock product — Sold Out button is disabled | Negative |
| 5 | Buy Now on out-of-stock product — no navigation occurs | Negative |
| 6 | Minus button disabled at minimum quantity (qty = 1) | Negative |
| 7 | Cart badge count updates correctly after adding product | Edge Case |
| 8 | Cart contents persist after page refresh | Edge Case |

---

## Prerequisites

- Python 3.8 or higher
- Google Chrome or Mozilla Firefox installed
- pip (Python package manager)

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/AdNabuTestStore.git
cd AdNabuTestStore
```

**2. Create and activate a virtual environment** (recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

All environment settings are managed through `config.ini` — no hardcoding in test scripts.

```ini
[settings]
base_url = https://adnabu-store-assignment1.myshopify.com/password
browser  = chrome    # options: chrome | firefox

[credentials]
password = AdNabuQA
```

To switch browsers, change `browser = firefox` in `config.ini`. No test code changes required.

---

## Running Tests

**Run the full test suite**

```bash
pytest
```

**Run a specific test module**

```bash
pytest tests/test_product_search.py
pytest tests/test_add_to_cart.py
```

**Run a specific test case**

```bash
pytest tests/test_product_search.py::TestProductSearch::test_search_exact_product_name
```

**Run with verbose output**

```bash
pytest -v
```

> Reports are automatically generated at `reports/report.html` after every run (configured in `pytest.ini`).

---

## Test Reports

After each test run, an HTML report is generated at:

```
reports/report.html
```

Open it in any browser to see pass/fail results, test durations, and failure details. The report is self-contained (no external dependencies).

---

## Framework Design

### Page Object Model (POM)

Each page of the application has a dedicated class under `pages/`. Locators are defined as class-level constants. No locators or Selenium calls appear in test files — tests only call page object methods.

### SeleniumUtils

`utils/selenium_utils.py` wraps all WebDriverWait and low-level Selenium calls in named methods (`click`, `send_keys`, `scroll_into_view`, `js_click`, etc.), so page objects stay clean and readable. All waits use explicit waits — no `time.sleep()`.

### Data-Driven Testing

Test inputs are stored in `test_data/*.json` and loaded via `DataLoader.load_test_data()`. Test classes load data once at class level, keeping tests free of hardcoded values and easy to extend.

### Fixtures (conftest.py)

- `app_config` — session-scoped, reads `config.ini` once per run
- `driver` — function-scoped, spins up and tears down a browser per test
- `setup_login` — function-scoped, auto-use, logs in before every test automatically
