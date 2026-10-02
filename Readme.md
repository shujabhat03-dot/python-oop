# python-oop

Python object-oriented programming practice, built while learning full stack development.

## Projects

### 1. Bank accounts (`main.py`)
- `BankAccount` with validated `deposit` and `withdraw`, and a read-only `balance` property
- `SavingsAccount` (inheritance): interest and a minimum balance rule
- Interactive menu loop using `input()` and `try/except`

### 2. Library management (`library.py`)
- Abstract class `Item` with `Book` and `DVD` subclasses (polymorphic `loan_days()`)
- `Member` with a borrowing limit, and `Library` managing items and members
- Custom exception hierarchy (`LibraryError` and subclasses)
- Due dates and an overdue report

## Concepts practiced
Classes, inheritance, `super()`, polymorphism, abstract base classes, properties,
encapsulation, custom exceptions, type hints, composition

## Run it
```bash
python3 -m venv .venv
source .venv/bin/activate
python main.py
python library.py
```