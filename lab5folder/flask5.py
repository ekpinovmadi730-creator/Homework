from flask import Flask, request, jsonify, abort
from datetime import datetime
import pandas as pd
import numpy as np


class User:
    def __init__(self, _id, _name, _email):
        self._id = _id
        self._name = _name.strip().title()
        self._email = _email.strip().lower()
        if "@" not in self._email:
            raise ValueError("Email must contain @")

    @classmethod
    def from_string(cls, data):
        parts = data.split(",")
        return cls(int(parts[0].strip()), parts[1].strip(), parts[2].strip())

    def __str__(self):
        return f"User(id={self._id}, name={self._name}, email={self._email})"

    def __del__(self):
        print(f"User {self._name} deleted")

    def to_dict(self):
        return {"id": self._id, "name": self._name, "email": self._email,
                "registration_date": datetime.now().strftime("%Y-%m-%d")}


class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = float(price)
        self.category = category

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, category={self.category})"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category}


class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product.id not in self._products:
            self._products[product.id] = product

    def remove_product(self, product_id):
        self._products.pop(product_id, None)

    def get_product(self, product_id):
        return self._products.get(product_id)

    def get_all_products(self):
        return list(self._products.values())

    def unique_products(self):
        return set(self._products.values())

    def to_dict(self):
        return dict(self._products)

    def filter_by_price(self, min_price):
        return [p for p in self._products.values() if (lambda x: x >= min_price)(p.price)]


class Logger:
    def log_action(self, user, action, product, filename):
        line = f"{datetime.now().isoformat()};{user._id};{action};{product.id}\n"
        with open(filename, "a") as f:
            f.write(line)

    def read_logs(self, filename):
        logs = []
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                logs.append({"timestamp": parts[0], "user_id": parts[1],
                             "action": parts[2], "product_id": parts[3]})
        return logs


class Order:
    def __init__(self, id, user, products=None):
        self.id = id
        self.user = user
        self.products = products if products is not None else []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]

    def total_price(self):
        return sum(p.price for p in self.products)

    def most_expensive_products(self, n):
        return sorted(self.products, key=lambda p: p.price, reverse=True)[:n]

    def __str__(self):
        return f"Order(id={self.id}, user={self.user._name}, total={self.total_price()})"

    def to_dict(self):
        return {"id": self.id, "user_id": self.user._id, "user_name": self.user._name,
                "products": [p.to_dict() for p in self.products], "total": self.total_price()}


def price_stream(products):
    for product in products:
        yield product.price


class OrderIterator:
    def __init__(self, orders):
        self._orders = orders
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._orders):
            raise StopIteration
        order = self._orders[self._index]
        self._index += 1
        return order


class NumPyAnalytics:

    @staticmethod
    def create_price_array(products):
        return np.array([p.price for p in products])

    @staticmethod
    def mean_median_price(prices):
        return (round(float(np.mean(prices)), 2), float(np.median(prices)))

    @staticmethod
    def normalize_prices(prices):
        mn, mx = prices.min(), prices.max()
        if mx == mn:
            return np.zeros_like(prices, dtype=float)
        return (prices - mn) / (mx - mn)

    @staticmethod
    def create_category_array(products):
        return np.array([p.category for p in products])

    @staticmethod
    def count_unique_categories(categories):
        return int(len(np.unique(categories)))

    @staticmethod
    def products_above_average(prices, products):
        mean = np.mean(prices)
        return [p for p, price in zip(products, prices) if price > mean]

    @staticmethod
    def apply_discount(prices):
        return prices * 0.9

    @staticmethod
    def create_orders_array(orders):
        return np.array([[o.total_price()] for o in orders])

    @staticmethod
    def mean_order_per_user(totals):
        return float(np.mean(totals))

    @staticmethod
    def orders_above_threshold(totals, threshold=1000.0):
        return list(np.where(totals > threshold)[0])


class PandasAnalytics:

    @staticmethod
    def create_users_df(users):
        return pd.DataFrame([{"id": u._id, "name": u._name, "email": u._email,
                               "registration_date": datetime.now().strftime("%Y-%m-%d")} for u in users])

    @staticmethod
    def create_products_df(products):
        return pd.DataFrame([{"id": p.id, "name": p.name, "category": p.category, "price": p.price} for p in products])

    @staticmethod
    def merge_users_orders(users_df, orders_df):
        merged = pd.merge(orders_df, users_df, left_on="user_id", right_on="id")
        return merged[["order_id", "name", "total"]].rename(columns={"name": "user_name"})

    @staticmethod
    def filter_orders_by_total(orders_df, min_total):
        return orders_df[orders_df["total"] > min_total]

    @staticmethod
    def group_orders_sum(orders_df):
        return orders_df.groupby("user_name")["total"].sum().reset_index().rename(columns={"total": "total_sum"})

    @staticmethod
    def group_orders_mean(orders_df):
        return orders_df.groupby("user_name")["total"].mean().reset_index().rename(columns={"total": "mean_total"})

    @staticmethod
    def count_orders_per_user(orders_df):
        return orders_df.groupby("user_name")["order_id"].count().reset_index().rename(columns={"order_id": "orders_count"})

    @staticmethod
    def mean_price_by_category(products_df):
        return products_df.groupby("category")["price"].mean().reset_index().rename(columns={"price": "mean_price"})

    @staticmethod
    def add_discounted_price(products_df):
        df = products_df.copy()
        df["discounted_price"] = df["price"] * 0.9
        return df

    @staticmethod
    def sort_by_price_desc(products_df):
        return products_df.sort_values("price", ascending=False).reset_index(drop=True)

    @staticmethod
    def add_quantity_column(orders_df):
        df = orders_df.copy()
        df["quantity"] = 1
        return df

    @staticmethod
    def add_total_price_column(orders_df):
        df = orders_df.copy()
        df["total_price"] = df["price"] * df["quantity"]
        return df

    @staticmethod
    def filter_by_category(products_df, category):
        return products_df[products_df["category"] == category]

    @staticmethod
    def sort_orders_by_total_price(orders_df):
        return orders_df.sort_values("total_price", ascending=False).reset_index(drop=True)

    @staticmethod
    def top_n_expensive_orders(orders_df, n):
        return orders_df.sort_values("total_price", ascending=False).head(n).reset_index(drop=True)

    @staticmethod
    def mean_order_per_user(orders_df):
        return orders_df.groupby("user_name")["total_price"].mean().reset_index().rename(columns={"total_price": "mean_total"})

    @staticmethod
    def orders_count_per_user(orders_df):
        return orders_df.groupby("user_name")["order_id"].count().reset_index().rename(columns={"order_id": "orders_count"})

    @staticmethod
    def max_order_per_user(orders_df):
        return orders_df.groupby("user_name")["total_price"].max().reset_index().rename(columns={"total_price": "max_order"})

    @staticmethod
    def unique_categories_per_user(orders_df):
        return orders_df.groupby("user_name")["category"].nunique().reset_index().rename(columns={"category": "unique_categories"})

    @staticmethod
    def add_vip_column(summary_df):
        df = summary_df.copy()
        df["VIP"] = df["total_sum"] > 1000
        return df

    @staticmethod
    def sort_users_multikey(summary_df):
        return summary_df.sort_values(["total_sum", "mean_total"], ascending=[False, True]).reset_index(drop=True)

    @staticmethod
    def final_report(orders_df):
        agg = orders_df.groupby("user_name").agg(
            total_orders=("order_id", "count"),
            total_sum=("total_price", "sum"),
            mean_total=("total_price", "mean"),
            max_order=("total_price", "max"),
            unique_categories=("category", "nunique")
        ).reset_index()
        agg["VIP"] = agg["total_sum"] > 1000
        return agg


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

_users = {}
_products = {}
_orders = {}
_inventory = Inventory()
_logger = Logger()
_np = NumPyAnalytics()
_pd = PandasAnalytics()
LOG_FILE = "logs.txt"

_users[1] = User(1, "John Doe", "john@example.com")
_users[2] = User(2, "Alice Smith", "alice@example.com")

p1 = Product(1, "Laptop", 1200.0, "Electronics")
p2 = Product(2, "Mouse", 25.0, "Electronics")
p3 = Product(3, "Monitor", 450.0, "Electronics")
p4 = Product(4, "T-Shirt", 20.0, "Clothing")

for p in [p1, p2, p3, p4]:
    _products[p.id] = p
    _inventory.add_product(p)

_orders[1] = Order(1, _users[1], [p1, p2])
_orders[2] = Order(2, _users[2], [p2, p3])
_orders[3] = Order(3, _users[1], [p3, p4])


def _json():
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="JSON body required")
    return data


def _build_df():
    rows = []
    for order in _orders.values():
        for product in order.products:
            rows.append({"user_name": order.user._name, "order_id": order.id,
                         "total_price": order.total_price(), "category": product.category})
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def _get_products():
    prods = list(_products.values())
    if not prods:
        abort(404, description="Өнімдер жоқ")
    return prods


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e.description)), 404

@app.errorhandler(422)
def unprocessable(e):
    return jsonify(error=str(e.description)), 422


@app.route("/1", methods=["POST"])
def task1():
    data = _json()
    try:
        user = User(data["id"], data["name"], data["email"])
    except (ValueError, KeyError) as e:
        abort(422, description=str(e))
    _users[user._id] = user
    return jsonify(user.to_dict()), 201


@app.route("/2", methods=["POST"])
def task2():
    data = _json()
    try:
        user = User.from_string(data["csv_string"])
    except (ValueError, IndexError, KeyError) as e:
        abort(422, description=str(e))
    _users[user._id] = user
    return jsonify(user.to_dict()), 201


@app.route("/3", methods=["POST"])
def task3():
    data = _json()
    try:
        product = Product(data["id"], data["name"], float(data["price"]), data["category"])
    except (KeyError, ValueError) as e:
        abort(422, description=str(e))
    _products[product.id] = product
    _inventory.add_product(product)
    return jsonify(product.to_dict()), 201


@app.route("/4", methods=["GET"])
def task4():
    return jsonify([p.to_dict() for p in _inventory.get_all_products()])


@app.route("/5", methods=["GET"])
def task5():
    min_price = float(request.args.get("min_price", 0))
    return jsonify([p.to_dict() for p in _inventory.filter_by_price(min_price)])


@app.route("/6", methods=["POST"])
def task6_write():
    data = _json()
    user = _users.get(data.get("user_id"))
    product = _products.get(data.get("product_id"))
    if not user or not product:
        abort(404, description="User немесе Product табылмады")
    _logger.log_action(user, data.get("action", "view"), product, LOG_FILE)
    return jsonify(detail="logged"), 201

@app.route("/6", methods=["GET"])
def task6_read():
    try:
        return jsonify(_logger.read_logs(LOG_FILE))
    except FileNotFoundError:
        return jsonify([])


@app.route("/7", methods=["POST"])
def task7():
    data = _json()
    user = _users.get(data.get("user_id"))
    if not user:
        abort(404, description="User табылмады")
    prods = [_products[pid] for pid in data.get("product_ids", []) if pid in _products]
    order = Order(data["id"], user, prods)
    _orders[order.id] = order
    return jsonify(order.to_dict()), 201


@app.route("/8", methods=["GET"])
def task8():
    order_id = int(request.args.get("order_id", 0))
    n = int(request.args.get("n", 3))
    order = _orders.get(order_id)
    if not order:
        abort(404, description="Order табылмады")
    return jsonify([p.to_dict() for p in order.most_expensive_products(n)])


@app.route("/9", methods=["GET"])
def task9():
    order_id = int(request.args.get("order_id", 0))
    order = _orders.get(order_id)
    if not order:
        abort(404, description="Order табылмады")
    return jsonify({"prices": list(price_stream(order.products))})


@app.route("/10", methods=["GET"])
def task10():
    return jsonify([o.to_dict() for o in OrderIterator(list(_orders.values()))])


@app.route("/11", methods=["GET"])
def task11():
    return jsonify({"prices": _np.create_price_array(_get_products()).tolist()})


@app.route("/12", methods=["GET"])
def task12():
    mean, median = _np.mean_median_price(_np.create_price_array(_get_products()))
    return jsonify({"mean": mean, "median": median})


@app.route("/13", methods=["GET"])
def task13():
    arr = _np.normalize_prices(_np.create_price_array(_get_products()))
    return jsonify({"normalized": [round(v, 4) for v in arr.tolist()]})


@app.route("/14", methods=["GET"])
def task14():
    return jsonify({"categories": _np.create_category_array(_get_products()).tolist()})


@app.route("/15", methods=["GET"])
def task15():
    return jsonify({"unique_count": _np.count_unique_categories(_np.create_category_array(_get_products()))})


@app.route("/16", methods=["GET"])
def task16():
    prods = _get_products()
    return jsonify([p.to_dict() for p in _np.products_above_average(_np.create_price_array(prods), prods)])


@app.route("/17", methods=["GET"])
def task17():
    return jsonify({"discounted_prices": _np.apply_discount(_np.create_price_array(_get_products())).tolist()})


@app.route("/18", methods=["GET"])
def task18():
    if not _orders:
        abort(404, description="Тапсырыстар жоқ")
    return jsonify({"orders_totals": _np.create_orders_array(list(_orders.values())).tolist()})


@app.route("/19", methods=["GET"])
def task19():
    if not _orders:
        abort(404, description="Тапсырыстар жоқ")
    return jsonify({"mean_order": _np.mean_order_per_user(_np.create_orders_array(list(_orders.values())))})


@app.route("/20", methods=["GET"])
def task20():
    if not _orders:
        abort(404, description="Тапсырыстар жоқ")
    threshold = float(request.args.get("threshold", 1000))
    totals = np.array([o.total_price() for o in _orders.values()])
    return jsonify({"indices": _np.orders_above_threshold(totals, threshold)})


@app.route("/21", methods=["GET"])
def task21():
    return jsonify(_pd.create_users_df(list(_users.values())).to_dict(orient="records"))


@app.route("/22", methods=["GET"])
def task22():
    return jsonify(_pd.create_products_df(list(_products.values())).to_dict(orient="records"))


@app.route("/23", methods=["GET"])
def task23():
    if not _orders:
        return jsonify([])
    users_df = _pd.create_users_df(list(_users.values()))
    orders_raw = pd.DataFrame([{"order_id": o.id, "user_id": o.user._id, "total": o.total_price()} for o in _orders.values()])
    return jsonify(_pd.merge_users_orders(users_df, orders_raw).to_dict(orient="records"))


@app.route("/24", methods=["GET"])
def task24():
    min_total = float(request.args.get("min_total", 100))
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.filter_orders_by_total(df.rename(columns={"total_price": "total"}), min_total).to_dict(orient="records"))


@app.route("/25", methods=["GET"])
def task25():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.group_orders_sum(df.rename(columns={"total_price": "total"})).to_dict(orient="records"))


@app.route("/26", methods=["GET"])
def task26():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.group_orders_mean(df.rename(columns={"total_price": "total"})).to_dict(orient="records"))


@app.route("/27", methods=["GET"])
def task27():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.count_orders_per_user(df.rename(columns={"total_price": "total"})).to_dict(orient="records"))


@app.route("/28", methods=["GET"])
def task28():
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return jsonify([])
    return jsonify(_pd.mean_price_by_category(df).to_dict(orient="records"))


@app.route("/29", methods=["GET"])
def task29():
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return jsonify([])
    return jsonify(_pd.add_discounted_price(df).to_dict(orient="records"))


@app.route("/30", methods=["GET"])
def task30():
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return jsonify([])
    return jsonify(_pd.sort_by_price_desc(df).to_dict(orient="records"))


@app.route("/31", methods=["GET"])
def task31():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.add_quantity_column(df).to_dict(orient="records"))


@app.route("/32", methods=["GET"])
def task32():
    df = _build_df()
    if df.empty:
        return jsonify([])
    df2 = _pd.add_quantity_column(df.rename(columns={"total_price": "price"}))
    return jsonify(_pd.add_total_price_column(df2).to_dict(orient="records"))


@app.route("/33", methods=["GET"])
def task33():
    category = request.args.get("category", "Electronics")
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return jsonify([])
    return jsonify(_pd.filter_by_category(df, category).to_dict(orient="records"))


@app.route("/34", methods=["GET"])
def task34():
    return task28()


@app.route("/35", methods=["GET"])
def task35():
    return task28()


@app.route("/36", methods=["GET"])
def task36():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.sort_orders_by_total_price(df).to_dict(orient="records"))


@app.route("/37", methods=["GET"])
def task37():
    n = int(request.args.get("n", 3))
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.top_n_expensive_orders(df, n).to_dict(orient="records"))


@app.route("/38", methods=["GET"])
def task38():
    return task23()


@app.route("/39", methods=["GET"])
def task39():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.mean_order_per_user(df).to_dict(orient="records"))


@app.route("/40", methods=["GET"])
def task40():
    return task27()


@app.route("/41", methods=["GET"])
def task41():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.max_order_per_user(df).to_dict(orient="records"))


@app.route("/42", methods=["GET"])
def task42():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.unique_categories_per_user(df).to_dict(orient="records"))


@app.route("/43", methods=["GET"])
def task43():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.add_vip_column(_pd.final_report(df)).to_dict(orient="records"))


@app.route("/44", methods=["GET"])
def task44():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.sort_users_multikey(_pd.add_vip_column(_pd.final_report(df))).to_dict(orient="records"))


@app.route("/45", methods=["GET"])
def task45():
    df = _build_df()
    if df.empty:
        return jsonify([])
    return jsonify(_pd.final_report(df).to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)