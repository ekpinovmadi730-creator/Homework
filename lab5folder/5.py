class User:
    def __init__(self,_id: int,_name:str,_email:str):
        self.id=_id
        self.name=_name.strip().title()
        self.email=_email.lower()
        if "@" not in self._email:
            raise ValueError(f"Invalid email:'{_email}'- must contain '@'")
    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email={self._email})"
    def __del__(self):
        print(f"User {self._name} deleted")
# u = User(1, " john doe ", "John@Example.COM")
# print(u)
#  # User(id=1, name='John Doe', email='john@example.com'
# del u
    @classmethod
    def from_string(cls,data:str):
        parts=data.split(",")
        _id=int(parts[0].stirp())
        _name=parts[1].strip()
        _email=parts[2].strip()
        return cls(_id, _name, _email)
class Product:
    def __init__(self, id:int, name:str, price:float, category:str):
        self.id=id
        self.name=name
        self.price=price
        self.category=category
    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category='{self.category}')"
    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id
    def t_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'category':self.category
        }
p1=Product(1, "Laptop", 1200.0, "Ecetronis")
p2=Product(2, "Phone", 800.0, "Electronics")
# __str__
print(p1)
# to_dict
print(p1.to_dict())
#set
products={p1,p2}
print(len(products))
# __eq__
print(p1==p2)
class Inventory:
    def __init__(self):
        self._products={}
    def add_product(self, product:Product):
        if product.id not in self._products:
            self.products[product.id]=product
    def remove_product(self, product_id: Product):
        self._products.pop(product_id, None)
    def get_product(self,product_id:int):
        return self._products.get(products.get(product_id))
    def get_all_product(self, product_id:int):
        return list(self._products.values())
    def unique_products(self):
        return set(self._products.values())
    def to_dict(self):
        return self._products
    def filter_by_price(self, min_price: float):
        f=lambda p: p.price>=min_price
        return [p for p in self._products.values() if f(p)]
#5
inv = Inventory()
inv.add_product(Product(1, "Laptop", 1200.0, "Electronics"))
inv.add_product(Product(2, "Mouse", 25.0, "Electronics"))

expensive = inv.filter_by_price(100.0)
print([p.name for p in expensive])
# ['Laptop']