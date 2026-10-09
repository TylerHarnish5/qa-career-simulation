## Overview

Harbor & Pine Outfitters is a local Flask-based e-commerce application used as a hands-on software QA and test automation simulation.

The project covers the QA process from written acceptance criteria and manual black-box testing through defect reporting, regression testing, browser automation, HTTP integration testing, database validation, unit testing, API testing, cross-browser testing, and continuous integration.

The goal is to demonstrate practical QA and automation experience across multiple testing layers rather than focusing only on UI automation.

# Harbor & Pine Outfitters — QA & Test Automation Project

[![QA Test Suite](https://github.com/TylerHarnish5/qa-career-simulation/actions/workflows/tests.yml/badge.svg)](https://github.com/TylerHarnish5/qa-career-simulation/actions/workflows/tests.yml)

## QA Objectives

- Validate application behavior against written acceptance criteria
- Identify and reproduce functional defects
- Document defects with clear expected and actual behavior
- Retest fixes and perform regression testing
- Build maintainable automated regression tests
- Test behavior at the UI, HTTP, database, and unit levels
- Exercise positive, negative, and boundary test cases
- Organize reusable automation with pytest fixtures and Page Object Model concepts
- Run automated tests consistently in a clean CI environment

## Technologies

- Python
- Flask
- pytest
- Playwright
- Chromium
- Firefox
- WebKit
- Requests
- SQLite
- SQL
- Postman
- Git
- GitHub
- GitHub Actions

## Testing Performed

### Manual / Black-Box Testing

The application was initially tested manually against documented acceptance criteria.

Areas tested included:

- Authentication
- Product discovery
- Product search
- Category filtering
- Product details
- Cart management
- Quantity validation
- Checkout
- Shipping calculations
- Order history

Testing included valid inputs, invalid inputs, boundary conditions, session behavior, and user-visible application state.

Supporting QA documentation is available in the `documents/` directory.

## Defects Identified

Manual and automated testing uncovered multiple application defects.

Examples included:

- Product search matched product names but failed to return products when the search term appeared only in the product description
- Decimal cart quantities such as `5.00` were incorrectly converted into quantity `1`
- Standard shipping was incorrectly charged at exactly the `$50.00` free-shipping boundary
- Additional cart quantity and stock-validation issues were identified during initial acceptance testing

Defects were reproduced, documented, corrected, and retested.

Example QA documents included in the repository:

- `documents/Defect Report.docx`
- `documents/Initial Acceptance Criteria Test Report.docx`

## UI Automation

Playwright and pytest were used to automate browser-based regression tests.

Automated UI coverage includes:

- Product-description search regression testing
- The `$50.00` free-shipping boundary
- Reusable authenticated browser setup
- Playwright locators and assertions
- Browser interaction initially recorded with Playwright Codegen
- Reusable pytest fixtures
- Page Object Model organization

The UI tests verify real user-facing workflows through the browser rather than calling application functions directly.

## Page Object Model

Reusable page objects were introduced to separate UI interaction details from test logic.

Current page objects include:

```text
pages/
├── __init__.py
├── login_page.py
└── checkout_page.py
```

For example, login behavior is encapsulated in `LoginPage` rather than repeating username, password, and sign-in locators throughout the suite.

The checkout page object similarly encapsulates shipping-form interactions.

This makes the UI automation easier to maintain if page structure or locators change.

## Cross-Browser Testing

Critical Playwright UI tests were executed across all three Playwright browser engines:

- Chromium
- Firefox
- WebKit

The product-search and shipping-boundary workflows were executed across each browser engine, producing six successful cross-browser test executions.

Cross-browser testing is intentionally limited to important smoke/regression flows rather than duplicating the entire suite across every browser.

## HTTP / Integration Testing

Python's `requests` library was used to interact directly with the Flask application without going through a browser.

Integration tests include:

- Verifying protected routes redirect unauthenticated users
- Verifying invalid login attempts do not establish authenticated sessions
- Verifying valid login establishes authenticated session state
- Sending cart requests directly to Flask
- Testing valid and invalid quantity input
- Verifying server-side behavior independently of the browser

A `requests.Session()` is used where authentication state and cookies need to persist across multiple requests.

This layer was also used to determine whether defects originated in browser behavior or backend application logic.

## Database Testing and Validation

SQLite and SQL were used to inspect persisted application state and validate relationships between stored data.

Database validation work included:

- Checking that stored order totals equal subtotal plus shipping
- Checking shipping values against business rules
- Comparing stored order subtotals with the calculated sum of corresponding `order_items`
- Inspecting the relationship between the `orders` and `order_items` tables
- Using database state to investigate previously observed application defects

Database-audit logic is kept separate from the main regression suite so historical development data does not make the automated suite fail unpredictably.

The database audit utility is located under:

```text
tools/
└── database_audit.py
```

The local `store.db` file is not committed to Git. It can be recreated from the committed schema and reset script.

## Unit Testing

pytest unit tests directly exercise internal application logic.

Examples include:

- Shipping-cost calculation
- Cart-line subtotal calculation
- Empty-cart behavior
- Database connection cleanup

### Boundary Testing

The shipping calculation is tested around the exact free-shipping boundary:

```text
$49.99 standard shipping → $6.00
$50.00 standard shipping → $0.00
$50.01 standard shipping → $0.00
```

Express-shipping behavior is also tested independently.

### Parameterized Testing

`pytest.mark.parametrize` is used to execute the same shipping test logic against multiple input and expected-output combinations.

This keeps related boundary cases concise while still making each case independently testable.

### Mocking

`MagicMock` and `patch` are used to isolate application functions from dependencies.

For example, `cart_lines()` is tested using controlled fake product data instead of relying on the real SQLite database.

Mock interaction assertions are also used to verify that database connections are closed when expected.

## Code and Branch Coverage

`pytest-cov` was used during development to inspect which application statements and branches were exercised by automated tests.

Coverage analysis was used to:

- Identify unexecuted statements
- Identify partially covered decision branches
- Add a targeted test for previously uncovered behavior
- Understand the difference between statement coverage and branch coverage

Coverage was treated as a tool for identifying test gaps rather than as a target percentage.

Generated coverage files are excluded from Git through `.gitignore`.

## API Testing with Postman

A Postman collection was created to exercise HTTP behavior independently of the Python test code.

The collection covers:

- Unauthenticated access to protected routes
- Valid authentication
- Session and cookie persistence
- Authenticated access to order history
- Valid cart additions
- Invalid cart quantities
- HTTP response status validation
- Response-header validation
- Positive and negative API test cases

Postman post-response scripts include automated assertions rather than relying only on manually inspecting responses.

The exported collection is available at:

```text
postman/
└── Harbor & Pine QA API Tests.postman_collection.json
```

## Test Organization

qa-career-simulation/
├── .github/
│   └── workflows/
│       └── tests.yml
├── documents/
│   ├── Defect Report.docx
│   └── Initial Acceptance Criteria Test Report.docx
├── pages/
│   ├── __init__.py
│   ├── checkout_page.py
│   └── login_page.py
├── postman/
│   └── Harbor & Pine QA API Tests.postman_collection.json
├── requirements/
│   ├── acceptance-criteria.md
│   └── product-requirements.md
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── data_constants.py
│   ├── test_auth_integration.py
│   ├── test_cart_unit.py
│   ├── test_database_unit.py
│   ├── test_product_search.py
│   ├── test_shipping.py
│   └── test_shipping_unit.py
├── tools/
│   └── database_audit.py
├── app.py
├── requirements.txt
├── reset_db.py
├── schema.sql
└── README.md

## Reusable Test Configuration

Shared seeded test data is centralized in:

```text
tests/data_constants.py
```

This avoids scattering values such as login credentials, product identifiers, and expected seeded products throughout multiple test files.

Reusable pytest fixtures are located in:

```text
tests/conftest.py
```

These fixtures handle behavior such as:

- Automatically starting the Flask application when required
- Waiting until the server is ready
- Shutting down the server after the test session
- Providing a reusable authenticated Playwright page

This allows the primary regression suite to run without manually starting Flask first.

## Running the Project

### 1. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
python -m playwright install chromium firefox webkit
```

### 3. Initialize the Database

```bash
python reset_db.py
```

### 4. Run the Automated Test Suite

```bash
python -m pytest tests -v
```

The test infrastructure automatically starts the Flask server for tests that require the running application.

## Running Cross-Browser UI Tests

Run the critical Playwright UI regression tests against Chromium, Firefox, and WebKit:

```bash
python -m pytest tests/test_product_search.py tests/test_shipping.py -v --browser chromium --browser firefox --browser webkit
```

This produces six test executions:

```text
Product search × Chromium
Product search × Firefox
Product search × WebKit
Shipping boundary × Chromium
Shipping boundary × Firefox
Shipping boundary × WebKit
```

## Continuous Integration

GitHub Actions automatically executes the QA regression suite on:

- Pushes
- Pull requests

The CI workflow:

1. Checks out the repository
2. Sets up Python
3. Installs project dependencies
4. Installs Playwright browser dependencies
5. Initializes a clean application database
6. Runs the pytest test suite
7. Reports the resulting pass or failure status

The workflow is located at:

```text
.github/workflows/tests.yml
```

CI also exposed an accidental undeclared local dependency that had gone unnoticed because it was already installed on the development machine. Running the suite in GitHub's clean environment exposed the dependency, allowing it to be removed.

## Test Strategy

The project uses multiple testing layers rather than attempting to prove every behavior through browser automation.

### Unit Tests

Used for isolated application logic where direct inputs and outputs can be tested efficiently.

Examples:

- Shipping-cost calculation
- Cart calculations
- Connection-cleanup behavior

### Integration Tests

Used when multiple real application components need to interact.

Examples:

- Flask authentication
- Session state
- Server-side cart validation
- HTTP redirects

### End-to-End / UI Tests

Used for important user-visible workflows.

Examples:

- Product-description search
- Checkout free-shipping boundary

The project follows the principle of using the lowest-cost testing layer that can confidently validate a behavior while retaining end-to-end coverage for important user workflows.

## Example Defect Regression Cycles

### Product Description Search

Initial behavior:

```text
Search term: waxed
Expected: Harbor Canvas Tote appears
Actual: No Products Found
```

The defect was documented and corrected.

A Playwright regression test was then created to:

1. Authenticate through the application
2. Search for `waxed`
3. Apply the search
4. Verify that `Harbor Canvas Tote` is visible

The automated test now protects the corrected behavior from regression.

### $50 Free-Shipping Boundary

Initial behavior:

```text
Subtotal: $50.00
Shipping: $6.00
Total: $56.00
```

Expected behavior:

```text
Subtotal: $50.00
Shipping: $0.00
Total: $50.00
```

The issue was reproduced through Playwright, corrected, and retested.

The resulting automated regression test verifies that standard shipping is free at exactly `$50.00`.

## Key QA Skills Demonstrated

- Acceptance testing
- Manual black-box testing
- Functional testing
- Regression testing
- Defect reporting
- Defect retesting
- Boundary-value testing
- Positive and negative testing
- UI automation
- Playwright
- pytest
- Test fixtures
- Parameterized testing
- Page Object Model
- HTTP integration testing
- Session and cookie testing
- API testing with Postman
- SQL/database validation
- Unit testing
- Mocking and dependency patching
- Code and branch coverage
- Cross-browser testing
- Git and GitHub
- GitHub Actions CI
- Test-suite maintainability and organization

## Project Status

The project currently includes a passing automated regression suite, reusable UI automation structure, API tests, QA documentation, cross-browser validation, and GitHub Actions CI.

The repository is intended as a practical portfolio demonstration of entry-level software QA and test automation skills.
