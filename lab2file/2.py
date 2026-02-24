users=set()
total_buys=0
total_sum=0
user_spent={}
with open("shop_logs.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts=line.strip().split(";")
        date=parts[0]
        user=parts[1]
        act=parts[2].upper()
        users.add(user)
        if act=="BUY":
            amount=int(parts[3])
            total_buys +=1
            total_sum+=amount
            if user in user_spent:
                user_spent[user]+=amount
            else:
                user_spent[user]=amount
max_user=""
max_money=0
for u in user_spent:
    if user_spent[u]>max_money:
        max_money=user_spent[u]
        max_user=u
if total_buys>0:
    avg_check=total_sum/ total_buys
else:
    avg_check=0
with open("report.txt", "w", encoding="utf-8") as f:
    f.write(f"Уникальных пользователей: {len(users)}\n")
    f.write(f"Всего покупок: {total_buys}\n")
    f.write(f"Общая сумма продаж: {total_sum}\n")
    f.write(f"Пользователь, потративший больше всего: {max_user} ({max_money})\n")
    f.write(f"Средний чек: {avg_check:.2f}\n")
print("Excellent")
# #2
# import csv
# employees=[]
# dept_salaries={}
# with open("employees.csv", encoding="utf-8") as f:
#     reader=csv.DictReader(f)
#     for row in reader:
#         salary=int(row["salary"])
#         row["salary"]=salary
#         employees.append(row)
#         dept=row["department"]
#         if dept not in dept_salaries:
#             dept_salaries[dept]=[]
#         dept_salaries[dept].append(salary)
# total_salary=0
# for e in employees:
#     total_salary +=e["salary"]
# avg_salary=total_salary/len(employees)
# dept_avg={}
# for d in dept_salaries:
#     s=0
#     for salary in dept_salaries[d]:
#         s +=salary
#     dept_avg[d]=s/len(dept_salaries[d])
# best_dept=""
# max_avg=0
# for d in dept_avg:
#     if dept_avg[d]>max_avg:
#         max_avg=dept_avg[d]
#         best_dept=d
# top_employee=employees[0]
# for e in employees:
#     if e["salary"]>top_employee["salary"]:
#         top_employee=e
# high_paid=[]
# for e in employees:
#     if e["salary"]>avg_salary:
#         high_paid.append(e)
# with open("high_salary.csv", "w", newline="", encoding="utf-8") as f:
#     writer=csv.DictWriter(f, fieldnames=["name", "department", "salary"])
#     writer.writeheader()
#     writer.writerows(high_paid)
# print("Средняя зарплата:", avg_salary)
# print("Средняя по отделам:", dept_avg)
# print("Лучший отдел:", best_dept)
# print("Топ сотрудник:", top_employee["name"])
# print("Выше средней:", [e["name"] for e in high_paid])