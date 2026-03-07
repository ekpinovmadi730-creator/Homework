#1
squares = [x**2 for x in range(1, 21) if x % 2 == 0]
print(squares)
#2
matrix = [[1,2,3], [4,5,6], [7,8,9]]
result = [(lambda x: x[0]*x[1]*x[2])(x) for x in matrix]
print(result)
#3
words = ["кот", "машина", "ананас", "дом"]
result = [word for word in words if len(word) > 4 and "а" not in word]
print(result)
#4
numbers = [1, 2, 3, 4, 5]
result = {n: ("чётное" if n % 2 == 0 else "нечётное") for n in numbers}
print(result)
#5
matrix = [[1,2], [3,4], [5,6]]
flat = [x for row in matrix for x in row]
print(flat)
#6
numbers = list(range(1, 21))
result = [
    "FizzBuzz" if n % 3 == 0 and n % 5 == 0 else "Fizz" if n % 3 == 0
    else "Buzz" if n % 5 == 0
    else n
    for n in numbers]
print(result)
#1
def is_prime(x):
    if x < 2:
        return False
    for i in range(2, x):
        if x % i == 0:
            return False
    return True
def special_numbers(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            yield "FizzBuzz"
        elif i % 3 == 0:
            yield "Fizz"
        elif i % 5 == 0:
            yield "Buzz"
        elif is_prime(i):
            yield "простое"
        else:
            yield i
for x in special_numbers(15):
    print(x)
#2
words = ["кот", "машина", "арбуз", "дом", "ананас"]
result = [
    (lambda w: (w.upper() if len(w) > 4 else "short") + ("*" if "а" in w else ""))(word)
    for word in words]
print(result)
#3
def process_numbers(numbers):
    positive = filter(lambda x: x >= 0, numbers)
    for n in positive:
        yield (lambda x: x/2 if x % 2 == 0 else x*3 + 1)(n)
numbers = [5, -2, 8, 0, -7, 3]
for x in process_numbers(numbers):
    print(x)
#4
students = [("Иван", 85), ("Анна", 72), ("Пётр", 90), ("Мария", 60)]
g = lambda x: "Отлично" if x >= 90 else "Хорошо" if x >= 70 else "Удовлетворительно"
r = {name: g(score) for name, score in students}
print(r)
#5
def matrix_transform(matrix):
    for row in matrix:
        for x in row:
            yield (
                "кратно 6" if x%6 == 0
                else "чётное" if x%2 == 0
                else "кратно 3" if x%3 == 0
                else x)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
for x in matrix_transform(matrix):
    print(x)
#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)
#2
words = ["кот", "машина", "арбуз", "дом"]
result = list(map(lambda w: w.upper() + "!" if len(w) > 3 else w.upper(), words))
print(result)
#3
numbers = [1,2,3,4,5,6,7,8,9,10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)
#4
numbers = [0, 5, 12, 7, 20, -3, 8]
result = list(
    map(lambda x: x/2 if x % 2 == 0 else x*3,filter(lambda x: x > 5, numbers)))
print(result)