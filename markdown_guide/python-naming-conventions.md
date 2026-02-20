# Python Naming Conventions — The Complete Guide

> Covers PEP 8, PEP 257, PEP 526, PEP 544, PEP 695, Google Python Style Guide, and modern Python 3.10+ community standards.

---

## Table of Contents

1. [General Principles](#1-general-principles)
2. [Variables](#2-variables)
3. [Constants](#3-constants)
4. [Functions](#4-functions)
5. [Classes](#5-classes)
6. [Abstract Classes](#6-abstract-classes)
7. [Dataclasses](#7-dataclasses)
8. [Protocols (Structural Subtyping)](#8-protocols-structural-subtyping)
9. [Methods](#9-methods)
10. [Properties](#10-properties)
11. [Private / Protected Members](#11-private--protected-members)
12. [Parameters](#12-parameters)
13. [Type Hints & Generics](#13-type-hints--generics)
14. [Modules & Packages](#14-modules--packages)
15. [Files & Directories](#15-files--directories)
16. [Boolean Variables](#16-boolean-variables)
17. [Exceptions](#17-exceptions)
18. [Enums](#18-enums)
19. [Decorators](#19-decorators)
20. [Comprehensions & Lambda](#20-comprehensions--lambda)
21. [Async / Coroutines](#21-async--coroutines)
22. [Dunder (Magic) Names](#22-dunder-magic-names)
23. [Django Conventions](#23-django-conventions)
24. [FastAPI / Pydantic Conventions](#24-fastapi--pydantic-conventions)
25. [Test Files & Test Identifiers](#25-test-files--test-identifiers)
26. [Abbreviations & Acronyms](#26-abbreviations--acronyms)
27. [Naming Anti-patterns](#27-naming-anti-patterns)
28. [Quick Reference Cheatsheet](#28-quick-reference-cheatsheet)
29. [References & Further Reading](#29-references--further-reading)

---

## 1. General Principles

- **Follow PEP 8** — the official Python style guide. It is the baseline for all Python projects.
- **Be descriptive, not terse.** `user_account_list` beats `ul` or `data`.
- **Be consistent.** Pick one convention per construct and never mix.
- **Avoid abbreviations** unless they are universally known (`url`, `id`, `http`, `api`, `db`).
- **Pronounceable names.** If you can't say it out loud, reconsider.
- **Don't encode the type in the name** (Hungarian notation): `str_name` → `name`, `list_items` → `items`.
- **Avoid noise words**: `data`, `info`, `object`, `manager` add no meaning unless necessary.
- **Use positive naming for booleans**: `is_loading`, not `is_not_loading`.
- **Avoid single-letter names** except for loop counters (`i`, `j`, `k`), math (`x`, `y`, `z`), or short lambdas.
- **`_` (single underscore)** as a throwaway variable name for values you don't need.

---

## 2. Variables

Use **snake_case** (PEP 8).

```python
# ✅ Good
user_name = "Alice"
item_count = 42
fetched_users = []
order_total = 99.95
is_active = True

# ❌ Bad
userName = "Alice"       # camelCase (JS style)
UserName = "Alice"       # PascalCase (class style)
usrnm = "Alice"          # cryptic abbreviation
strUserName = "Alice"    # Hungarian notation

# ✅ Throwaway variable
for _ in range(10):
    do_something()

_, last_name = get_name_parts()
```

### Naming patterns by data type

| Data | Example |
|------|---------|
| String | `first_name`, `page_title` |
| Integer | `item_count`, `max_retries`, `page_index` |
| Float | `total_price`, `tax_rate` |
| List | `users`, `order_items`, `selected_ids` (plural nouns) |
| Tuple | `coordinates`, `rgb_color`, `date_range` |
| Dict | `user_by_id`, `config`, `headers` |
| Set | `active_ids`, `unique_emails` |
| Optional | same name, type hint handles it: `user: User \| None` |
| Callable | `callback`, `formatter`, `comparator`, `predicate` |

---

## 3. Constants

Use **SCREAMING_SNAKE_CASE** (PEP 8). Place at module level.

```python
# ✅ Good
MAX_RETRY_COUNT = 3
API_BASE_URL = "https://api.example.com"
DEFAULT_TIMEOUT_SEC = 30
PI = 3.14159265358979
DB_CONNECTION_STRING = "postgresql://localhost/mydb"

# ❌ Bad
maxRetryCount = 3           # camelCase
max_retry_count = 3         # looks like a variable
MaxRetryCount = 3           # PascalCase (class style)
```

### Module-level "constants" that are mutable

If a module-level object is mutable but conceptually constant, still use SCREAMING_SNAKE_CASE:

```python
# ✅ Acceptable — dict is mutable but semantically constant
DEFAULT_HEADERS: dict[str, str] = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

SUPPORTED_FORMATS: list[str] = ["json", "xml", "csv"]
```

### Class-level constants

```python
class HttpStatus:
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class Order:
    MAX_ITEMS = 50
    DEFAULT_CURRENCY = "USD"
    TAX_RATE = 0.2
```

---

## 4. Functions

Use **snake_case** (PEP 8). Name with a **verb** or **verb phrase**.

```python
# ✅ Good
def get_user_by_id(user_id: int) -> User: ...
def calculate_total_price(items: list[CartItem]) -> float: ...
def format_date(date: datetime) -> str: ...
def is_email_valid(email: str) -> bool: ...
def fetch_orders_from_api(page: int = 1) -> list[Order]: ...

# ❌ Bad
def User(user_id: int) -> User: ...       # noun only, uppercase
def GetUser(user_id: int) -> User: ...    # PascalCase (class style)
def g(user_id: int) -> User: ...          # meaningless
def userData(user_id: int) -> User: ...   # camelCase
```

### Common verb prefixes

| Prefix | Use case | Example |
|--------|----------|---------|
| `get` | Returns a value | `get_user_by_id()`, `get_total()` |
| `fetch` | External / async retrieval | `fetch_users()`, `fetch_from_api()` |
| `find` | Search, may return `None` | `find_by_email()`, `find_or_none()` |
| `set` | Sets / updates a value | `set_user_name()` |
| `update` | Partial update | `update_profile()` |
| `create` | Factory / instantiation | `create_order()` |
| `make` | Same as create | `make_request()` |
| `build` | Builder pattern | `build_query()` |
| `handle` | Action / event handler | `handle_submit()` |
| `process` | Multi-step action | `process_payment()` |
| `is` / `has` / `can` / `should` | Boolean predicate | `is_admin()`, `has_permission()` |
| `check` | Validation, may raise | `check_auth()` |
| `validate` | Returns bool or raises | `validate_email()` |
| `parse` | Transforms raw data | `parse_response()` |
| `format` | Transforms for display | `format_currency()` |
| `calculate` / `compute` | Math / derived values | `calculate_discount()` |
| `render` | Returns output string/html | `render_template()` |
| `init` / `initialize` | Setup | `init_database()` |
| `reset` | Restore to defaults | `reset_form()` |
| `load` | Load data | `load_config()` |
| `save` / `store` | Persist data | `save_settings()` |
| `delete` / `remove` | Deletion | `delete_user()`, `remove_item()` |
| `clear` | Empty a collection | `clear_cache()` |
| `send` | Communication | `send_email()` |
| `emit` | Events | `emit_change()` |
| `dispatch` | Queue / events | `dispatch_job()` |
| `subscribe` | Pub/sub | `subscribe_to_events()` |
| `resolve` | DI / async resolution | `resolve_dependency()` |
| `map` / `transform` | Shape transformation | `map_to_dto()` |
| `convert` | Type conversion | `convert_to_csv()` |
| `serialize` / `deserialize` | Encoding | `serialize_user()` |

---

## 5. Classes

Use **PascalCase** (PEP 8). Name with a **noun** or **noun phrase**.

```python
# ✅ Good
class UserRepository: ...
class ShoppingCart: ...
class AuthenticationService: ...
class HttpClient: ...
class EventDispatcher: ...

# ❌ Bad
class userRepository: ...    # snake_case
class manage_users: ...      # snake_case verb
class USERREPOSITORY: ...    # all caps
class doUserStuff: ...       # camelCase verb
```

### Naming suffixes by responsibility

| Suffix | Purpose | Example |
|--------|---------|---------|
| `Service` | Business logic | `UserService`, `PaymentService` |
| `Repository` | Data access | `UserRepository`, `OrderRepository` |
| `Manager` | Lifecycle management | `ConnectionManager`, `CacheManager` |
| `Handler` | Handles command/event | `CreateOrderHandler` |
| `Controller` | Request handling (web) | `UserController` |
| `Middleware` | HTTP pipeline | `AuthMiddleware`, `CorsMiddleware` |
| `Factory` | Object creation | `UserFactory`, `SessionFactory` |
| `Builder` | Fluent construction | `QueryBuilder`, `RequestBuilder` |
| `Client` | External API wrapper | `HttpClient`, `SlackClient` |
| `Command` | Command object (CQRS) | `CreateOrderCommand` |
| `Query` | Query object (CQRS) | `GetUserQuery` |
| `Event` | Domain event | `UserCreatedEvent`, `OrderPaidEvent` |
| `Listener` | Handles event | `SendWelcomeEmailListener` |
| `Observer` | Observer pattern | `MetricsObserver` |
| `Processor` | Data processing | `ImageProcessor`, `BatchProcessor` |
| `Validator` | Validation logic | `EmailValidator`, `PasswordValidator` |
| `Serializer` | Serialization | `JsonSerializer`, `UserSerializer` |
| `Formatter` | Formatting | `DateFormatter`, `CurrencyFormatter` |
| `Parser` | Parsing | `HtmlParser`, `CsvParser` |
| `Converter` | Type conversion | `CsvConverter`, `XmlConverter` |
| `Adapter` | Adapter pattern | `DatabaseAdapter`, `CacheAdapter` |
| `Decorator` | Decorator pattern | `LoggingDecorator`, `CachingRepository` |
| `Mixin` | Mixin class | `TimestampMixin`, `SerializableMixin` |
| `Schema` | Validation schema (Pydantic) | `UserSchema`, `CreateOrderSchema` |
| `Model` | ORM model | `User`, `Order` (Django style: no suffix) |
| `View` | Django view | `UserListView`, `LoginView` |
| `Serializer` | DRF serializer | `UserSerializer` |
| `Exception` / `Error` | Custom exception | `UserNotFoundError`, `ValidationException` |
| `Config` | Configuration object | `DatabaseConfig`, `AppConfig` |
| `Settings` | Settings class | `DevelopmentSettings` |

---

## 6. Abstract Classes

Use `ABC` from the `abc` module. Name as a plain noun (what it represents) or prefix with `Abstract` / `Base`:

```python
from abc import ABC, abstractmethod

# ✅ Option 1 — plain noun (Pythonic, used in stdlib)
class Repository(ABC):
    @abstractmethod
    def find_by_id(self, entity_id: int) -> object | None: ...

    @abstractmethod
    def save(self, entity: object) -> None: ...


# ✅ Option 2 — Base prefix (common in large projects)
class BaseRepository(ABC):
    @abstractmethod
    def find_by_id(self, entity_id: int) -> object | None: ...


# ✅ Option 3 — Abstract prefix (explicit)
class AbstractSerializer(ABC):
    @abstractmethod
    def serialize(self, data: dict) -> str: ...

    @abstractmethod
    def deserialize(self, raw: str) -> dict: ...


# ❌ Bad
class repositoryAbstract(ABC): ...   # wrong order + case
class IRepository(ABC): ...          # I prefix (Java/C# style)
```

---

## 7. Dataclasses

Use **PascalCase** (same as classes). Field names use **snake_case**:

```python
from dataclasses import dataclass, field
from datetime import datetime

# ✅ Good
@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    roles: list[str] = field(default_factory=list)


@dataclass(frozen=True)   # immutable — good for value objects
class Money:
    amount: float
    currency: str = "USD"


@dataclass
class CreateUserDto:
    first_name: str
    last_name: str
    email: str
    role: str = "viewer"


# ❌ Bad
@dataclass
class user_dto:            # snake_case
    FirstName: str         # PascalCase field
    strEmail: str          # Hungarian notation
```

---

## 8. Protocols (Structural Subtyping)

Use **PascalCase** (PEP 544). Protocols describe capabilities — name as adjectives or noun phrases:

```python
from typing import Protocol, runtime_checkable

# ✅ Adjective / capability (preferred)
class Serializable(Protocol):
    def serialize(self) -> str: ...

class Comparable(Protocol):
    def __lt__(self, other: object) -> bool: ...

class Closeable(Protocol):
    def close(self) -> None: ...

# ✅ Noun phrase for interfaces
class UserRepository(Protocol):
    def find_by_id(self, user_id: int) -> "User | None": ...
    def save(self, user: "User") -> None: ...

# ✅ Runtime checkable
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

# ❌ Bad
class IUserRepository(Protocol): ...    # I prefix
class userRepository(Protocol): ...    # snake_case
```

---

## 9. Methods

Use **snake_case** (PEP 8). Same verb conventions as functions.

```python
class UserService:
    # ✅ Good
    def get_user_by_id(self, user_id: int) -> User: ...
    def create_user(self, dto: CreateUserDto) -> User: ...
    def update_user_email(self, user_id: int, email: str) -> None: ...
    def delete_user(self, user_id: int) -> None: ...
    def is_admin(self, user: User) -> bool: ...
    def has_permission(self, user: User, action: str) -> bool: ...

    # ❌ Bad
    def User(self, user_id: int) -> User: ...           # noun
    def GET_USER(self, user_id: int) -> User: ...       # screaming
    def getUserById(self, user_id: int) -> User: ...    # camelCase
    def u(self, user_id: int) -> User: ...              # meaningless


# Class methods
class User:
    @classmethod
    def from_dict(cls, data: dict) -> "User": ...       # factory

    @classmethod
    def create_guest(cls) -> "User": ...                # named constructor

    @staticmethod
    def validate_email(email: str) -> bool: ...         # utility
```

---

## 10. Properties

Use **`@property`** decorator. Name as a noun (what it represents), not a verb:

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    # ✅ noun — describes what it IS
    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:                    # computed property — noun
        return 3.14159 * self._radius ** 2

    @property
    def diameter(self) -> float:
        return self._radius * 2


class User:
    def __init__(self, first_name: str, last_name: str) -> None:
        self._first_name = first_name
        self._last_name = last_name

    @property
    def full_name(self) -> str:                 # ✅ noun phrase
        return f"{self._first_name} {self._last_name}"

    @property
    def is_verified(self) -> bool:              # ✅ boolean — is_ prefix
        return bool(self._email_verified_at)
```

---

## 11. Private / Protected Members

Python uses naming conventions (not access modifiers) to signal visibility:

### Single underscore `_` — "internal use" / protected

```python
class UserService:
    def __init__(self) -> None:
        self._cache: dict[int, User] = {}    # protected — subclasses can use
        self._logger = logging.getLogger(__name__)

    def _validate_user_data(self, data: dict) -> None:  # internal method
        ...

    def _get_from_cache(self, user_id: int) -> User | None:
        return self._cache.get(user_id)
```

### Double underscore `__` — name-mangled (truly private)

```python
class BankAccount:
    def __init__(self, balance: float) -> None:
        self.__balance = balance              # name-mangled to _BankAccount__balance
        self.__transaction_log: list = []

    def __validate_amount(self, amount: float) -> None:  # private method
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def deposit(self, amount: float) -> None:
        self.__validate_amount(amount)
        self.__balance += amount
```

> Use `__` sparingly. It prevents subclassing from being straightforward. Prefer `_` for most "private" use cases.

### Module-level private

```python
# Single underscore prefix — not exported by `from module import *`
_internal_helper = {}
_MAX_CONNECTIONS = 10

def _build_query(params: dict) -> str: ...    # internal function
```

---

## 12. Parameters

Use **snake_case**. Be descriptive:

```python
# ✅ Good
def create_user(first_name: str, last_name: str, role: UserRole) -> User: ...
def fetch_orders(start_date: date, end_date: date, page: int = 1) -> list[Order]: ...

# ❌ Bad
def create_user(fn: str, ln: str, r: UserRole) -> User: ...   # cryptic
def fetch_orders(s: date, e: date, p: int) -> list[Order]: ...  # meaningless


# Variadic — use plural noun
def log_messages(*messages: str) -> None: ...
def merge_dicts(**kwargs: Any) -> dict: ...

# ✅ kwargs naming — use descriptive keys when possible
def create_response(*, status_code: int, body: str, headers: dict | None = None) -> Response:
    ...
```

### Avoid shadowing built-ins

```python
# ❌ Bad — shadows built-ins
def process(list: list[str]) -> None: ...
def get_item(id: int) -> Item: ...         # 'id' is a built-in, use item_id
def filter_users(type: str) -> None: ...   # 'type' is a built-in, use user_type

# ✅ Good
def process(items: list[str]) -> None: ...
def get_item(item_id: int) -> Item: ...
def filter_users(user_type: str) -> None: ...
```

### `*` (keyword-only) and `/` (positional-only) separators

```python
def create_user(
    first_name: str,
    last_name: str,
    /,                        # positional-only above
    *,                        # keyword-only below
    email: str,
    role: UserRole = UserRole.VIEWER,
    is_active: bool = True,
) -> User: ...
```

---

## 13. Type Hints & Generics

### Basic type hints (Python 3.9+)

```python
# ✅ Modern Python 3.9+ — use built-in generics
def get_users() -> list[User]: ...
def get_user_map() -> dict[str, User]: ...
def find_user(user_id: int) -> User | None: ...  # Python 3.10+ union syntax

# ✅ Python 3.8 compatible
from typing import List, Dict, Optional, Union
def get_users() -> List[User]: ...
def find_user(user_id: int) -> Optional[User]: ...
```

### TypeVar — use single uppercase letter or descriptive name

```python
from typing import TypeVar

# Simple generic
T = TypeVar("T")
U = TypeVar("U")

# Constrained TypeVar
AnyStr = TypeVar("AnyStr", str, bytes)

# Bound TypeVar
Comparable = TypeVar("Comparable", bound="SupportsLessThan")

# Descriptive names for domain-specific generics
TEntity = TypeVar("TEntity")
TId = TypeVar("TId", int, str)
TKey = TypeVar("TKey")
TValue = TypeVar("TValue")
TReturn = TypeVar("TReturn")
```

### Generic classes

```python
from typing import Generic

class Repository(Generic[TEntity, TId]):
    def find_by_id(self, entity_id: TId) -> TEntity | None: ...
    def save(self, entity: TEntity) -> TEntity: ...
    def delete(self, entity_id: TId) -> None: ...


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

### TypeAlias (PEP 613 / PEP 695)

```python
# Python 3.10+ (PEP 613)
from typing import TypeAlias

UserId: TypeAlias = int
Callback: TypeAlias = Callable[[str], None]
JsonDict: TypeAlias = dict[str, Any]
Matrix: TypeAlias = list[list[float]]

# Python 3.12+ (PEP 695 — cleaner syntax)
type UserId = int
type Callback = Callable[[str], None]
type JsonDict = dict[str, Any]
```

### Common type hint patterns

```python
from typing import Any, Callable, Iterator, Generator, AsyncIterator
from collections.abc import Sequence, Mapping, MutableMapping

# Callable
formatter: Callable[[str], str]
predicate: Callable[[User], bool]
factory: Callable[[], User]

# Sequences
def process_items(items: Sequence[str]) -> None: ...   # read-only
def modify_items(items: list[str]) -> None: ...        # mutable

# Generator
def read_lines(path: str) -> Generator[str, None, None]: ...

# Overloads for multiple signatures
from typing import overload

@overload
def process(value: str) -> str: ...
@overload
def process(value: int) -> int: ...
def process(value: str | int) -> str | int:
    ...
```

---

## 14. Modules & Packages

Use **short, lowercase, no underscores if possible** (PEP 8). Underscores are acceptable for readability:

```python
# ✅ Good module names
import users
import auth
import utils
import http_client
import email_validator
import database

# ✅ Acceptable with underscore
import user_service
import order_repository

# ❌ Bad
import Users           # PascalCase
import userService     # camelCase
import user-service    # hyphen (not valid in Python)
import UserRepository  # PascalCase
```

### Package (directory) names — same rules

```
myproject/
  auth/
    __init__.py
    service.py
    models.py
    views.py
  users/
    __init__.py
    service.py
    repository.py
    schemas.py
  core/
    __init__.py
    config.py
    exceptions.py
    middleware.py
  utils/
    __init__.py
    date_helpers.py
    string_helpers.py
    validators.py
```

### `__all__` — explicit public API

```python
# module.py
__all__ = [
    "UserService",
    "UserRepository",
    "get_user_by_id",
]

# Not listed — considered private even without underscore
_internal_state: dict = {}
```

---

## 15. Files & Directories

### Python source files — snake_case

```
# ✅ Good
user_service.py
shopping_cart.py
auth_middleware.py
format_date.py
http_client.py
create_user_command.py

# ❌ Bad
UserService.py         # PascalCase
userService.py         # camelCase
user-service.py        # hyphen (not importable)
```

### Special files

```
__init__.py            # package marker + public API
__main__.py            # entry point for `python -m package`
conftest.py            # pytest fixtures
settings.py            # application settings
config.py              # configuration
constants.py           # module-level constants
exceptions.py          # custom exceptions
types.py               # type aliases
utils.py               # utility functions
helpers.py             # helper functions
```

### Directory structure examples

```
# Django project
myapp/
  migrations/
    0001_initial.py
    0002_add_email_verified.py
  templates/
    myapp/
      user_list.html
      user_detail.html
  static/
    myapp/
      style.css

# FastAPI project
app/
  api/
    v1/
      endpoints/
        users.py
        orders.py
      __init__.py
  core/
    config.py
    security.py
  models/
    user.py
    order.py
  schemas/
    user.py
    order.py
  services/
    user_service.py
    order_service.py
  repositories/
    user_repository.py
```

---

## 16. Boolean Variables

Use **`is_`, `has_`, `can_`, `should_`, `was_`, `did_`** prefixes:

```python
# ✅ Good
is_loading = False
is_authenticated = False
is_active = True
is_verified = True
has_errors = False
has_permission = True
can_edit = False
can_delete = False
should_refetch = True
was_modified = False
did_submit = False

# In dataclasses / models
@dataclass
class User:
    is_active: bool = True
    is_verified: bool = False
    has_subscription: bool = False

# ❌ Bad
loading = False          # ambiguous — could be a loading object
authenticated = False    # adjective without prefix
errors = False           # sounds like list of errors
edit_permission = False  # noun phrase, unclear it's boolean
```

---

## 17. Exceptions

Use **PascalCase** with `Error` suffix (stdlib convention) or `Exception` suffix:

```python
# ✅ Good — Error suffix (matches Python stdlib style: ValueError, TypeError...)
class UserNotFoundError(Exception): ...
class InvalidEmailError(ValueError): ...
class PaymentFailedError(RuntimeError): ...
class AuthorizationError(PermissionError): ...
class DuplicateEmailError(ValueError): ...
class InsufficientFundsError(ValueError): ...
class ApiConnectionError(ConnectionError): ...
class ConfigurationError(RuntimeError): ...

# ✅ Also acceptable — Exception suffix
class UserNotFoundException(Exception): ...
class ValidationException(Exception): ...

# ❌ Bad
class UserException(Exception): ...     # too vague
class BadUser(Exception): ...           # "bad" adds no info
class user_not_found(Exception): ...    # snake_case
```

### Exception hierarchy

```python
# Base domain exception
class DomainError(Exception):
    """Base class for all domain errors."""


class UserError(DomainError):
    """Base class for user-related errors."""


class UserNotFoundError(UserError):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"User with id={user_id} not found")
        self.user_id = user_id


class UserAlreadyExistsError(UserError):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email={email!r} already exists")
        self.email = email


# Infrastructure exceptions
class DatabaseError(RuntimeError): ...
class ConnectionTimeoutError(DatabaseError): ...

# Application exceptions
class ValidationError(ValueError):
    def __init__(self, errors: dict[str, list[str]]) -> None:
        super().__init__("Validation failed")
        self.errors = errors
```

---

## 18. Enums

Use **PascalCase** for the enum class. Use **SCREAMING_SNAKE_CASE** for members (PEP 8):

```python
from enum import Enum, IntEnum, Flag, auto

# ✅ Good — string enum
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# ✅ Int enum
class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# ✅ Auto-numbered
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


# ✅ Flag enum (bitmask)
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    ALL = READ | WRITE | EXECUTE


# ❌ Bad
class userRole(Enum):            # camelCase
    admin = "admin"               # lowercase member (avoid)
    Admin = "admin"               # PascalCase member


# Usage
role = UserRole.ADMIN
role.value   # "admin"
UserRole("admin")  # UserRole.ADMIN
```

---

## 19. Decorators

Use **snake_case** for decorator functions, **PascalCase** for decorator classes:

```python
import functools

# ✅ Decorator functions — snake_case
def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper

def cache(timeout: int = 300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return decorator

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return decorator


# ✅ Decorator classes — PascalCase
class Singleton:
    _instances: dict = {}

    def __call__(self, cls):
        if cls not in self._instances:
            self._instances[cls] = cls()
        return self._instances[cls]


class Memoize:
    def __init__(self, func):
        self.func = func
        self.cache: dict = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]


# Usage
@login_required
@cache(timeout=60)
def get_dashboard_data() -> dict: ...

@Singleton()
class DatabaseConnection: ...

@Memoize
def fibonacci(n: int) -> int: ...
```

---

## 20. Comprehensions & Lambda

### Comprehensions — keep short variable names acceptable

```python
# ✅ Short names acceptable in comprehensions (scope is clear)
squares = [x**2 for x in range(10)]
even_numbers = [n for n in numbers if n % 2 == 0]
user_names = [user.name for user in users]
user_map = {user.id: user for user in users}
active_ids = {user.id for user in users if user.is_active}

# ✅ Nested — use descriptive names to avoid confusion
flat = [item for sublist in matrix for item in sublist]
order_items = [item for order in orders for item in order.items if item.is_available]
```

### Lambda — keep short, assign meaningful names

```python
# ✅ Acceptable — simple transforms
sort_key = lambda user: user.last_name
formatter = lambda x: f"${x:.2f}"
is_positive = lambda n: n > 0

# ✅ Better — use def for anything non-trivial
def sort_by_last_name(user: User) -> str:
    return user.last_name

users.sort(key=sort_by_last_name)

# ❌ Complex lambdas are hard to read — use def
transform = lambda x: x * 2 + 1 if x > 0 else abs(x) - 3   # BAD
```

---

## 21. Async / Coroutines

Use same naming rules as regular functions. No special prefix needed — `async def` signals it:

```python
import asyncio

# ✅ Good — async functions
async def fetch_user(user_id: int) -> User: ...
async def create_order(dto: CreateOrderDto) -> Order: ...
async def send_notification(user: User, message: str) -> None: ...

# ✅ Async generators
async def stream_events() -> AsyncIterator[Event]: ...
async def read_lines(path: str) -> AsyncGenerator[str, None]: ...

# ✅ Async context managers
class DatabaseSession:
    async def __aenter__(self) -> "DatabaseSession": ...
    async def __aexit__(self, *args) -> None: ...

# ✅ Async iterators
class EventStream:
    def __aiter__(self) -> "EventStream": ...
    async def __anext__(self) -> Event: ...


# ❌ Bad — misleading prefix
async def async_get_user(user_id: int) -> User: ...   # redundant "async_"
async def coroutine_fetch(url: str) -> bytes: ...     # redundant "coroutine_"


# Variable names for awaitables
user_coro = fetch_user(1)               # coroutine object
user = await fetch_user(1)              # resolved value (not "user_coro" after await)

# asyncio.Task
user_task = asyncio.create_task(fetch_user(1))   # Task, not the result
```

---

## 22. Dunder (Magic) Names

All dunder names are **`__lowercase__`** (language convention, not configurable):

```python
class User:
    # Object lifecycle
    def __init__(self, name: str) -> None: ...
    def __del__(self) -> None: ...
    def __new__(cls) -> "User": ...

    # String representation
    def __repr__(self) -> str: ...      # unambiguous, for developers
    def __str__(self) -> str: ...       # human-readable

    # Comparison
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: "User") -> bool: ...
    def __le__(self, other: "User") -> bool: ...
    def __hash__(self) -> int: ...

    # Container protocol
    def __len__(self) -> int: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, item: Any) -> bool: ...
    def __iter__(self) -> Iterator: ...
    def __next__(self) -> Any: ...

    # Arithmetic
    def __add__(self, other: "User") -> "User": ...
    def __mul__(self, n: int) -> "User": ...

    # Context manager
    def __enter__(self) -> "User": ...
    def __exit__(self, *args) -> None: ...

    # Callable
    def __call__(self, *args, **kwargs) -> Any: ...

    # Attribute access
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...

    # Serialization
    def __reduce__(self) -> tuple: ...
    def __getstate__(self) -> dict: ...
    def __setstate__(self, state: dict) -> None: ...

    # Async context manager
    async def __aenter__(self) -> "User": ...
    async def __aexit__(self, *args) -> None: ...


# Module-level dunders
__version__ = "1.0.0"
__author__ = "Alice Smith"
__all__ = ["User", "UserService"]
__slots__ = ("name", "email")   # in class
```

---

## 23. Django Conventions

### Models — singular PascalCase (no suffix)

```python
from django.db import models

# ✅ Good
class User(models.Model): ...
class Order(models.Model): ...
class BlogPost(models.Model): ...

# ❌ Bad
class Users(models.Model): ...      # plural
class UserModel(models.Model): ...  # redundant Model suffix


class User(models.Model):
    # ✅ Fields — snake_case
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ ForeignKey — singular snake_case
    role = models.ForeignKey("Role", on_delete=models.PROTECT)

    # ✅ ManyToMany — plural snake_case
    groups = models.ManyToManyField("Group", blank=True)

    class Meta:
        db_table = "users"                    # snake_case
        ordering = ["-created_at"]
        verbose_name = "user"                 # lowercase
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:           # ✅ verb phrase method
        return f"{self.first_name} {self.last_name}"
```

### Views — PascalCase + `View` suffix

```python
from django.views import View
from django.views.generic import ListView, DetailView

# ✅ Class-based views
class UserListView(ListView): ...
class UserDetailView(DetailView): ...
class UserCreateView(CreateView): ...
class UserUpdateView(UpdateView): ...
class UserDeleteView(DeleteView): ...
class LoginView(View): ...

# ✅ Function-based views — snake_case
def user_list(request): ...
def user_detail(request, pk: int): ...
def login_view(request): ...
```

### URLs — snake_case names

```python
# urls.py
urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("users/create/", views.UserCreateView.as_view(), name="user_create"),
]
```

### Serializers (DRF) — PascalCase + `Serializer`

```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer): ...
class CreateUserSerializer(serializers.Serializer): ...
class UserDetailSerializer(serializers.ModelSerializer): ...
```

### Templates — snake_case

```
templates/
  users/
    user_list.html
    user_detail.html
    user_form.html
    user_confirm_delete.html
  partials/
    _user_card.html        ← partial, prefixed with _
    _pagination.html
  base.html
```

---

## 24. FastAPI / Pydantic Conventions

### Pydantic models — PascalCase

```python
from pydantic import BaseModel, Field
from datetime import datetime

# ✅ Request schemas
class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: str = "viewer"

class UpdateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

# ✅ Response schemas
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2

# ✅ Nested schemas
class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class OrderSchema(BaseModel):
    items: list[OrderItemSchema]
    shipping_address: str
    notes: str | None = None
```

### FastAPI routers and endpoints

```python
from fastapi import APIRouter, Depends

# ✅ Router — snake_case module, APIRouter instance
router = APIRouter(prefix="/users", tags=["users"])

# ✅ Endpoint functions — snake_case + verb
@router.get("/", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]: ...

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends()) -> UserResponse: ...

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(request: CreateUserRequest, service: UserService = Depends()) -> UserResponse: ...

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, request: UpdateUserRequest, service: UserService = Depends()) -> UserResponse: ...

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, service: UserService = Depends()) -> None: ...
```

### Dependency functions — snake_case

```python
# ✅ Dependency providers — snake_case
def get_db() -> Generator[Session, None, None]: ...
def get_user_service(db: Session = Depends(get_db)) -> UserService: ...
def get_current_user(token: str = Depends(oauth2_scheme)) -> User: ...
def require_admin(current_user: User = Depends(get_current_user)) -> User: ...
```

---

## 25. Test Files & Test Identifiers

### Test file naming

```
tests/
  unit/
    test_user_service.py         ← unit test
    test_user_repository.py
  integration/
    test_user_controller.py
  e2e/
    test_user_registration.py
  conftest.py                    ← shared fixtures
```

> Files **must** start with `test_` (pytest convention) or end with `_test.py`.

### Test functions and methods — snake_case, descriptive

```python
# ✅ pytest style
def test_get_user_returns_user_when_found(): ...
def test_get_user_raises_error_when_not_found(): ...
def test_create_user_stores_hashed_password(): ...
def test_create_user_raises_error_on_duplicate_email(): ...

# ✅ Class-based (grouped by subject)
class TestUserService:
    def test_get_user_by_id_returns_correct_user(self): ...
    def test_get_user_by_id_raises_user_not_found_error(self): ...
    def test_create_user_sets_default_role(self): ...


class TestUserRepository:
    def test_find_by_email_returns_user_when_exists(self): ...
    def test_find_by_email_returns_none_when_not_found(self): ...


# ❌ Bad
def test_user(): ...             # vague
def test_it_works(): ...         # vague
def testGetUser(): ...           # camelCase (unittest style in pytest — inconsistent)
def test1(): ...                 # meaningless
```

### Fixtures — snake_case nouns

```python
import pytest

# ✅ Good — noun naming
@pytest.fixture
def user() -> User:
    return User(id=1, name="Alice", email="alice@example.com")

@pytest.fixture
def admin_user() -> User:
    return User(id=2, name="Bob", role=UserRole.ADMIN)

@pytest.fixture
def user_service(mock_repository: UserRepository) -> UserService:
    return UserService(repository=mock_repository)

@pytest.fixture
def mock_repository() -> MagicMock:
    return MagicMock(spec=UserRepository)

# ✅ Scoped fixtures
@pytest.fixture(scope="session")
def db_engine(): ...

@pytest.fixture(scope="module")
def db_session(db_engine): ...
```

### Test variables

```python
def test_create_user_returns_correct_data(user_service: UserService) -> None:
    # ✅ expected / actual pattern
    expected_name = "Alice Smith"
    dto = CreateUserDto(first_name="Alice", last_name="Smith", email="alice@example.com")

    actual_user = user_service.create_user(dto)

    assert actual_user.name == expected_name
    assert actual_user.is_active is True


# ✅ Mock prefixes
mock_repo = MagicMock(spec=UserRepository)
mock_emailer = MagicMock(spec=EmailService)
stub_config = SimpleNamespace(timeout=30, retries=3)
```

---

## 26. Abbreviations & Acronyms

### Well-known abbreviations — camelCase treatment (all lowercase in snake_case)

```python
# ✅ Good
api_url = "https://api.example.com"
html_content = "<p>Hello</p>"
user_id = 123
http_client = HttpClient()
xml_parser = XmlParser()
json_response = parse_response(data)
db_connection = get_db_connection()

# ❌ Bad
API_URL = "..."       # looks like a module-level constant
HTML_Content = "..."  # inconsistent casing
userID = "..."        # camelCase
```

### Acronyms in PascalCase — capitalize first letter only

```python
# ✅ Good
class HttpClient: ...       # not HTTPClient
class XmlParser: ...        # not XMLParser
class JsonSerializer: ...   # not JSONSerializer
class HtmlSanitizer: ...    # not HTMLSanitizer
class SqlAlchemy: ...       # not SQLAlchemy (exception: brand names)
class ApiGateway: ...       # not APIGateway

# Common exceptions (brand names, widely accepted)
class SQLAlchemy: ...       # brand name — keep as-is
class HTMLParser: ...       # stdlib — keep as-is
```

---

## 27. Naming Anti-patterns

### ❌ Generic / meaningless names

```python
# Bad
data = get_users()
result = process_order(order)
temp = calculate_total()
obj = UserService()
info = get_user_info(user_id)
val = compute(x)

# Good
users = get_users()
processed_order = process_order(order)
order_total = calculate_total()
user_service = UserService()
user_profile = get_user_profile(user_id)
discounted_price = compute_discount(price)
```

### ❌ Misleading names

```python
# Implies list but holds count
users = 42               # should be user_count

# Implies boolean but returns object
is_user = get_user(id)   # should be user

# Name lies about return type
def get_users() -> User: ...       # returns one, name says many
def find_user() -> list[User]: ... # returns many, name says one
```

### ❌ Unnecessary context repetition

```python
# In class UserService — "user" is redundant
class UserService:
    def get_user_by_id(self, id: int) -> User: ...   # ❌ redundant
    def get_by_id(self, id: int) -> User: ...         # ✅ better

    def create_user_account(self) -> User: ...         # ❌
    def create_account(self) -> User: ...              # ✅

# In a user dict
user = {
    "user_name": "Alice",    # ❌ redundant prefix
    "name": "Alice",          # ✅
    "user_email": "a@x.com",  # ❌
    "email": "a@x.com",       # ✅
}
```

### ❌ Shadowing built-ins

```python
# ❌ Bad — shadows built-ins
list = [1, 2, 3]         # shadows list()
id = get_user_id()       # shadows id()
type = "admin"           # shadows type()
filter = lambda x: x     # shadows filter()
input = get_input()      # shadows input()

# ✅ Good
items = [1, 2, 3]
user_id = get_user_id()
user_type = "admin"
my_filter = lambda x: x
user_input = get_input()
```

### ❌ Numeric suffixes

```python
# Bad
user1 = get_user(id1)
user2 = get_user(id2)

# Good
current_user = get_user(current_user_id)
target_user = get_user(target_user_id)
```

### ❌ Negated booleans

```python
# Bad
is_not_active = not user.is_active
if not is_not_active:    # double negative!
    do_something()

# Good
is_active = user.is_active
if is_active:
    do_something()
```

---

## 28. Quick Reference Cheatsheet

| Construct | Convention | Example |
|-----------|-----------|---------|
| Variable | snake_case | `user_count`, `is_loading` |
| Constant | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_URL` |
| Function | snake_case + verb | `get_user_by_id()`, `fetch_orders()` |
| Class | PascalCase + noun | `UserService`, `ShoppingCart` |
| Abstract class | `Abstract`/`Base` + PascalCase | `AbstractRepository`, `BaseController` |
| Protocol | PascalCase + adjective/noun | `Serializable`, `UserRepository` |
| Dataclass | PascalCase | `User`, `CreateUserDto` |
| Dataclass field | snake_case | `first_name`, `created_at` |
| Method | snake_case + verb | `get_user_by_id()`, `is_admin()` |
| Class method | snake_case + verb | `from_dict()`, `create_guest()` |
| Static method | snake_case + verb | `validate_email()` |
| Property | snake_case noun | `full_name`, `area`, `is_verified` |
| Protected member | `_` + snake_case | `_cache`, `_validate_data()` |
| Private member | `__` + snake_case | `__balance`, `__validate()` |
| Parameter | snake_case | `user_id`, `start_date` |
| Variadic param | snake_case plural | `*messages`, `**options` |
| Module | short lowercase (snake) | `user_service`, `http_client` |
| Package | short lowercase | `auth`, `users`, `core` |
| File (source) | snake_case.py | `user_service.py` |
| TypeVar | T, U / PascalCase | `T`, `TEntity`, `TId` |
| TypeAlias | PascalCase | `UserId`, `JsonDict` |
| Boolean | `is_/has_/can_/should_` | `is_active`, `has_errors` |
| Exception | PascalCase + `Error` | `UserNotFoundError` |
| Enum | PascalCase | `UserRole`, `HttpStatus` |
| Enum member | SCREAMING_SNAKE_CASE | `UserRole.ADMIN`, `Direction.UP` |
| Decorator fn | snake_case | `@login_required`, `@retry` |
| Decorator cls | PascalCase | `@Singleton`, `@Memoize` |
| Dunder | `__lowercase__` | `__init__`, `__str__`, `__all__` |
| Django model | singular PascalCase | `User`, `BlogPost` |
| Django view cls | PascalCase + `View` | `UserListView` |
| Django view fn | snake_case | `user_list()`, `user_detail()` |
| Django URL name | snake_case | `user_list`, `user_detail` |
| DRF serializer | PascalCase + `Serializer` | `UserSerializer` |
| Pydantic model | PascalCase | `UserResponse`, `CreateUserRequest` |
| FastAPI endpoint | snake_case + verb | `get_users()`, `create_user()` |
| FastAPI dependency | snake_case | `get_db()`, `get_current_user()` |
| Test file | `test_` + snake_case | `test_user_service.py` |
| Test function | `test_` + snake_case behavior | `test_returns_user_when_found()` |
| Test class | `Test` + PascalCase | `TestUserService` |
| Pytest fixture | snake_case noun | `user`, `admin_user`, `mock_repo` |
| Module constant | `__` + lowercase + `__` | `__version__`, `__all__` |
| Throwaway var | `_` | `for _ in range(10)` |

---

## 29. References & Further Reading

| Resource | URL |
|----------|-----|
| **PEP 8 — Style Guide for Python Code** | https://peps.python.org/pep-0008/ |
| **PEP 257 — Docstring Conventions** | https://peps.python.org/pep-0257/ |
| **PEP 526 — Variable Annotations** | https://peps.python.org/pep-0526/ |
| **PEP 544 — Protocols** | https://peps.python.org/pep-0544/ |
| **PEP 613 — TypeAlias** | https://peps.python.org/pep-0613/ |
| **PEP 695 — Type Parameter Syntax (3.12+)** | https://peps.python.org/pep-0695/ |
| **Google Python Style Guide** | https://google.github.io/styleguide/pyguide.html |
| **Python Typing Docs** | https://docs.python.org/3/library/typing.html |
| **mypy** | https://mypy.readthedocs.io |
| **Pyright** | https://github.com/microsoft/pyright |
| **Ruff (linter + formatter)** | https://docs.astral.sh/ruff/ |
| **Black (formatter)** | https://black.readthedocs.io |
| **isort** | https://pycqa.github.io/isort/ |
| **Pylint** | https://pylint.readthedocs.io |
| **Django Coding Style** | https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/ |
| **FastAPI Docs** | https://fastapi.tiangolo.com |
| **Pydantic Docs** | https://docs.pydantic.dev |
| **Clean Code Python** | https://github.com/zedr/clean-code-python |

### Recommended tool config

```toml
# pyproject.toml

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "N", "UP", "B", "SIM", "I"]
# N = pep8-naming — enforces all naming rules automatically

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.isort]
profile = "black"
```

```ini
# .pylintrc
[BASIC]
# snake_case for functions, variables, arguments
function-naming-style = snake_case
variable-naming-style = snake_case
argument-naming-style = snake_case
attr-naming-style = snake_case
method-naming-style = snake_case

# PascalCase for classes
class-naming-style = PascalCase

# UPPER_CASE for constants
const-naming-style = UPPER_CASE

# Short names allowlist
good-names = i,j,k,x,y,z,id,_,T,U,V
```

---

*Last updated: 2026 — Based on Python 3.12, PEP 8, Django 5.x, FastAPI 0.115+*
