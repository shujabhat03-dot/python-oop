from abc import ABC, abstractmethod
from datetime import date, timedelta 

#Custom exceptions for library items
class LibraryError(Exception):
    pass

class LimitReachedError(LibraryError):
    pass

class ItemNotFoundError(LibraryError):
    pass

class MemberNotFoundError(LibraryError):
    pass

class DuplicateIdError(LibraryError):
    pass

class ItemUnavailableError(LibraryError):
    pass


class Item(ABC):
    def __init__(self, item_id: str, title: str) -> None:
        self._item_id = item_id
        self._title = title
        self._available = True
        self._due_date: date | None = None  # Optional due date for borrowed items

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
    @property
    def due_date(self) -> date | None:
        return self._due_date
    

    def check_out(self) -> None:
        if self._available:
            self._available = False
        else:
            raise ItemUnavailableError("Item is not available for checkout")
        self._due_date = date.today() + timedelta(days=self.loan_days())

    def return_item(self) -> None:
        if not self._available:
            self._available = True
        else:
            raise ItemUnavailableError("Item is already available in the library")
        self._due_date = None  # Reset due date when item is returned
    

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
        return list(self._borrowed)  # Return a copy of the borrowed items list to prevent external modification


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
        titles = [item.title for item in self._borrowed]
        return f"Member({self._member_id}, {self._name}, borrowed={titles})"


class Library:
    def __init__(self) -> None:
        self._items: dict[str, Item] = {}  # Dictionary to store items by their ID
        self._members: dict[str, Member] = {}  # Dictionary to store members by their ID

    def add_item(self, item: Item) -> None:
        if item.item_id in self._items:
            raise DuplicateIdError("Item with this ID already exists in the library")
        self._items[item.item_id] = item

    def add_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise DuplicateIdError("Member with this ID already exists in the library")
        self._members[member.member_id] = member

    def get_item(self, item_id: str) -> Item:
        if item_id not in self._items:
            raise ItemNotFoundError("Item not found in the library")
        return self._items[item_id]

    def get_member(self, member_id: str) -> Member:
        if member_id not in self._members:
            raise MemberNotFoundError("Member not found in the library")
        return self._members[member_id]

    def lend_item(self, member_id: str, item_id: str) -> None:
        member = self.get_member(member_id)
        item = self.get_item(item_id)
        member.borrow_item(item)

    def take_back_item(self, member_id: str, item_id: str) -> None:
        member = self.get_member(member_id)
        item = self.get_item(item_id)
        member.give_back_item(item)

    def overdue_items(self, current_date: date) -> list[Item]:
        result: list[Item] = []
        for member in self._members.values():
            for item in member.borrowed:
                if item.due_date is not None and current_date > item.due_date:
                    result.append(item)
        return result 

    def list_available_items(self) -> list[Item]:
        return [item for item in self._items.values() if item.is_available]

    def search_text(self, text: str) -> list[Item]:
        return [item for item in self._items.values() if text.lower() in item.title.lower()]

    def __str__(self) -> str:
        return f"Library(items={len(self._items)}, available={len(self.list_available_items())}, members={len(self._members)})"

# demos and tests

if __name__ == "__main__":
# abstract class can't be instantiated
    try:
        Item()  # type: ignore
    except TypeError as e:
        print("TypeError:", e)

    lib = Library()
    for i in range(1, 3):
        lib.add_item(Book(f"b{i}", f"Python Book {i}", "Author"))
        lib.add_item(DVD(f"d{i}", f"Film {i}", "Director", 90))
    lib.add_member(Member("m1", "Anna"))
    lib.add_member(Member("m2", "Ben"))
    print(lib)

    # 5 first: available items before lending, after lending, after take back
    print("Available before:", len(lib.list_available_items()))      # 4
    lib.lend_item("m1", "b1")
    print("Available after lend:", len(lib.list_available_items()))  # 3
    lib.take_back_item("m1", "b1")
    print("Available after return:", len(lib.list_available_items()))  # 4

    # 1. limit: Anna borrows 3, the 4th must fail
    try:
        lib.lend_item("m1", "b1")
        lib.lend_item("m1", "b2")
        lib.lend_item("m1", "d1")
        lib.lend_item("m1", "d2")
    except LimitReachedError as e:
        print("Limit reached:", e)

    # 2. unknown ids
    try:
        lib.lend_item("m1", "b3")
    except ItemNotFoundError as e:
        print("Item not found:", e)
    try:
        lib.lend_item("m9", "d2")
    except MemberNotFoundError as e:
        print("Member not found:", e)

    # item already out: Ben tries something Anna holds
    try:
        lib.lend_item("m2", "b1")
    except ItemUnavailableError as e:
        print("Unavailable:", e)

    # 3. duplicate id
    try:
        lib.add_item(Book("b1", "Duplicate Book", "Author"))
    except DuplicateIdError as e:
        print("Duplicate item ID:", e)

    # 4. search ignores case
    print("python:", [i.title for i in lib.search_text("python")])
    print("PYTHON:", [i.title for i in lib.search_text("PYTHON")])

      # --- overdue test (fresh library) ---
    lib2 = Library()
    lib2.add_item(Book("b1", "Python Book 1", "Author"))
    lib2.add_item(DVD("d1", "Film 1", "Director", 90))
    lib2.add_member(Member("m1", "Anna"))

    lib2.lend_item("m1", "b1")    # book: due in 21 days
    lib2.lend_item("m1", "d1")    # DVD: due in 7 days

    today = date.today()
    print("Overdue today:", len(lib2.overdue_items(today)))                         # 0
    print("Overdue in 10 days:", len(lib2.overdue_items(today + timedelta(days=10))))  # 1 (the DVD)
    print("Overdue in 30 days:", len(lib2.overdue_items(today + timedelta(days=30))))  # 2 (both)