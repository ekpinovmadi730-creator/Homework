from datetime import datetime
import numpy as np
import pandas as pd


class User:
    def __init__(self, _id: int, _name: str, _email: str):
        self._id = _id
        self._name = _name.strip().title()
        self._email = _email.strip().lower()
        if "@" not in self._email:
            raise ValueError("Email must contain @")

    @classmethod
    def from_string(cls, data: str):
        parts = data.split(",")
        _id = int(parts[0].strip())
        _name = parts[1].strip()
        _email = parts[2].strip()
        return cls(_id, _name, _email)

    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"

    def __del__(self):
        print(f"User {self._name} deleted")


class Product:
    def __init__(self, id: int, name: str, price: float, category: str):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category='{self.category}')"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category}


class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product: Product):
        if product.id not in self._products:
            self._products[product.id] = product

    def remove_product(self, product_id: int):
        self._products.pop(product_id, None)

    def get_product(self, product_id: int):
        return self._products.get(product_id)

    def get_all_products(self):
        return list(self._products.values())

    def unique_products(self):
        return set(self._products.values())

    def to_dict(self):
        return dict(self._products)

    def filter_by_price(self, min_price: float):
        return [p for p in self._products.values() if (lambda x: x >= min_price)(p.price)]


class Logger:
    def log_action(self, user: User, action: str, product: Product, filename: str):
        timestamp = datetime.now().isoformat()
        line = f"{timestamp};{user._id};{action};{product.id}\n"
        with open(filename, "a") as f:
            f.write(line)

    def read_logs(self, filename: str):
        logs = []
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                logs.append({
                    "timestamp": parts[0],
                    "user_id": parts[1],
                    "action": parts[2],
                    "product_id": parts[3]
                })
        return logs


class Order:
    def __init__(self, id: int, user: User, products: list = None):
        self.id = id
        self.user = user
        self.products = products if products is not None else []

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, product_id: int):
        self.products = [p for p in self.products if p.id != product_id]

    def total_price(self):
        return sum(p.price for p in self.products)

    def most_expensive_products(self, n: int):
        return sorted(self.products, key=lambda p: p.price, reverse=True)[:n]

    def __str__(self):
        return f"Order(id={self.id}, user={self.user._name}, total={self.total_price()})"


def price_stream(products: list):
    for product in products:
        yield product.price


class OrderIterator:
    def __init__(self, orders: list):
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


def get_price_array(products: list):
    return np.array([p.price for p in products])


def get_mean_median(prices: np.ndarray):
    return (round(float(np.mean(prices)), 2), float(np.median(prices)))


def normalize_prices(prices: np.ndarray):
    min_p = prices.min()
    max_p = prices.max()
    return (prices - min_p) / (max_p - min_p)


def get_category_array(products: list):
    return np.array([p.category for p in products])


def count_unique_categories(categories: np.ndarray):
    return len(np.unique(categories))


def products_above_mean(prices: np.ndarray, products: list):
    mean = np.mean(prices)
    return [p for p, price in zip(products, prices) if price > mean]


def apply_discount(prices: np.ndarray):
    return prices * 0.9


def orders_to_2d_array(orders: list):
    return np.array([[o.total_price()] for o in orders])


def mean_order_per_user(totals: np.ndarray):
    return float(np.mean(totals))


def indices_above_1000(totals: np.ndarray):
    return list(np.where(totals > 1000)[0])


def users_to_dataframe(users: list):
    return pd.DataFrame([{
        "id": u._id,
        "name": u._name,
        "email": u._email,
        "registration_date": datetime.now().strftime("%Y-%m-%d")
    } for u in users])


def products_to_dataframe(products: list):
    return pd.DataFrame([{
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "price": p.price
    } for p in products])


def merge_users_orders(users_df: pd.DataFrame, orders_df: pd.DataFrame):
    merged = pd.merge(orders_df, users_df, left_on="user_id", right_on="id")
    return merged[["order_id", "name", "total"]].rename(columns={"name": "user_name"})


def filter_orders_by_total(orders_df: pd.DataFrame, min_total: float):
    return orders_df[orders_df["total"] > min_total]


def group_orders_by_user_sum(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["total"].sum().reset_index().rename(columns={"total": "total_sum"})


def group_orders_by_user_mean(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["total"].mean().reset_index().rename(columns={"total": "mean_total"})


def count_orders_per_user(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["order_id"].count().reset_index().rename(columns={"order_id": "orders_count"})


def mean_price_by_category(products_df: pd.DataFrame):
    return products_df.groupby("category")["price"].mean().reset_index().rename(columns={"price": "mean_price"})


def add_discounted_price(products_df: pd.DataFrame):
    df = products_df.copy()
    df["discounted_price"] = df["price"] * 0.9
    return df


def sort_by_price_desc(products_df: pd.DataFrame):
    return products_df.sort_values("price", ascending=False).reset_index(drop=True)


def add_quantity_column(orders_df: pd.DataFrame):
    df = orders_df.copy()
    df["quantity"] = 1
    return df


def add_total_price_column(orders_df: pd.DataFrame):
    df = orders_df.copy()
    df["total_price"] = df["price"] * df["quantity"]
    return df


def filter_by_category(products_df: pd.DataFrame, category: str):
    return products_df[products_df["category"] == category]


def count_products_by_category(products_df: pd.DataFrame):
    return products_df.groupby("category")["product_name"].count().reset_index().rename(columns={"product_name": "count"})


def mean_price_by_category_v2(products_df: pd.DataFrame):
    return products_df.groupby("category")["price"].mean().reset_index().rename(columns={"price": "mean_price"})


def sort_orders_by_total_price(orders_df: pd.DataFrame):
    return orders_df.sort_values("total_price", ascending=False).reset_index(drop=True)


def top_n_expensive_orders(orders_df: pd.DataFrame, n: int):
    return orders_df.sort_values("total_price", ascending=False).head(n).reset_index(drop=True)


def merge_orders_users(users_df: pd.DataFrame, orders_df: pd.DataFrame):
    merged = pd.merge(orders_df, users_df, on="user_id")
    return merged[["order_id", "user_name", "total_price"]]


def mean_order_per_user_df(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["total_price"].mean().reset_index().rename(columns={"total_price": "mean_total"})


def count_orders_per_user_df(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["order_id"].count().reset_index().rename(columns={"order_id": "orders_count"})


def max_order_per_user(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["total_price"].max().reset_index().rename(columns={"total_price": "max_order"})


def unique_categories_per_user(orders_df: pd.DataFrame):
    return orders_df.groupby("user_name")["category"].nunique().reset_index().rename(columns={"category": "unique_categories"})


def add_vip_column(summary_df: pd.DataFrame):
    df = summary_df.copy()
    df["VIP"] = df["total_sum"] > 1000
    return df


def sort_users_by_sum_and_mean(summary_df: pd.DataFrame):
    return summary_df.sort_values(["total_sum", "mean_total"], ascending=[False, True]).reset_index(drop=True)


def final_report(orders_df: pd.DataFrame):
    agg = orders_df.groupby("user_name").agg(
        total_orders=("order_id", "count"),
        total_sum=("total_price", "sum"),
        mean_total=("total_price", "mean"),
        max_order=("total_price", "max"),
        unique_categories=("category", "nunique")
    ).reset_index()
    agg["VIP"] = agg["total_sum"] > 1000
    return agg
import numpy as np
import pandas as pd

print("=" * 60)
print("БЛОК 1")
print("=" * 60)

print("\n--- Задача 1 ---")
u1 = User(1, " john doe ", "John@Example.COM")
print(u1)

print("\n--- Задача 2 ---")
u2 = User.from_string("2, Alice Wonderland , alice@wonder.com")
print(u2)

print("\n--- Задача 3 ---")
p1 = Product(1, "Laptop", 1200.0, "Electronics")
p2 = Product(2, "Mouse", 25.0, "Electronics")
p3 = Product(3, "Monitor", 450.0, "Electronics")
p4 = Product(4, "T-Shirt", 20.0, "Clothing")
print(p1)
print(p1.to_dict())

print("\n--- Задача 4 ---")
inv = Inventory()
inv.add_product(p1)
inv.add_product(p2)
inv.add_product(p3)
inv.add_product(p4)
inv.add_product(p1)
print("All products:", [str(p) for p in inv.get_all_products()])
print("Unique products count:", len(inv.unique_products()))
inv.remove_product(4)
print("After remove T-Shirt:", [p.name for p in inv.get_all_products()])
print("Get product 1:", inv.get_product(1))
print("To dict keys:", list(inv.to_dict().keys()))

print("\n--- Задача 5 ---")
inv2 = Inventory()
inv2.add_product(Product(1, "Laptop", 1200.0, "Electronics"))
inv2.add_product(Product(2, "Mouse", 25.0, "Electronics"))
expensive = inv2.filter_by_price(100.0)
print([p.name for p in expensive])

print("\n--- Задача 6 ---")
logger = Logger()
logger.log_action(u1, "purchase", p1, "logs.txt")
logger.log_action(u2, "view", p2, "logs.txt")
logs = logger.read_logs("logs.txt")
for log in logs:
    print(log)

print("\n--- Задача 7 ---")
o1 = Order(1, u1, [p1, p2])
o2 = Order(2, u2, [p2, p3])
print(o1)
print("Total price:", o1.total_price())
o1.add_product(p3)
print("After add Monitor:", o1.total_price())
o1.remove_product(3)
print("After remove Monitor:", o1.total_price())

print("\n--- Задача 8 ---")
o1.add_product(p3)
print("Most expensive 2:", [str(p) for p in o1.most_expensive_products(2)])

print("\n--- Задача 9 ---")
products_list = [p1, p2, p3]
gen = price_stream(products_list)
print("Prices from generator:", list(price_stream(products_list)))

print("\n--- Задача 10 ---")
orders_list = [o1, o2]
iterator = OrderIterator(orders_list)
for order in iterator:
    print(order)

print("\n" + "=" * 60)
print("БЛОК 2 — NumPy")
print("=" * 60)

products_all = [p1, p2, p3, p4]

print("\n--- Задача 11 ---")
prices_arr = get_price_array(products_all)
print(prices_arr)

print("\n--- Задача 12 ---")
mean_med = get_mean_median(prices_arr)
print(f"mean={mean_med[0]}, median={mean_med[1]}")

print("\n--- Задача 13 ---")
norm = normalize_prices(prices_arr)
print(np.round(norm, 4))

print("\n--- Задача 14 ---")
cat_arr = get_category_array(products_all)
print(cat_arr)

print("\n--- Задача 15 ---")
print("Unique categories count:", count_unique_categories(cat_arr))

print("\n--- Задача 16 ---")
above_mean = products_above_mean(prices_arr, products_all)
print([p.name for p in above_mean])

print("\n--- Задача 17 ---")
discounted = apply_discount(prices_arr)
print(discounted)

print("\n--- Задача 18 ---")
arr_2d = orders_to_2d_array([o1, o2])
print(arr_2d)

print("\n--- Задача 19 ---")
totals_arr = np.array([o1.total_price(), o2.total_price()])
print("Mean order per user:", mean_order_per_user(totals_arr))

print("\n--- Задача 20 ---")
sample = np.array([1200.0, 900.0, 1500.0])
print("Indices above 1000:", indices_above_1000(sample))

print("\n" + "=" * 60)
print("БЛОК 3 — Pandas")
print("=" * 60)

users_list = [u1, u2]

print("\n--- Задача 21 ---")
users_df = users_to_dataframe(users_list)
print(users_df)

print("\n--- Задача 22 ---")
products_df = products_to_dataframe(products_all)
print(products_df)

print("\n--- Задача 23 ---")
u_df = pd.DataFrame({"id": [1, 2], "name": ["John", "Alice"]})
o_df = pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2], "total": [1200, 25]})
print(merge_users_orders(u_df, o_df))

print("\n--- Задача 24 ---")
merged_df = merge_users_orders(u_df, o_df)
print(filter_orders_by_total(merged_df, 100))

print("\n--- Задача 25 ---")
orders_full = pd.DataFrame({
    "order_id": [101, 103, 102],
    "user_name": ["John", "John", "Alice"],
    "total": [1200, 500, 25]
})
print(group_orders_by_user_sum(orders_full))

print("\n--- Задача 26 ---")
print(group_orders_by_user_mean(orders_full))

print("\n--- Задача 27 ---")
print(count_orders_per_user(orders_full))

print("\n--- Задача 28 ---")
print(mean_price_by_category(products_df))

print("\n--- Задача 29 ---")
print(add_discounted_price(products_df))

print("\n--- Задача 30 ---")
print(sort_by_price_desc(products_df))

print("\n--- Задача 31 ---")
orders_items = pd.DataFrame({
    "order_id": [101, 102],
    "product_name": ["Laptop", "Mouse"],
    "price": [1200, 25]
})
print(add_quantity_column(orders_items))

print("\n--- Задача 32 ---")
orders_qty = pd.DataFrame({
    "order_id": [101, 102],
    "product_name": ["Laptop", "Mouse"],
    "price": [1200, 25],
    "quantity": [1, 2]
})
print(add_total_price_column(orders_qty))

print("\n--- Задача 33 ---")
products_named = pd.DataFrame({
    "product_name": ["Laptop", "T-Shirt"],
    "category": ["Electronics", "Clothing"],
    "price": [1200, 20]
})
print(filter_by_category(products_named, "Electronics"))

print("\n--- Задача 34 ---")
products_cat = pd.DataFrame({
    "product_name": ["Laptop", "Mouse", "Shirt"],
    "category": ["Electronics", "Electronics", "Clothing"]
})
print(count_products_by_category(products_cat))

print("\n--- Задача 35 ---")
products_price_cat = pd.DataFrame({
    "product_name": ["Laptop", "Mouse", "Shirt"],
    "category": ["Electronics", "Electronics", "Clothing"],
    "price": [1200, 25, 20]
})
print(mean_price_by_category_v2(products_price_cat))

print("\n--- Задача 36 ---")
orders_tp = pd.DataFrame({"order_id": [101, 102], "total_price": [1200, 50]})
print(sort_orders_by_total_price(orders_tp))

print("\n--- Задача 37 ---")
orders_tp2 = pd.DataFrame({"order_id": [101, 102, 103, 104], "total_price": [1200, 50, 500, 1500]})
print(top_n_expensive_orders(orders_tp2, 3))

print("\n--- Задача 38 ---")
users_38 = pd.DataFrame({"user_id": [1, 2], "user_name": ["John", "Alice"]})
orders_38 = pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2], "total_price": [1200, 50]})
print(merge_orders_users(users_38, orders_38))

print("\n--- Задача 39 ---")
orders_39 = pd.DataFrame({
    "user_name": ["John", "John", "Alice"],
    "total_price": [1200, 500, 50]
})
print(mean_order_per_user_df(orders_39))

print("\n--- Задача 40 ---")
orders_40 = pd.DataFrame({
    "user_name": ["John", "John", "Alice"],
    "order_id": [101, 103, 102]
})
print(count_orders_per_user_df(orders_40))

print("\n--- Задача 41 ---")
orders_41 = pd.DataFrame({
    "user_name": ["John", "John", "Alice"],
    "total_price": [1200, 500, 50]
})
print(max_order_per_user(orders_41))

print("\n--- Задача 42 ---")
orders_42 = pd.DataFrame({
    "user_name": ["John", "John", "John", "Alice"],
    "category": ["Electronics", "Electronics", "Clothing", "Clothing"]
})
print(unique_categories_per_user(orders_42))

print("\n--- Задача 43 ---")
summary_43 = pd.DataFrame({
    "user_name": ["John", "Alice"],
    "total_sum": [1700, 25]
})
print(add_vip_column(summary_43))

print("\n--- Задача 44 ---")
summary_44 = pd.DataFrame({
    "user_name": ["John", "Alice", "Bob"],
    "total_sum": [1700, 25, 1700],
    "mean_total": [850, 25, 600]
})
print(sort_users_by_sum_and_mean(summary_44))

print("\n--- Задача 45 ---")
orders_45 = pd.DataFrame({
    "user_name": ["John", "John", "Alice"],
    "order_id": [101, 103, 102],
    "total_price": [1200, 500, 25],
    "category": ["Electronics", "Clothing", "Clothing"]
})
print(final_report(orders_45))