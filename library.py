from abc import ABC, abstractmethod 

#Custom exceptions for library items
class LibraryError(Exception):
    pass

class LimitReachedError(LibraryError):
    pass

class ItemNotFoundError(LibraryError):
    pass

class MemberNotFoundError(LibraryError):
    pass

class Item(ABC):                  
    def __init__(self, item_id: str, title: str) -> None:
        self._item_id = item_id
        self._title = title
        self._available = True

    @property
    def is_available(self) -> bool:
        return self._available

    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @abstractmethod
    def loan_days(self) -> int:
        pass

    def check_out(self) -> None:
        if self._available:
            self._available = False
        else:
            raise ValueError("Item is not available for checkout")

    def return_item(self) -> None:
        if not self._available:
            self._available = True
        else:
            raise ValueError("Item is already available in the library")

    def __str__(self) -> str:
        return f"{type(self).__name__}({self._item_id}, {self._title}, available={self._available})"


class Book(Item):
    def __init__(self, item_id: str, title: str, author: str) -> None:
        super().__init__(item_id, title)
        self._author = author

    @property
    def author(self) -> str:
        return self._author

    def loan_days(self) -> int:
        return 21


class DVD(Item):
    def __init__(self, item_id: str, title: str, director: str, duration: int) -> None:
        super().__init__(item_id, title)
        self._duration = duration
        self._director = director

    @property
    def director(self) -> str:
        return self._director

    @property
    def duration(self) -> int:
        return self._duration

    def loan_days(self) -> int:
        return 7


class Member:
    MAX_ITEMS = 3  # Class variable to track the maximum number of items a member can borrow

    def __init__(self, member_id: str, name: str) -> None:
        self._member_id = member_id
        self._name = name
        self._borrowed: list[Item] = []  # List to keep track of borrowed items

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def name(self) -> str:
        return self._name
    @property
    def borrowed(self) -> list[Item]:
        return self._borrowed

    def borrow_item(self, item: Item) -> None:
        if len(self._borrowed) >= Member.MAX_ITEMS:
            raise LimitReachedError("Member has reached the maximum number of borrowed items")
        else:
            item.check_out()
            self._borrowed.append(item)

    def give_back_item(self, item: Item) -> None:
        if item not in self._borrowed:
            raise ItemNotFoundError("Member does not hold this item")
        else:
            item.return_item()
            self._borrowed.remove(item)

    def __str__(self) -> str:
        return f"Member({self._member_id}, {self._name}, borrowed={len(self._borrowed)})"

# test that item(...) raises an type error

if __name__ == "__main__":
    a = Member("m1", "Anna")
    b = Member("m2", "Ben")
    items = [Book(f"b{i}", f"Book {i}", "Author") for i in range(1, 5)]

    for it in items[:3]:
        a.borrow_item(it)
    try:
        a.borrow_item(items[3])
    except LimitReachedError as e:
        print("Limit:", e)

    try:
        b.borrow_item(items[0])          # held by Anna
    except ValueError as e:
        print("Unavailable:", e)
    print(len(b.borrowed))               # 0

    a.give_back_item(items[0])
    b.borrow_item(items[0])
    print(a, b)

    try:
        a.give_back_item(items[0])       # Anna no longer has it
    except ItemNotFoundError as e:
        print("Not held:", e)