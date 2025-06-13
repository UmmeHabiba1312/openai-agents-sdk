from dataclasses import dataclass,field
from typing import Callable
@dataclass
class Person:
    name:str
    age:str
    email: str |None  = None
    tags: list[str] = field(default_factory=list)

    def is_adult(self) -> bool:
        return self.age >= 18
    
def demo_good_usage():
    person1 = Person(name="Habiba",age=20,email="ummeyhabiab1312@gmail.com")
    person2 = Person(name="Ahmed",age=13)
    person3 = Person(name="mustafa",age=17,tags=["Student","class-10"])

    person1.tags.append("developer")

    print(f"person1:  {person1}")
    print(f"person2:  {person2}")
    print(f"person3:  {person3}")

    print(f"Is {person1.name} an adult? {person1.is_adult()}")
    print(f"Is {person3.name} an adult? {person3.is_adult()}")

if __name__ == "__main__":
    print("--Goods DataClasses Example--\n")
    demo_good_usage()


# # callable

@dataclass
class Calculator:
    operation = Callable[[int,int] ,str]
    def calculate(self, num1: int, num2: int) -> str:
        return self.operation(num1, num2)
    
def add(num1: int, num2: int)-> str:
    return str(num1 + num2)

calc = Calculator(operation=add)
print(calc.calculate(6,7))


# # second method to make it callable
@dataclass
class Calculator:
    operation : Callable[[int,int] ,str]
    def __call__(self, num1: int, num2: int) -> str:
        return self.operation(num1, num2)
    
def add(num1: int, num2: int)-> str:
    return str(num1 + num2)

calc = Calculator(operation=add)
print(calc(6,7))



# Generics

from typing import TypeVar
T = TypeVar("T")

# # use generics instead of Any type
def generics_first_elem(items:list[T])->T:
    return items[0]

nums = [1,2,3,4,5,6,7]
string = ['a','b','c','d','e','f','g']

res = generics_first_elem(nums)
res2 = generics_first_elem(string)

print(res)  # print 1
print(res2)  # print a


# # generics for dictionary

# from typing import TypeVar

# K = TypeVar("K")   # k for key
# V = TypeVar("V")  # v for key
 
# def get_item(container: dict[K, V], key:K)->V:
#     return container[key]


# d1 = { "a": 1, "b": 2, "c":3}
# value = get_item(d1, "a")

# print(value)


# # for dataclass
# from typing import TypeVar , Generic, ClassVar
# from dataclasses import dataclass , field
# T = TypeVar("T")

# @dataclass
# class Stack(Generic[T]):
#     items : list[T] = field(default_factory=list)
#     limit : ClassVar[int] = 10

#     def push(self, item: T) -> None:
#         self.items.append(item)

#     def pop(self) -> T:
#         return self.items.pop()
    

# stack_of_ints = Stack[int]()
# print(stack_of_ints)
# print(stack_of_ints.limit)

# stack_of_ints.push(1)
# stack_of_ints.push(2)
# stack_of_ints.push(3)
# stack_of_ints.push(4)

# print(stack_of_ints.pop()) 
# print(stack_of_ints)
