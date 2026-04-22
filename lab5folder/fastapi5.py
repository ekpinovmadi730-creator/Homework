"""
FastAPI — E-commerce API
Барлық маршруттар тек сан: /1 ... /45
Запуск: uvicorn fastapi_app:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""

from typing import List
import pandas as pd
import numpy as np

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import User, Product, Order, Inventory, Logger, price_stream, OrderIterator
from numpy_tasks import NumPyAnalytics

from pandas_tasks import PandasAnalytics

_np = NumPyAnalytics()
_pd = PandasAnalytics()

app = FastAPI(title="E-commerce API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_users:    dict[int, User]    = {}
_products: dict[int, Product] = {}
_orders:   dict[int, Order]   = {}
_inventory = Inventory()
_logger    = Logger()
LOG_FILE   = "actions.log"


class UserIn(BaseModel):
    id: int
    name: str
    email: str

class UserFromString(BaseModel):
    csv_string: str

class ProductIn(BaseModel):
    id: int
    name: str
    price: float
    category: str

class OrderIn(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]


def _build_df() -> pd.DataFrame:
    rows = []
    for order in _orders.values():
        for product in order.products:
            rows.append({
                "user_name":   order.user._name,
                "order_id":    order.id,
                "total_price": order.total_price(),
                "category":    product.category,
            })
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def _get_products():
    prods = list(_products.values())
    if not prods:
        raise HTTPException(404, "Өнімдер жоқ")
    return prods


# ══════════════════════════════════════════════
# БЛОК 1 — Python / ООП
# ══════════════════════════════════════════════

@app.post("/1", tags=["Блок 1"], summary="Задача 1 — User жасау")
def task1(data: UserIn):
    try:
        user = User(data.id, data.name, data.email)
    except ValueError as e:
        raise HTTPException(422, str(e))
    _users[user._id] = user
    return user.to_dict()


@app.post("/2", tags=["Блок 1"], summary="Задача 2 — User.from_string")
def task2(data: UserFromString):
    try:
        user = User.from_string(data.csv_string)
    except (ValueError, IndexError) as e:
        raise HTTPException(422, str(e))
    _users[user._id] = user
    return user.to_dict()


@app.post("/3", tags=["Блок 1"], summary="Задача 3 — Product жасау")
def task3(data: ProductIn):
    product = Product(data.id, data.name, data.price, data.category)
    _products[product.id] = product
    _inventory.add_product(product)
    return product.to_dict()


@app.get("/4", tags=["Блок 1"], summary="Задача 4 — Inventory барлық өнімдер")
def task4():
    return [p.to_dict() for p in _inventory.get_all_products()]


@app.get("/5", tags=["Блок 1"], summary="Задача 5 — filter_by_price(min_price)")
def task5(min_price: float = Query(0.0, ge=0)):
    return [p.to_dict() for p in _inventory.filter_by_price(min_price)]


@app.post("/6", tags=["Блок 1"], summary="Задача 6 — log_action жазу")
def task6_write(user_id: int, action: str, product_id: int):
    user = _users.get(user_id)
    product = _products.get(product_id)
    if not user or not product:
        raise HTTPException(404, "User немесе Product табылмады")
    _logger.log_action(user, action, product, LOG_FILE)
    return {"detail": "logged"}

@app.get("/6", tags=["Блок 1"], summary="Задача 6 — read_logs оқу")
def task6_read():
    try:
        return _logger.read_logs(LOG_FILE)
    except FileNotFoundError:
        return []


@app.post("/7", tags=["Блок 1"], summary="Задача 7 — Order жасау")
def task7(data: OrderIn):
    user = _users.get(data.user_id)
    if not user:
        raise HTTPException(404, "User табылмады")
    prods = [_products[pid] for pid in data.product_ids if pid in _products]
    order = Order(data.id, user, prods)
    _orders[order.id] = order
    return order.to_dict()


@app.get("/8", tags=["Блок 1"], summary="Задача 8 — most_expensive_products(order_id, n)")
def task8(order_id: int, n: int = Query(3, ge=1)):
    order = _orders.get(order_id)
    if not order:
        raise HTTPException(404, "Order табылмады")
    return [p.to_dict() for p in order.most_expensive_products(n)]


@app.get("/9", tags=["Блок 1"], summary="Задача 9 — price_stream генератор")
def task9(order_id: int):
    order = _orders.get(order_id)
    if not order:
        raise HTTPException(404, "Order табылмады")
    return {"prices": list(price_stream(order.products))}


@app.get("/10", tags=["Блок 1"], summary="Задача 10 — OrderIterator")
def task10():
    return [o.to_dict() for o in OrderIterator(list(_orders.values()))]


# ══════════════════════════════════════════════
# БЛОК 2 — NumPy
# ══════════════════════════════════════════════

@app.get("/11", tags=["Блок 2 — NumPy"], summary="Задача 11 — бағалар массиві")
def task11():
    return {"prices": _np.create_price_array(_get_products()).tolist()}


@app.get("/12", tags=["Блок 2 — NumPy"], summary="Задача 12 — mean / median")
def task12():
    mean, median = _np.mean_median_price(_np.create_price_array(_get_products()))
    return {"mean": mean, "median": median}


@app.get("/13", tags=["Блок 2 — NumPy"], summary="Задача 13 — нормализация [0,1]")
def task13():
    arr = _np.normalize_prices(_np.create_price_array(_get_products()))
    return {"normalized": [round(v, 4) for v in arr.tolist()]}


@app.get("/14", tags=["Блок 2 — NumPy"], summary="Задача 14 — категориялар массиві")
def task14():
    return {"categories": _np.create_category_array(_get_products()).tolist()}


@app.get("/15", tags=["Блок 2 — NumPy"], summary="Задача 15 — бірегей категориялар саны")
def task15():
    return {"unique_count": _np.count_unique_categories(_np.create_category_array(_get_products()))}


@app.get("/16", tags=["Блок 2 — NumPy"], summary="Задача 16 — орташадан қымбат өнімдер")
def task16():
    prods = _get_products()
    return [p.to_dict() for p in _np.products_above_average(_np.create_price_array(prods), prods)]


@app.get("/17", tags=["Блок 2 — NumPy"], summary="Задача 17 — векторлық жеңілдік")
def task17(discount: float = Query(0.1, ge=0, le=1)):
    return {"discounted_prices": _np.apply_discount(_np.create_price_array(_get_products()), discount).tolist()}


@app.get("/18", tags=["Блок 2 — NumPy"], summary="Задача 18 — 2D тапсырыстар массиві")
def task18():
    if not _orders:
        raise HTTPException(404, "Тапсырыстар жоқ")
    return {"orders_totals": _np.create_orders_array(list(_orders.values())).tolist()}


@app.get("/19", tags=["Блок 2 — NumPy"], summary="Задача 19 — орташа тапсырыс сомасы")
def task19():
    if not _orders:
        raise HTTPException(404, "Тапсырыстар жоқ")
    return {"mean_order": _np.mean_order_per_user(_np.create_orders_array(list(_orders.values())))}


@app.get("/20", tags=["Блок 2 — NumPy"], summary="Задача 20 — шектен жоғары индекстер")
def task20(threshold: float = Query(1000.0)):
    if not _orders:
        raise HTTPException(404, "Тапсырыстар жоқ")
    totals = np.array([o.total_price() for o in _orders.values()])
    return {"indices": _np.orders_above_threshold(totals, threshold)}


# ══════════════════════════════════════════════
# БЛОК 3 — Pandas
# ══════════════════════════════════════════════

@app.get("/21", tags=["Блок 3 — Pandas"], summary="Задача 21 — users DataFrame")
def task21():
    return _pd.create_users_df(list(_users.values())).to_dict(orient="records")


@app.get("/22", tags=["Блок 3 — Pandas"], summary="Задача 22 — products DataFrame")
def task22():
    return _pd.create_products_df(list(_products.values())).to_dict(orient="records")


@app.get("/23", tags=["Блок 3 — Pandas"], summary="Задача 23 — users + orders merge")
def task23():
    if not _orders:
        return []
    users_df = _pd.create_users_df(list(_users.values()))
    orders_raw = pd.DataFrame([
        {"order_id": o.id, "user_id": o.user._id, "total": o.total_price()}
        for o in _orders.values()
    ])
    return _pd.merge_users_orders(users_df, orders_raw).to_dict(orient="records")


@app.get("/24", tags=["Блок 3 — Pandas"], summary="Задача 24 — тапсырыстарды сомасы бойынша сүзу")
def task24(min_total: float = Query(100.0)):
    df = _build_df()
    if df.empty:
        return []
    return _pd.filter_orders_by_total(df.rename(columns={"total_price": "total"}), min_total).to_dict(orient="records")


@app.get("/25", tags=["Блок 3 — Pandas"], summary="Задача 25 — groupby sum")
def task25():
    df = _build_df()
    if df.empty:
        return []
    return _pd.group_orders_sum(df.rename(columns={"total_price": "total"})).to_dict(orient="records")


@app.get("/26", tags=["Блок 3 — Pandas"], summary="Задача 26 — groupby mean")
def task26():
    df = _build_df()
    if df.empty:
        return []
    return _pd.mean_order_per_user(df).to_dict(orient="records")


@app.get("/27", tags=["Блок 3 — Pandas"], summary="Задача 27 — groupby count")
def task27():
    df = _build_df()
    if df.empty:
        return []
    return _pd.orders_count_per_user(df).to_dict(orient="records")


@app.get("/28", tags=["Блок 3 — Pandas"], summary="Задача 28 — категория бойынша орташа баға")
def task28():
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return []
    return _pd.mean_price_by_category(df).to_dict(orient="records")


@app.get("/29", tags=["Блок 3 — Pandas"], summary="Задача 29 — discounted_price баған")
def task29(discount: float = Query(0.1)):
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return []
    return _pd.add_discounted_price(df, discount).to_dict(orient="records")


@app.get("/30", tags=["Блок 3 — Pandas"], summary="Задача 30 — бағасы бойынша сорттау")
def task30():
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return []
    return _pd.sort_products_by_price(df).to_dict(orient="records")


@app.get("/31", tags=["Блок 3 — Pandas"], summary="Задача 31 — quantity баған қосу")
def task31():
    df = _build_df()
    if df.empty:
        return []
    return _pd.add_quantity_column(df).to_dict(orient="records")


@app.get("/32", tags=["Блок 3 — Pandas"], summary="Задача 32 — total_price = price * quantity")
def task32():
    df = _build_df()
    if df.empty:
        return []
    df2 = _pd.add_quantity_column(df.rename(columns={"total_price": "price"}))
    return _pd.add_total_price(df2).to_dict(orient="records")


@app.get("/33", tags=["Блок 3 — Pandas"], summary="Задача 33 — категория бойынша сүзу")
def task33(category: str = "Electronics"):
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return []
    return _pd.filter_by_category(df, category).to_dict(orient="records")


@app.get("/34", tags=["Блок 3 — Pandas"], summary="Задача 34 — категориядағы өнімдер саны")
def task34():
    df = _pd.create_products_df(list(_products.values()))
    if df.empty:
        return []
    return _pd.count_products_by_category(df).to_dict(orient="records")


@app.get("/35", tags=["Блок 3 — Pandas"], summary="Задача 35 — категория бойынша орташа баға")
def task35():
    return task28()


@app.get("/36", tags=["Блок 3 — Pandas"], summary="Задача 36 — total_price бойынша сорттау")
def task36():
    df = _build_df()
    if df.empty:
        return []
    return _pd.sort_orders_by_total_price(df).to_dict(orient="records")


@app.get("/37", tags=["Блок 3 — Pandas"], summary="Задача 37 — топ-N қымбат тапсырыстар")
def task37(n: int = Query(3, ge=1)):
    df = _build_df()
    if df.empty:
        return []
    return _pd.top_n_expensive_orders(df, n).to_dict(orient="records")


@app.get("/38", tags=["Блок 3 — Pandas"], summary="Задача 38 — orders + users merge")
def task38():
    return task23()


@app.get("/39", tags=["Блок 3 — Pandas"], summary="Задача 39 — орташа тапсырыс сомасы")
def task39():
    return task26()


@app.get("/40", tags=["Блок 3 — Pandas"], summary="Задача 40 — тапсырыстар саны")
def task40():
    return task27()


@app.get("/41", tags=["Блок 3 — Pandas"], summary="Задача 41 — max тапсырыс бағасы")
def task41():
    df = _build_df()
    if df.empty:
        return []
    return _pd.max_order_per_user(df).to_dict(orient="records")


@app.get("/42", tags=["Блок 3 — Pandas"], summary="Задача 42 — бірегей категориялар саны")
def task42():
    df = _build_df()
    if df.empty:
        return []
    return _pd.unique_categories_per_user(df).to_dict(orient="records")


@app.get("/43", tags=["Блок 3 — Pandas"], summary="Задача 43 — VIP баған қосу")
def task43():
    df = _build_df()
    if df.empty:
        return []
    return _pd.add_vip_column(_pd.final_report(df)).to_dict(orient="records")


@app.get("/44", tags=["Блок 3 — Pandas"], summary="Задача 44 — VIP + multi-key сорттау")
def task44():
    df = _build_df()
    if df.empty:
        return []
    return _pd.sort_users_multikey(_pd.add_vip_column(_pd.final_report(df))).to_dict(orient="records")


@app.get("/45", tags=["Блок 3 — Pandas"], summary="Задача 45 — финалды агрегация есебі")
def task45():
    df = _build_df()
    if df.empty:
        return []
    return _pd.final_report(df).to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True)