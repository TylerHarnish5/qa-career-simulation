# Harbor & Pine Outfitters — Acceptance Criteria

## Authentication

1. Given valid account credentials, when a customer signs in, then the catalog opens and the customer is treated as signed in.
2. Given missing or invalid credentials, when sign-in is submitted, then the customer remains signed out and receives an understandable error.
3. Given a signed-in customer, when they sign out, then protected pages require sign-in again.

## Product discovery

1. The catalog initially shows every seeded product, with its correct name, price, category, and stock status.
2. A case-insensitive search finds products when the term appears in either the product name or description.
3. A category selection limits results to that category, and combined search/category selections require both conditions.
4. Every product detail page matches the selected product and shows the current stock level.

## Cart management

1. Adding a valid quantity from 1 to 10 adds the selected product and updates the cart count.
2. Adding the same product again combines quantities in one cart line, subject to available stock.
3. Non-numeric, fractional, zero, negative, over-10, or over-stock quantities are rejected without changing the cart.
4. Updating a cart line to a valid quantity recalculates its line total, cart subtotal, and cart count.
5. Removing a line removes it and recalculates all cart displays.
6. Cart contents remain available while navigating between catalog, details, cart, and checkout during the same browser session.

## Checkout

1. An empty cart cannot proceed to checkout.
2. Checkout cannot be completed until every required shipping field is present and valid.
3. The shipping choice is required and the displayed total always equals merchandise subtotal plus the applicable shipping charge.
4. A $49.99 standard-shipping subtotal adds $6.00; a $50.00 standard-shipping subtotal adds $0.00; express shipping adds $15.00 at either subtotal.
5. A successful order creates one order, stores every cart line and correct amounts, decrements inventory, clears the cart, and presents an order confirmation.
6. Repeating a browser refresh after the confirmation does not create another order.

## Order history

1. The history page is accessible only to a signed-in customer.
2. The page lists that customer's orders only, newest first.
3. Each entry shows the stored order number, placement date, items, quantities, unit prices, shipping method, merchandise subtotal, shipping cost, and total.
