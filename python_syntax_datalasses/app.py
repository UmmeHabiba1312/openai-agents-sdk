from dataclasses import dataclass
from typing import ClassVar
# @dataclass
# class User:
#     name: str
#     country_language : ClassVar[str] = "English"
#     national_food : ClassVar[str] = "Biryani"

#     def usr_name(self):
#         return (f"{self.name} is speaking {User.country_language}")

#     def eat_food(self):
#         return (f"{self.name} is eating {User.national_food}")

#     @staticmethod
#     def greet():
#         return User.country_language
    

# john = User(name="John")
# print(john.usr_name())
# print(john.eat_food())
# print(User.country_language)
# print(User.national_food)


@dataclass
class Human:
    name:str
    age:int

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old"
    def works(self):
        return "i am working..."
    
    def __call__(self):
        return "Hello world"
    
obj = Human(name="John", age=25)
print(obj.greet())
print(obj.works())


# this is __call__ wihtout it error will raise TypeError: 'Human' object is not callable
print(obj())

# it converts all the values into dictionary
print(obj.__dict__)


# it prints all the attributes and their types
print(obj.__annotations__)


# it prints the class name
print(obj.__class__)

# it prints the class docstring
print(obj.__doc__)

# it prints the class fields
print(obj.__dataclass_fields__)


print(obj.__format__)