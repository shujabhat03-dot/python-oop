class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} says Woof!")

    def birthday(self):
        self.age += 1
        print(f"{self.name} is now {self.age}")


rex = Dog("Rex", 3)
rex.bark()
rex.birthday()