#1
users=set()
total_buys=0
total_sum=0
user_spent={}
with open("shop_logs.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts=line.strip().split(";")
        date=parts[0]
        user=parts[1]
        act=parts[2]
        users.add(user)
        if act=="BUY":
            amount=int(parts[3])
            total_buys+=1
            total_sum+=amount
            if user in user_spent:
                user_spent[user]+=amount
            else:
                user_spent[user]=amount
max_money=0
max_user=""
for u in user_spent:
    if user_spent[u]>max_money:
        max_money=user_spent[u]
        max_user=u
if total_buys>0:
    avg_check=total_sum/total_buys
else:
    avg_check=0
with open("report.txt", "w", encoding="utf-8") as f:
    f.write(f"Уникальных пользователей: {len(users)}\n")
    f.write(f"Всего покупок: {total_buys}\n")
    f.write(f"Общая сумма продаж: {total_sum}\n")
    f.write(f"Пользователь, потративший больше всего: {max_user} ({max_money})\n")
    f.write(f"Средний чек: {avg_check:.2f}\n")
#2
import csv
employees=[]
dept_salaries={}
with open("employees.csv", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for row in reader:
        salary=int(row["salary"])
        row["salary"]=salary
        employees.append(row)
        dept=row["department"]
        if dept not in dept_salaries:
            dept_salaries[dept]=[]
        dept_salaries[dept].append(salary)
total_salary=0
for e in employees:
    total_salary +=e["salary"]
avg_salary=total_salary/len(employees)
dept_avg={}
for d in dept_salaries:
    s=0
    for salary in dept_salaries[d]:
        s +=salary
    dept_avg[d]=s/len(dept_salaries[d])
best_dept=""
max_avg=0
for d in dept_avg:
    if dept_avg[d]>max_avg:
        max_avg=dept_avg[d]
        best_dept=d
top_employee=employees[0]
for e in employees:
    if e["salary"]>top_employee["salary"]:
        top_employee=e
high_paid=[]
for e in employees:
    if e["salary"]>avg_salary:
        high_paid.append(e)
with open("high_salary.csv", "w", newline="", encoding="utf-8") as f:
    writer=csv.DictWriter(f, fieldnames=["name", "department", "salary"])
    writer.writeheader()
    writer.writerows(high_paid)
#3
import json
with open("orders.json", "r", encoding="utf-8") as f:
    orders=json.load(f)
total_revenue=0
orders_per_user={}
total_items_sold=0
item_count={}
top_order_total=-1
top_user=""
for order in orders:
    user=order["user"]
    total=order["total"]
    items=order["items"]
    total_revenue +=total
    if user in orders_per_user:
        orders_per_user[user] +=1
    else:
        orders_per_user[user]=1
    total_items_sold +=len(items)
    if total>top_order_total:
        top_order_total=total
        top_user=user
    for item in items:
        if item in item_count:
            item_count[item] +=1
        else:
            item_count[item] =1
most_popular_item = max(item_count, key=item_count.get)
summary = {
    "total_revenue": total_revenue,
    "top_user": top_user,
    "most_popular_item": most_popular_item,
    "total_orders": len(orders)
}
with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
#4
import csv
import json
SUSPICIOUS_LIMIT=500_000
suspicious_tx=[]
tx_count={}
suspicious_sum=0
with open("transactions.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for row in reader:
        user = row["user_id"]
        amount = int(row["amount"])
        tx_count[user]=tx_count.get(user, 0) + 1
        if amount>SUSPICIOUS_LIMIT:
            suspicious_tx.append({"user_id": user, "amount": amount})
            suspicious_sum+=amount
suspicious_users=[]
for user, cnt in tx_count.items():
    if cnt>3:
        suspicious_users.append(user)
with open("fraud_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Подозрительных транзакций: {len(suspicious_tx)}\n")
    f.write(f"Подозрительных пользователей: {len(suspicious_users)}\n")
    f.write("Список пользователей: " + (", ".join(suspicious_users) if suspicious_users else "-") + "\n")
    f.write(f"Общая сумма подозрительных операций: {suspicious_sum}\n")
with open("fraud_users.json", "w", encoding="utf-8") as f:
    json.dump(suspicious_users, f, ensure_ascii=False, indent=2)