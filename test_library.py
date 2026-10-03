import pytest
from library import (
    Book, DVD, Member, Library,
    ItemUnavailableError, LimitReachedError, ItemNotFoundError,
    MemberNotFoundError, DuplicateIdError
)


@pytest.fixture
def lib() -> Library:
    """A fresh library for every test."""
    library = Library()
    library.add_item(Book("b1", "Python Basics", "Someone"))
    library.add_item(DVD("d1", "Film", "Director", 90))
    library.add_item(Book("b2","Advanced Java","Najar Sb" ))
    library.add_item(DVD("d2","Peter Hujar's Day","Ira Sachs",76))
    library.add_member(Member("m1", "Anna"))
    library.add_member(Member("m2", "Ben"))
    return library


def test_book_loan_days_is_21():
    assert Book("b1", "T", "A").loan_days() == 21


def test_unknown_item_id(lib: Library):
   with pytest.raises(ItemNotFoundError):
    lib.lend_item("m1", "zzz")
    assert lib.get_member("m1").borrowed == []

def test_unknown_member_id(lib:Library):
   with pytest.raises(MemberNotFoundError):
      lib.lend_item("nobody", "b1")
   assert lib.get_item("b1") 
    

def test_member_has_reached_limit(lib: Library):
   lib.lend_item("m1","b1")
   lib.lend_item("m1", "b2")
   lib.lend_item("m1", "d1")
   with pytest.raises(LimitReachedError):
    lib.lend_item("m1","d2")
   assert lib.get_item("d2").is_available
   assert len(lib.get_member("m1").borrowed) == 3
    
        


def test_check_out_twice_raises():
    book = Book("b1", "T", "A")
    book.check_out()
    with pytest.raises(ItemUnavailableError):
        book.check_out()


def test_lend_makes_item_unavailable(lib: Library):
    before = len(lib.list_available_items())
    lib.lend_item("m1", "b1")

    assert not lib.get_item("b1").is_available
    assert len(lib.list_available_items()) == before - 1
    