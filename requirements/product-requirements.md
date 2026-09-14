# Harbor & Pine Outfitters — Product Requirements

## Purpose

Harbor & Pine Outfitters is a local online store where signed-in customers can browse outdoor-lifestyle products, manage a cart, complete an order, and review their own past orders.

## Login and session

- Customers sign in using a valid username and password.
- Both fields are required. Invalid credentials must not create an authenticated session and must show a clear error message.
- A successful login redirects the customer to the product catalog.
- Signing out ends the authenticated session and redirects to the home page.
- Checkout and order history require authentication. Unauthenticated customers who attempt to open either page are directed to sign in.

## Catalog and search

- The catalog displays all available products with their name, category, price, stock status, and a link to details.
- Product details show the full product name, description, category, price, and remaining stock.
- Customers can search using text that appears in a product name or description. Search is case-insensitive and ignores leading/trailing whitespace.
- Customers can filter by category. Applying a search and a category filter returns products satisfying both selections.
- Clearing the search text and choosing All categories returns the full catalog.

## Cart

- A cart is maintained for the active browser session and is visible without sign-in.
- Customers may add 1 through 10 units of a product at a time, provided the resulting quantity does not exceed available stock.
- Adding a product already in the cart increases its existing quantity; it does not create a second line.
- Every cart line displays the product, unit price, quantity, line total, and a removal action.
- Cart quantities must be whole numbers from 1 through 10 and may not exceed the product's available stock. Invalid updates leave the existing cart quantity unchanged and explain the problem.
- Removing an item immediately removes it from the cart. Cart totals and the header cart count update to match the cart contents.
- The cart subtotal is the sum of every line total and is shown in US dollars with two decimal places.

## Checkout and shipping

- Checkout is unavailable for an empty cart.
- Checkout requires recipient name, email address, street address, city, postal code, and a shipping method.
- Email addresses must have a local part, an `@`, and a domain portion. Postal codes must contain at least five non-space characters.
- Standard shipping costs $6.00 for orders below $50.00 and is free for orders with a merchandise subtotal of $50.00 or more.
- Express shipping costs $15.00 for all order subtotals.
- The checkout summary displays merchandise subtotal, shipping cost, and final total. The final total equals subtotal plus shipping.

## Orders and history

- Placing an order creates exactly one order containing all current cart lines and the shipping details shown at checkout.
- An order records the product name, quantity, unit price, merchandise subtotal, shipping amount, total, shipping method, and time it was placed.
- Placing an order reduces stock by the ordered quantities and clears the cart only after the order is successfully stored.
- A completed checkout displays a confirmation with the order number and final total. Refreshing or navigating after completion must not create another order.
- Order history shows only the signed-in customer's orders, newest first. Each order includes its order number, date, shipping method, items, quantities, and totals.
