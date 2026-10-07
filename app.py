import sqlite3
from decimal import Decimal, InvalidOperation
from functools import wraps
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for


ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "store.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "harbor-pine-local-development-key"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def money(cents):
    return f"${cents / 100:,.2f}"


app.jinja_env.filters["money"] = money


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to continue.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def cart_count():
    return sum(session.get("cart", {}).values())


def cart_lines():
    cart = session.get("cart", {})
    if not cart:
        return [], 0
    ids = [int(product_id) for product_id in cart]
    placeholders = ",".join("?" for _ in ids)
    products = get_db().execute(
        f"SELECT * FROM products WHERE id IN ({placeholders})", ids
    ).fetchall()
    products_by_id = {str(product["id"]): product for product in products}
    lines = []
    subtotal = 0
    for product_id, quantity in cart.items():
        product = products_by_id.get(product_id)
        if product:
            line_total = product["price_cents"] * quantity
            subtotal += line_total
            lines.append({"product": product, "quantity": quantity, "line_total": line_total})
    return lines, subtotal


@app.context_processor
def inject_layout_data():
    return {"cart_count": cart_count(), "current_user": session.get("full_name")}


@app.route("/")
def home():
    featured = get_db().execute("SELECT * FROM products ORDER BY id LIMIT 4").fetchall()
    return render_template("home.html", featured=featured)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
        ).fetchone()
        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            flash(f"Welcome back, {user['full_name'].split()[0]}.", "success")
            return redirect(url_for("products"))
        flash("We couldn't sign you in with those details.", "error")
    return render_template("login.html")


@app.post("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("home"))


@app.route("/products")
def products():
    search_term = request.args.get("q", "").strip()
    selected_category = request.args.get("category", "")
    query = "SELECT * FROM products WHERE 1 = 1"
    parameters = []
    if search_term:
        query += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
        search_pattern = f"%{search_term.lower()}%"
        parameters.extend([search_pattern, search_pattern])
    if selected_category:
        query += " AND category = ?"
        parameters.append(selected_category)
    query += " ORDER BY name"
    product_rows = get_db().execute(query, parameters).fetchall()
    categories = get_db().execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    return render_template(
        "products.html",
        products=product_rows,
        categories=categories,
        search_term=search_term,
        selected_category=selected_category,
    )


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if product is None:
        flash("That product is no longer available.", "error")
        return redirect(url_for("products"))
    return render_template("product_detail.html", product=product)


@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if product is None:
        flash("That product is no longer available.", "error")
        return redirect(url_for("products"))
    try:
        entered_quantity = Decimal(request.form.get("quantity", "1"))
        if entered_quantity != entered_quantity.to_integral_value():
            raise ValueError
        quantity = int(entered_quantity)
    except (InvalidOperation, OverflowError, ValueError):
        quantity = 1
    if quantity < 1:
        flash("Choose at least one item.", "error")
        return redirect(request.referrer or url_for("product_detail", product_id=product_id))
    cart = session.get("cart", {})
    cart[str(product_id)] = quantity
    session["cart"] = cart
    flash(f"{product['name']} was added to your cart.", "success")
    return redirect(request.referrer or url_for("cart"))


@app.route("/cart")
def cart():
    lines, subtotal = cart_lines()
    return render_template("cart.html", lines=lines, subtotal=subtotal)


@app.post("/cart/update/<int:product_id>")
def update_cart(product_id):
    cart = session.get("cart", {})
    if str(product_id) not in cart:
        flash("That item is not in your cart.", "error")
        return redirect(url_for("cart"))
    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        quantity = 1
    if quantity == 0:
        cart.pop(str(product_id), None)
        flash("Item removed from your cart.", "info")
    else:
        cart[str(product_id)] = quantity
        flash("Cart updated.", "success")
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Item removed from your cart.", "info")
    return redirect(url_for("cart"))


def shipping_cost(subtotal, method):
    if method == "express":
        return 1500
    return 0 if subtotal >= 5000 else 600


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    lines, subtotal = cart_lines()
    if not lines:
        flash("Your cart is empty. Add an item before checking out.", "info")
        return redirect(url_for("products"))

    form_data = {field: request.form.get(field, "").strip() for field in ["customer_name", "email", "address", "city", "postal_code"]}
    selected_shipping = request.form.get("shipping_method", "standard")
    if request.method == "POST":
        missing = [name for name, value in form_data.items() if not value]
        if missing:
            flash("Please complete all shipping details.", "error")
        elif "@" not in form_data["email"]:
            flash("Enter a valid email address.", "error")
        elif selected_shipping not in {"standard", "express"}:
            flash("Choose a shipping method.", "error")
        else:
            shipping = shipping_cost(subtotal, selected_shipping)
            total = subtotal + shipping
            db = get_db()
            cursor = db.execute(
                """INSERT INTO orders
                   (user_id, customer_name, email, address, city, postal_code, shipping_method, shipping_cents, subtotal_cents, total_cents)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (session["user_id"], form_data["customer_name"], form_data["email"], form_data["address"], form_data["city"], form_data["postal_code"], selected_shipping, shipping, subtotal, total),
            )
            order_id = cursor.lastrowid
            for line in lines:
                db.execute(
                    """INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price_cents)
                       VALUES (?, ?, ?, ?, ?)""",
                    (order_id, line["product"]["id"], line["product"]["name"], line["quantity"], line["product"]["price_cents"]),
                )
                db.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (line["quantity"], line["product"]["id"]))
            db.commit()
            session["cart"] = {}
            return render_template("order_confirmation.html", order_id=order_id, total=total)
    shipping = shipping_cost(subtotal, selected_shipping)
    return render_template("checkout.html", lines=lines, subtotal=subtotal, shipping=shipping, total=subtotal + shipping, form_data=form_data, selected_shipping=selected_shipping)


@app.route("/orders")
@login_required
def order_history():
    orders = get_db().execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC, id DESC", (session["user_id"],)
    ).fetchall()
    order_items = {}
    for order in orders:
        order_items[order["id"]] = get_db().execute(
            "SELECT * FROM order_items WHERE order_id = ?", (order["id"],)
        ).fetchall()
    return render_template("orders.html", orders=orders, order_items=order_items)


if __name__ == "__main__":
    if not DATABASE.exists():
        from reset_db import reset_database
        reset_database()
    app.run(debug=True)
