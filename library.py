from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, item_id, title):
        self._item_id = item_id
        self._title = title
        self._available = True

    @property
    def is_available(self):
        return self._available
    @property
    def item_id(self):
        return self._item_id
    @property
    def title(self):
        return self._title
    
    @abstractmethod
    def loan_days(self):
        pass
        
    def check_out(self):
        if self._available:
            self._available = False
        else:
            raise ValueError("Item is not available for checkout")

    def return_item(self):
        if not self._available:
            self._available = True
        else:
            raise ValueError("Item is already available in the library")

    def __str__(self):  
        return f"{type(self).__name__}({self._item_id}, {self._title}, available={self._available})"

class Book(Item):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title)
        self._author = author
    @property
    def author(self):
        return self._author

    def loan_days(self):
        return 21


class DVD(Item):
    def __init__(self, item_id, director, title, duration):
        super().__init__(item_id, title)
        self._duration = duration
        self._director = director

    @property
    def director(self):
        return self._director

    @property
    def duration(self):
        return self._duration

    def loan_days(self):
        return 7


# test that item(...) raises an type error
if __name__ == "__main__":
    try:
        Item()
    except TypeError as e:
        print(f"TypeError: {e}") 
    
    book = Book("b1", "Python Basics", "Someone")
    dvd = DVD("d1", "Intro to Git", "Someone Else", 90)

    print(book)
    print(book.is_available)        # True
    book.check_out()
    print(book.is_available)        # False

    try:
        book.check_out()            # already out
    except ValueError as e:
        print("Error:", e)

    book.return_item()
    for thing in (book, dvd):
        print(thing.title, thing.loan_days())