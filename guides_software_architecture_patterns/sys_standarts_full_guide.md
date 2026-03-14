# ASGUARD01 — SYSTEM STANDARDS: FULL ARCHITECT'S GUIDE
**Version 3.0 · God-Tier Edition**
*(C) Copyright 1985–2026 Asguard01 Corp.*

> *"Any fool can write code that a computer can understand.*
> *Good programmers write code that humans can understand."*
> — Martin Fowler

---

## TABLE OF CONTENTS

1. [Code Integrity — The Foundation](#1-code-integrity--the-foundation)
2. [Naming Conventions & Readability](#2-naming-conventions--readability)
3. [SOLID Principles](#3-solid-principles)
4. [Clean Architecture & Layered Topology](#4-clean-architecture--layered-topology)
5. [Hexagonal Architecture (Ports & Adapters)](#5-hexagonal-architecture-ports--adapters)
6. [GoF Design Patterns — Creational](#6-gof-design-patterns--creational)
7. [GoF Design Patterns — Structural](#7-gof-design-patterns--structural)
8. [GoF Design Patterns — Behavioral](#8-gof-design-patterns--behavioral)
9. [Enterprise & Architectural Patterns](#9-enterprise--architectural-patterns)
10. [Distributed Systems Patterns](#10-distributed-systems-patterns)
11. [CQRS & Event Sourcing](#11-cqrs--event-sourcing)
12. [Microservices Architecture](#12-microservices-architecture)
13. [Event-Driven Architecture (EDA)](#13-event-driven-architecture-eda)
14. [API Design Standards](#14-api-design-standards)
15. [Data Modeling & Persistence](#15-data-modeling--persistence)
16. [Resilience & Fault Tolerance](#16-resilience--fault-tolerance)
17. [Security Standards](#17-security-standards)
18. [Observability: Logs, Metrics, Traces](#18-observability-logs-metrics-traces)
19. [Testing Strategy](#19-testing-strategy)
20. [Performance Engineering](#20-performance-engineering)
21. [CI/CD & DevOps Pipeline](#21-cicd--devops-pipeline)
22. [Infrastructure as Code (IaC)](#22-infrastructure-as-code-iac)
23. [Domain-Driven Design (DDD)](#23-domain-driven-design-ddd)
24. [Concurrency & Async Patterns](#24-concurrency--async-patterns)
25. [Documentation Standards](#25-documentation-standards)
26. [Team Process & Code Culture](#26-team-process--code-culture)
27. [Anti-Patterns — What to Avoid](#27-anti-patterns--what-to-avoid)
28. [Checklists — Pre-Deploy & Architecture Review](#28-checklists--pre-deploy--architecture-review)

---

## 1. Code Integrity — The Foundation

These are not suggestions. These are laws.

### [DRY] — Don't Repeat Yourself

Every piece of knowledge must have a **single, unambiguous, authoritative representation** within a system.

**BAD:**
```python
# User registration
user_age = int(input_data["age"])
if user_age < 0 or user_age > 150:
    raise ValueError("Invalid age")

# Profile update
user_age = int(profile_data["age"])
if user_age < 0 or user_age > 150:
    raise ValueError("Invalid age")
```

**GOOD:**
```python
def validate_age(age: int) -> int:
    """Validates human age range. Single source of truth."""
    if not (0 <= age <= 150):
        raise InvalidAgeError(f"Age {age} is outside acceptable range [0, 150]")
    return age

# Registration
validate_age(int(input_data["age"]))

# Profile update
validate_age(int(profile_data["age"]))
```

> DRY violation is not just duplication of *text* — it's duplication of *intent* and *logic*. If you change one place and have to hunt for another, you have a DRY violation.

---

### [KISS] — Keep It Simple, Stupid

Complexity is the enemy. **Solve the problem in front of you**, not the imaginary one.

**Complexity metrics to monitor:**
- Cyclomatic complexity per function: **max 10**
- Function length: **max 40 lines**
- Nesting depth: **max 3 levels**
- Number of parameters: **max 4** (use parameter objects beyond that)

**BAD:**
```python
def process(data, mode, flag1, flag2, flag3, extra=None, callback=None):
    if mode == 1:
        if flag1:
            if flag2 and not flag3:
                ...
```

**GOOD:**
```python
@dataclass
class ProcessConfig:
    mode: ProcessingMode
    options: ProcessingOptions

def process(data: RawData, config: ProcessConfig) -> ProcessedData:
    strategy = ProcessingStrategyFactory.create(config.mode)
    return strategy.execute(data, config.options)
```

---

### [YAGNI] — You Aren't Gonna Need It

Do not build features based on speculation. **Every line of code is a liability.** Unused code is technical debt without ROI.

Rules:
- No `// TODO: implement later` without a ticket
- No "future-proof" abstractions without a concrete use case
- No configurable behavior that will only ever have one value
- No generic frameworks for a problem that has only one client

---

### [UNIT] — Single Responsibility at Function Level

A function that does one thing is:
- Easier to name
- Easier to test
- Easier to reuse
- Easier to debug

**Signal that a function violates UNIT:** if its name contains "and", "or", "also", "then" — split it.

---

### [INFO] — Comments Justify *Why*, Not *What*

```python
# BAD: explains WHAT (the code already shows that)
# increment counter by 1
counter += 1

# GOOD: explains WHY
# Skip zero index: protocol header occupies slot 0, data starts at 1
for i in range(1, len(packets)):
    ...

# GOOD: explains a non-obvious business rule
# Grace period of 3 days is defined in contract §4.2
if days_overdue <= 3:
    apply_soft_warning(account)
```

---

## 2. Naming Conventions & Readability

Names are the primary interface between the programmer and the reader.

### Universal Rules

| Entity | Convention | Example |
|--------|-----------|---------|
| Variable | noun, descriptive | `user_invoice_count` |
| Boolean | is/has/can/should prefix | `is_active`, `has_permission` |
| Function | verb + noun | `calculate_tax()`, `fetch_user()` |
| Class | PascalCase noun | `InvoiceRepository` |
| Constant | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Interface | IEntity or EntityInterface | `IPaymentGateway` |
| Abstract | Abstract prefix or -Base suffix | `AbstractProcessor` |
| Enum | PascalCase, values UPPER | `OrderStatus.PENDING` |

### Naming Anti-Patterns

```python
# FORBIDDEN — meaningless names
def do_stuff(d, x, temp, data2):
    ...

# FORBIDDEN — misleading names
def get_user():
    user.delete()  # "get" implies read-only!

# FORBIDDEN — encoding type in name (Hungarian notation)
strUserName = "John"  # type is in the type hint, not the name
intCount = 5

# CORRECT
def deactivate_expired_subscriptions(cutoff_date: date) -> int:
    ...
```

### Ubiquitous Language

All names in code, database, API, and documentation must use the **same domain vocabulary**. If the business says "Invoice", the code says `Invoice` — not `Bill`, not `Receipt`, not `Document`.

This connects directly to [Domain-Driven Design](#23-domain-driven-design-ddd).

---

## 3. SOLID Principles

### [S] Single Responsibility Principle

A class should have **one, and only one, reason to change**.

**BAD — UserService does too much:**
```python
class UserService:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...    # Email concern
    def generate_pdf_report(self, user): ...  # Reporting concern
    def log_user_activity(self, user): ...    # Logging concern
```

**GOOD — Each class owns one concern:**
```python
class UserService:
    def create_user(self, data: UserCreateDTO) -> User: ...

class UserNotificationService:
    def send_welcome_email(self, user: User) -> None: ...

class UserReportService:
    def generate_pdf_report(self, user: User) -> PDF: ...
```

---

### [O] Open/Closed Principle

Software entities should be **open for extension, closed for modification**.
New behavior is added by writing *new* code, not changing *existing* code.

**BAD — every new payment type requires modifying core logic:**
```python
def process_payment(payment):
    if payment.type == "credit_card":
        charge_credit_card(payment)
    elif payment.type == "paypal":
        charge_paypal(payment)
    elif payment.type == "crypto":  # Modified again!
        charge_crypto(payment)
```

**GOOD — new types extend via new classes:**
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, payment: Payment) -> PaymentResult: ...

class CreditCardProcessor(PaymentProcessor):
    def process(self, payment: Payment) -> PaymentResult: ...

class PayPalProcessor(PaymentProcessor):
    def process(self, payment: Payment) -> PaymentResult: ...

# Adding crypto = new class, zero changes to existing code
class CryptoProcessor(PaymentProcessor):
    def process(self, payment: Payment) -> PaymentResult: ...
```

---

### [L] Liskov Substitution Principle

If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` **without altering the correctness of the program**.

**Test:** can you use the subclass wherever the parent class is used, without breaking anything?

**BAD:**
```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        self.height = w  # Violates LSP — unexpected side effect!
```

**GOOD:** Use a common `Shape` abstraction instead of inheritance:
```python
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape):
    def __init__(self, width: float, height: float): ...
    def area(self) -> float: return self.width * self.height

class Square(Shape):
    def __init__(self, side: float): ...
    def area(self) -> float: return self.side ** 2
```

---

### [I] Interface Segregation Principle

**No client should be forced to depend on methods it does not use.**
Prefer many small, specific interfaces over one large general-purpose one.

**BAD — fat interface:**
```python
class IWorker(ABC):
    @abstractmethod def work(self): ...
    @abstractmethod def eat(self): ...  # Robots don't eat!
    @abstractmethod def sleep(self): ...
```

**GOOD — granular interfaces:**
```python
class IWorkable(ABC):
    @abstractmethod def work(self): ...

class IFeedable(ABC):
    @abstractmethod def eat(self): ...

class HumanWorker(IWorkable, IFeedable):
    def work(self): ...
    def eat(self): ...

class RobotWorker(IWorkable):
    def work(self): ...
```

---

### [D] Dependency Inversion Principle

- High-level modules must not depend on low-level modules. **Both should depend on abstractions.**
- Abstractions must not depend on details. **Details depend on abstractions.**

**BAD:**
```python
class OrderService:
    def __init__(self):
        self.db = PostgreSQLDatabase()      # Hard dependency on concrete impl
        self.mailer = SendGridMailer()      # Hard dependency on 3rd party
```

**GOOD:**
```python
class OrderService:
    def __init__(
        self,
        order_repo: IOrderRepository,       # Abstract
        notification_service: INotifier,    # Abstract
    ):
        self._repo = order_repo
        self._notifier = notification_service
```

> This makes testing trivial — inject mocks. It makes deployment flexible — swap PostgreSQL for MongoDB by writing a new adapter.

---

## 4. Clean Architecture & Layered Topology

Clean Architecture (Robert C. Martin) organizes code into concentric layers. **The Dependency Rule: source code dependencies can only point inward.**

```
┌─────────────────────────────────────────────────────────┐
│                   FRAMEWORKS & DRIVERS                   │
│         (Web, DB, UI, External APIs, CLI)                │
│   ┌───────────────────────────────────────────────┐     │
│   │            INTERFACE ADAPTERS                  │     │
│   │   (Controllers, Presenters, Gateways, DTOs)   │     │
│   │   ┌─────────────────────────────────────┐     │     │
│   │   │         APPLICATION LAYER            │     │     │
│   │   │  (Use Cases / Application Services) │     │     │
│   │   │   ┌─────────────────────────┐        │     │     │
│   │   │   │     DOMAIN / ENTITIES   │        │     │     │
│   │   │   │  (Business Rules, Core) │        │     │     │
│   │   │   └─────────────────────────┘        │     │     │
│   │   └─────────────────────────────────────┘     │     │
│   └───────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
                    Dependencies →  INWARD
```

### Layer Responsibilities

| Layer | What Lives Here | What It Must NOT Know |
|-------|----------------|----------------------|
| **Domain/Entities** | Business rules, domain models, value objects, domain events | Frameworks, DB, HTTP, anything external |
| **Application** | Use cases, application services, command/query handlers | Frameworks, DB drivers, HTTP |
| **Interface Adapters** | REST controllers, GraphQL resolvers, CLI handlers, DTO mappers | Business rules logic |
| **Frameworks & Drivers** | Django/FastAPI setup, ORM config, message brokers, email clients | Business rules |

### The Rule in Practice

```
domain/
│   entities/
│       order.py          ← Pure Python, zero imports from outer layers
│       user.py
│   value_objects/
│       money.py
│       email.py
│   repositories/         ← Interfaces (abstract), not implementations
│       i_order_repo.py
│
application/
│   use_cases/
│       place_order.py    ← Orchestrates domain, calls repo interface
│       cancel_order.py
│   dtos/
│       order_dto.py
│
infrastructure/           ← Implements domain interfaces
│   persistence/
│       postgres_order_repo.py
│   messaging/
│       kafka_event_bus.py
│
interfaces/
│   http/
│       order_controller.py
│   cli/
│       admin_commands.py
```

### DTO (Data Transfer Object) Rule

Cross-boundary communication uses **DTOs only** — plain data structures with no behavior. Never pass domain entities across boundaries.

```python
# DTO — just data, no logic
@dataclass(frozen=True)
class PlaceOrderDTO:
    user_id: UUID
    items: list[OrderItemDTO]
    shipping_address: AddressDTO

# Use Case receives DTO, returns DTO
class PlaceOrderUseCase:
    def execute(self, dto: PlaceOrderDTO) -> OrderConfirmationDTO:
        order = Order.create(dto)            # Domain logic
        self._repo.save(order)
        self._events.publish(OrderPlacedEvent(order.id))
        return OrderConfirmationDTO.from_order(order)
```

---

## 5. Hexagonal Architecture (Ports & Adapters)

Proposed by Alistair Cockburn. Treats the application as a **hexagon** with "ports" (interfaces) and "adapters" (implementations).

```
               ┌──────────────┐
  HTTP API ───▶│   REST       │
               │  Adapter     │
               └──────┬───────┘
                       │ (primary/driving port)
         ┌─────────────▼──────────────┐
         │                            │
REST ──▶ │    APPLICATION CORE        │ ──▶ DB Adapter ──▶ PostgreSQL
gRPC ──▶ │                            │ ──▶ Email Adapter ──▶ SendGrid
CLI  ──▶ │  Business Logic lives here │ ──▶ Queue Adapter ──▶ RabbitMQ
         │                            │
         └────────────────────────────┘
                (secondary/driven ports)
```

**Primary Ports** (driving): How external actors call the app (HTTP, gRPC, CLI)
**Secondary Ports** (driven): How the app calls external systems (DB, email, queues)

**Benefit:** The core can be tested completely in isolation from all infrastructure.

```python
# PORT (interface defined in core)
class IPaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: Money, token: str) -> ChargeResult: ...

# ADAPTER (infrastructure, implements the port)
class StripePaymentAdapter(IPaymentGateway):
    def charge(self, amount: Money, token: str) -> ChargeResult:
        response = stripe.PaymentIntent.create(
            amount=amount.in_cents(),
            currency=amount.currency.lower(),
            payment_method=token,
        )
        return ChargeResult.from_stripe(response)

# FAKE ADAPTER for tests
class FakePaymentAdapter(IPaymentGateway):
    def charge(self, amount: Money, token: str) -> ChargeResult:
        return ChargeResult(success=True, transaction_id="fake-txn-001")
```

---

## 6. GoF Design Patterns — Creational

The 23 Gang of Four patterns, organized by category. These are proven solutions to recurring problems.

### Factory Method

Define an interface for creating an object, but let subclasses decide which class to instantiate.

```python
class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[EMAIL] {message}")

class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"[SMS] {message}")

class NotificationFactory:
    _registry: dict[str, type[Notification]] = {}

    @classmethod
    def register(cls, channel: str, notification_class: type[Notification]):
        cls._registry[channel] = notification_class

    @classmethod
    def create(cls, channel: str) -> Notification:
        if channel not in cls._registry:
            raise UnsupportedChannelError(channel)
        return cls._registry[channel]()

# Registration
NotificationFactory.register("email", EmailNotification)
NotificationFactory.register("sms", SMSNotification)

# Usage — zero coupling to concrete classes
notifier = NotificationFactory.create("email")
notifier.send("Your order is ready")
```

---

### Abstract Factory

Create families of related objects without specifying their concrete classes.

```python
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...
    @abstractmethod
    def create_dialog(self) -> Dialog: ...

class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button: return WindowsButton()
    def create_dialog(self) -> Dialog: return WindowsDialog()

class MacOSUIFactory(UIFactory):
    def create_button(self) -> Button: return MacButton()
    def create_dialog(self) -> Dialog: return MacDialog()

def render_application(factory: UIFactory):
    button = factory.create_button()
    dialog = factory.create_dialog()
    button.render()
    dialog.render()
```

---

### Builder

Construct complex objects step by step.

```python
@dataclass
class QueryConfig:
    table: str
    conditions: list[str]
    order_by: str | None
    limit: int | None
    joins: list[str]

class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._conditions: list[str] = []
        self._order_by: str | None = None
        self._limit: int | None = None
        self._joins: list[str] = []

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self  # Fluent interface

    def order_by(self, column: str) -> "QueryBuilder":
        self._order_by = column
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def join(self, join_clause: str) -> "QueryBuilder":
        self._joins.append(join_clause)
        return self

    def build(self) -> QueryConfig:
        return QueryConfig(
            table=self._table,
            conditions=self._conditions,
            order_by=self._order_by,
            limit=self._limit,
            joins=self._joins,
        )

# Fluent builder usage
query = (
    QueryBuilder("orders")
    .join("LEFT JOIN users ON orders.user_id = users.id")
    .where("orders.status = 'pending'")
    .where("orders.created_at > '2024-01-01'")
    .order_by("orders.created_at DESC")
    .limit(100)
    .build()
)
```

---

### Singleton

Ensure a class has only one instance. **Use sparingly** — often a sign of global state.

```python
class ApplicationConfig:
    _instance: "ApplicationConfig | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "ApplicationConfig":
        if cls._instance is None:
            with cls._lock:  # Thread-safe double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._load()
        return cls._instance

    def _load(self) -> None:
        self._data = load_from_env()

    def get(self, key: str) -> str:
        return self._data[key]
```

> **Warning:** Singleton is often an anti-pattern. Prefer dependency injection with a single instance managed by a DI container.

---

### Prototype

Clone objects instead of constructing from scratch.

```python
import copy

class DocumentTemplate:
    def __init__(self, title: str, sections: list[str]):
        self.title = title
        self.sections = sections
        self.metadata = {"created_at": datetime.now()}

    def clone(self) -> "DocumentTemplate":
        return copy.deepcopy(self)

# Base template created once
invoice_template = DocumentTemplate(
    title="Invoice",
    sections=["header", "items", "totals", "footer"]
)

# Each invoice is a clone, independently modifiable
new_invoice = invoice_template.clone()
new_invoice.title = f"Invoice #{next_id()}"
```

---

## 7. GoF Design Patterns — Structural

### Adapter

Convert the interface of a class into another interface that clients expect.

```python
# Target interface our system expects
class ITemperatureSensor(ABC):
    @abstractmethod
    def get_celsius(self) -> float: ...

# Legacy 3rd-party sensor (returns Fahrenheit, different method name)
class LegacyFahrenheitSensor:
    def read_temperature(self) -> float:
        return 98.6  # Fahrenheit

# Adapter bridges the gap
class FahrenheitSensorAdapter(ITemperatureSensor):
    def __init__(self, sensor: LegacyFahrenheitSensor):
        self._sensor = sensor

    def get_celsius(self) -> float:
        fahrenheit = self._sensor.read_temperature()
        return (fahrenheit - 32) * 5 / 9
```

---

### Decorator

Attach additional responsibilities to an object dynamically.

```python
class IDataFetcher(ABC):
    @abstractmethod
    def fetch(self, url: str) -> str: ...

class HttpDataFetcher(IDataFetcher):
    def fetch(self, url: str) -> str:
        return requests.get(url).text

# Decorator: adds caching without touching HttpDataFetcher
class CachingDecorator(IDataFetcher):
    def __init__(self, fetcher: IDataFetcher, cache: ICache):
        self._fetcher = fetcher
        self._cache = cache

    def fetch(self, url: str) -> str:
        if cached := self._cache.get(url):
            return cached
        result = self._fetcher.fetch(url)
        self._cache.set(url, result, ttl=300)
        return result

# Decorator: adds logging
class LoggingDecorator(IDataFetcher):
    def __init__(self, fetcher: IDataFetcher, logger: ILogger):
        self._fetcher = fetcher
        self._logger = logger

    def fetch(self, url: str) -> str:
        self._logger.info(f"Fetching: {url}")
        result = self._fetcher.fetch(url)
        self._logger.info(f"Fetched {len(result)} bytes")
        return result

# Stack decorators — composition over inheritance
fetcher = LoggingDecorator(
    CachingDecorator(
        HttpDataFetcher(),
        RedisCache()
    ),
    StructuredLogger()
)
```

---

### Composite

Compose objects into tree structures to represent part-whole hierarchies.

```python
class FileSystemItem(ABC):
    @abstractmethod
    def size(self) -> int: ...
    @abstractmethod
    def name(self) -> str: ...

class File(FileSystemItem):
    def __init__(self, name: str, size_bytes: int):
        self._name = name
        self._size = size_bytes

    def size(self) -> int: return self._size
    def name(self) -> str: return self._name

class Directory(FileSystemItem):
    def __init__(self, name: str):
        self._name = name
        self._children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def size(self) -> int:
        return sum(child.size() for child in self._children)

    def name(self) -> str: return self._name

# Client treats files and directories uniformly
root = Directory("root")
root.add(File("readme.md", 1024))
docs = Directory("docs")
docs.add(File("guide.pdf", 2048000))
root.add(docs)

print(root.size())  # Works recursively across entire tree
```

---

### Facade

Provide a simplified interface to a complex subsystem.

```python
# Complex subsystem
class VideoEncoder: ...
class AudioEncoder: ...
class MetadataExtractor: ...
class ThumbnailGenerator: ...
class StorageUploader: ...

# Facade — single simple interface
class VideoProcessingFacade:
    def __init__(self):
        self._video_encoder = VideoEncoder()
        self._audio_encoder = AudioEncoder()
        self._metadata = MetadataExtractor()
        self._thumbnails = ThumbnailGenerator()
        self._uploader = StorageUploader()

    def process_and_upload(self, video_path: str) -> str:
        """Single method hides the entire pipeline."""
        video = self._video_encoder.encode(video_path)
        audio = self._audio_encoder.extract_and_encode(video_path)
        meta = self._metadata.extract(video_path)
        thumb = self._thumbnails.generate(video_path)
        return self._uploader.upload(video, audio, meta, thumb)
```

---

### Proxy

Provide a surrogate or placeholder for another object to control access.

```python
class IExpensiveService(ABC):
    @abstractmethod
    def compute(self, data: str) -> str: ...

class ExpensiveService(IExpensiveService):
    def compute(self, data: str) -> str:
        time.sleep(5)  # Expensive!
        return data.upper()

class LazyLoadingProxy(IExpensiveService):
    """Service is only created on first use."""
    def __init__(self):
        self._service: ExpensiveService | None = None

    def compute(self, data: str) -> str:
        if self._service is None:
            self._service = ExpensiveService()
        return self._service.compute(data)
```

---

### Bridge

Decouple an abstraction from its implementation so the two can vary independently.

```python
# Implementation hierarchy
class IRenderer(ABC):
    @abstractmethod
    def render_shape(self, shape_data: dict) -> None: ...

class OpenGLRenderer(IRenderer): ...
class VulkanRenderer(IRenderer): ...

# Abstraction hierarchy — uses IRenderer, doesn't care which
class Shape(ABC):
    def __init__(self, renderer: IRenderer):
        self._renderer = renderer

    @abstractmethod
    def draw(self) -> None: ...

class Circle(Shape):
    def __init__(self, radius: float, renderer: IRenderer):
        super().__init__(renderer)
        self._radius = radius

    def draw(self) -> None:
        self._renderer.render_shape({"type": "circle", "radius": self._radius})
```

---

### Flyweight

Use sharing to efficiently support a large number of fine-grained objects.

```python
class CharacterStyle:
    """Shared flyweight — intrinsic state."""
    def __init__(self, font: str, size: int, color: str):
        self.font = font
        self.size = size
        self.color = color

class StyleFactory:
    _styles: dict[tuple, CharacterStyle] = {}

    @classmethod
    def get_style(cls, font: str, size: int, color: str) -> CharacterStyle:
        key = (font, size, color)
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, color)
        return cls._styles[key]

# A document with 1M characters shares only a handful of style objects
```

---

## 8. GoF Design Patterns — Behavioral

### Strategy

Define a family of algorithms, encapsulate each one, and make them interchangeable.

```python
class ISortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class QuickSort(ISortStrategy):
    def sort(self, data: list) -> list: ...

class MergeSort(ISortStrategy):
    def sort(self, data: list) -> list: ...

class TimSort(ISortStrategy):
    def sort(self, data: list) -> list: ...

class DataProcessor:
    def __init__(self, strategy: ISortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ISortStrategy) -> None:
        self._strategy = strategy  # Swap at runtime

    def process(self, data: list) -> list:
        return self._strategy.sort(data)
```

---

### Observer (Pub/Sub)

Define a one-to-many dependency between objects. When one object changes state, all dependents are notified automatically.

```python
from typing import Callable

class EventBus:
    """In-process event bus."""
    _subscribers: dict[str, list[Callable]] = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type: str, handler: Callable) -> None:
        cls._subscribers[event_type].append(handler)

    @classmethod
    def publish(cls, event_type: str, event: object) -> None:
        for handler in cls._subscribers.get(event_type, []):
            handler(event)

# Domain event
@dataclass
class OrderPlacedEvent:
    order_id: UUID
    user_id: UUID
    total: Money
    occurred_at: datetime = field(default_factory=datetime.now)

# Subscribers — completely decoupled from order creation
def send_confirmation_email(event: OrderPlacedEvent): ...
def update_inventory(event: OrderPlacedEvent): ...
def notify_warehouse(event: OrderPlacedEvent): ...

EventBus.subscribe("order.placed", send_confirmation_email)
EventBus.subscribe("order.placed", update_inventory)
EventBus.subscribe("order.placed", notify_warehouse)

# Publisher — knows nothing about subscribers
EventBus.publish("order.placed", OrderPlacedEvent(order_id=..., user_id=...))
```

---

### Command

Encapsulate a request as an object, allowing parameterization, queuing, logging, and undo.

```python
class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

class TransferMoneyCommand(ICommand):
    def __init__(self, from_account: Account, to_account: Account, amount: Money):
        self._from = from_account
        self._to = to_account
        self._amount = amount
        self._executed = False

    def execute(self) -> None:
        self._from.debit(self._amount)
        self._to.credit(self._amount)
        self._executed = True

    def undo(self) -> None:
        if not self._executed:
            raise CommandNotExecutedError()
        self._to.debit(self._amount)
        self._from.credit(self._amount)
        self._executed = False

class CommandHistory:
    def __init__(self):
        self._history: list[ICommand] = []

    def execute(self, command: ICommand) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            self._history.pop().undo()
```

---

### Chain of Responsibility

Pass a request along a chain of handlers. Each handler decides to process or pass it on.

```python
class RequestHandler(ABC):
    def __init__(self):
        self._next: RequestHandler | None = None

    def set_next(self, handler: "RequestHandler") -> "RequestHandler":
        self._next = handler
        return handler  # Fluent chaining

    def handle(self, request: Request) -> Response | None:
        if self._next:
            return self._next.handle(request)
        return None

class AuthenticationHandler(RequestHandler):
    def handle(self, request: Request) -> Response | None:
        if not request.has_valid_token():
            return Response(status=401, body="Unauthorized")
        return super().handle(request)

class RateLimitHandler(RequestHandler):
    def handle(self, request: Request) -> Response | None:
        if self._is_rate_limited(request.client_ip):
            return Response(status=429, body="Too Many Requests")
        return super().handle(request)

class BusinessLogicHandler(RequestHandler):
    def handle(self, request: Request) -> Response | None:
        return process_business_logic(request)

# Build the chain
auth = AuthenticationHandler()
auth.set_next(RateLimitHandler()).set_next(BusinessLogicHandler())

response = auth.handle(incoming_request)
```

---

### Template Method

Define the skeleton of an algorithm, deferring some steps to subclasses.

```python
class ReportGenerator(ABC):
    def generate(self) -> str:
        """Template method — defines the algorithm skeleton."""
        data = self.fetch_data()
        processed = self.process_data(data)
        formatted = self.format_output(processed)
        return self.render(formatted)

    @abstractmethod
    def fetch_data(self) -> RawData: ...

    @abstractmethod
    def process_data(self, data: RawData) -> ProcessedData: ...

    def format_output(self, data: ProcessedData) -> FormattedData:
        """Default implementation — can be overridden."""
        return DefaultFormatter().format(data)

    @abstractmethod
    def render(self, data: FormattedData) -> str: ...

class PDFReportGenerator(ReportGenerator):
    def fetch_data(self): return self._db.query_sales()
    def process_data(self, data): return aggregate_by_month(data)
    def render(self, data): return PDFRenderer().render(data)
```

---

### State

Allow an object to alter its behavior when its internal state changes.

```python
class IOrderState(ABC):
    @abstractmethod
    def confirm(self, order: "Order") -> None: ...
    @abstractmethod
    def ship(self, order: "Order") -> None: ...
    @abstractmethod
    def cancel(self, order: "Order") -> None: ...

class PendingState(IOrderState):
    def confirm(self, order: "Order") -> None:
        order.set_state(ConfirmedState())
    def ship(self, order: "Order") -> None:
        raise InvalidTransitionError("Cannot ship unconfirmed order")
    def cancel(self, order: "Order") -> None:
        order.set_state(CancelledState())

class ConfirmedState(IOrderState):
    def confirm(self, order: "Order") -> None:
        raise InvalidTransitionError("Already confirmed")
    def ship(self, order: "Order") -> None:
        order.set_state(ShippedState())
    def cancel(self, order: "Order") -> None:
        order.set_state(CancelledState())

class Order:
    def __init__(self):
        self._state: IOrderState = PendingState()

    def set_state(self, state: IOrderState) -> None:
        self._state = state

    def confirm(self): self._state.confirm(self)
    def ship(self): self._state.ship(self)
    def cancel(self): self._state.cancel(self)
```

---

### Iterator

Provide a way to access elements of a collection sequentially without exposing its internal structure.

### Mediator

Define an object that encapsulates how a set of objects interact, reducing direct coupling.

### Memento

Capture and externalize an object's internal state for later restoration — without violating encapsulation.

### Visitor

Represent an operation to be performed on elements of an object structure. Add new operations without changing element classes.

### Interpreter

Define a grammar for a language and provide an interpreter.

---

## 9. Enterprise & Architectural Patterns

### Repository Pattern

Mediate between the domain and data mapping layers. Provides a collection-like interface for accessing domain objects.

```python
# Interface in domain layer
class IOrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    def find_by_user(self, user_id: UUID, status: OrderStatus | None = None) -> list[Order]: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def delete(self, order_id: UUID) -> None: ...

# Implementation in infrastructure layer
class PostgresOrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, order_id: UUID) -> Order | None:
        record = self._session.query(OrderRecord).filter_by(id=order_id).first()
        return OrderMapper.to_domain(record) if record else None

    def save(self, order: Order) -> None:
        record = OrderMapper.to_record(order)
        self._session.merge(record)
```

---

### Unit of Work

Maintains a list of objects affected by a business transaction and coordinates the writing out of changes.

```python
class UnitOfWork:
    def __init__(self, session: Session):
        self._session = session
        self.orders = PostgresOrderRepository(session)
        self.users = PostgresUserRepository(session)

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()

# Usage — atomic transaction
def transfer_order(from_user_id: UUID, to_user_id: UUID, order_id: UUID):
    with UnitOfWork(get_session()) as uow:
        order = uow.orders.find_by_id(order_id)
        order.transfer_to(to_user_id)
        uow.orders.save(order)
        # Auto-commit on success, auto-rollback on exception
```

---

### Specification Pattern

Encapsulate business rules as composable, reusable specifications.

```python
class ISpecification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, entity: T) -> bool: ...

    def and_(self, other: "ISpecification[T]") -> "AndSpec[T]":
        return AndSpec(self, other)

    def or_(self, other: "ISpecification[T]") -> "OrSpec[T]":
        return OrSpec(self, other)

    def not_(self) -> "NotSpec[T]":
        return NotSpec(self)

class ActiveUserSpec(ISpecification[User]):
    def is_satisfied_by(self, user: User) -> bool:
        return user.is_active

class PremiumUserSpec(ISpecification[User]):
    def is_satisfied_by(self, user: User) -> bool:
        return user.subscription_tier == SubscriptionTier.PREMIUM

# Composition
eligible_for_discount = ActiveUserSpec().and_(PremiumUserSpec())
users = [u for u in all_users if eligible_for_discount.is_satisfied_by(u)]
```

---

### Saga Pattern

Manage distributed transactions across microservices using a sequence of local transactions and compensating actions.

**Choreography-based Saga:**
```
OrderService ──publish──▶ OrderCreated
                                │
                    InventoryService ──▶ StockReserved
                                                │
                                    PaymentService ──▶ PaymentProcessed
                                                               │
                                               ShippingService ──▶ OrderShipped
```

**Orchestration-based Saga:**
```python
class PlaceOrderSaga:
    def __init__(self, services: SagaServices):
        self._services = services

    async def execute(self, order_id: UUID) -> None:
        compensations: list[Coroutine] = []
        try:
            await self._services.inventory.reserve(order_id)
            compensations.append(self._services.inventory.release(order_id))

            await self._services.payment.charge(order_id)
            compensations.append(self._services.payment.refund(order_id))

            await self._services.shipping.schedule(order_id)

        except Exception as e:
            logger.error(f"Saga failed for {order_id}: {e}")
            for compensation in reversed(compensations):
                await compensation  # Rollback in reverse order
            raise SagaFailedError(order_id) from e
```

---

## 10. Distributed Systems Patterns

### Circuit Breaker

Prevent cascading failures by stopping requests to a failing service.

```
CLOSED ──(failure threshold exceeded)──▶ OPEN
   ▲                                        │
   │                              (timeout expires)
   │                                        ▼
   └──(success)──────────────── HALF-OPEN ──(failure)──▶ OPEN
```

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._last_failure_time: float | None = None

    def call(self, func: Callable, *args, **kwargs):
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time > self._recovery_timeout:
                self._state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        self._failures = 0
        self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        self._failures += 1
        self._last_failure_time = time.time()
        if self._failures >= self._threshold:
            self._state = CircuitState.OPEN
            logger.warning(f"Circuit breaker OPENED after {self._failures} failures")
```

---

### Retry with Exponential Backoff

```python
def retry_with_backoff(
    func: Callable,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
) -> Any:
    for attempt in range(max_attempts):
        try:
            return func()
        except TransientError as e:
            if attempt == max_attempts - 1:
                raise

            delay = min(base_delay * (2 ** attempt), max_delay)
            if jitter:
                delay *= (0.5 + random.random() * 0.5)  # Add randomness to prevent thundering herd

            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
            time.sleep(delay)
```

---

### Bulkhead

Isolate failures in one part of the system from cascading to others.

```python
class BulkheadExecutor:
    """Thread pool per service — one service exhaustion can't affect others."""
    def __init__(self, max_workers: int):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._semaphore = threading.Semaphore(max_workers)

    def submit(self, func: Callable, *args, timeout: float = 30.0) -> Future:
        if not self._semaphore.acquire(timeout=timeout):
            raise BulkheadFullError("Bulkhead capacity exhausted")
        try:
            future = self._executor.submit(func, *args)
            future.add_done_callback(lambda _: self._semaphore.release())
            return future
        except Exception:
            self._semaphore.release()
            raise

# Each downstream dependency gets its own pool
payment_pool = BulkheadExecutor(max_workers=20)
inventory_pool = BulkheadExecutor(max_workers=10)
email_pool = BulkheadExecutor(max_workers=5)
```

---

### Outbox Pattern

Ensure reliable event publishing alongside database writes.

```sql
-- Transactional outbox table
CREATE TABLE outbox_messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type  VARCHAR(255) NOT NULL,
    payload     JSONB NOT NULL,
    status      VARCHAR(50) DEFAULT 'pending',
    created_at  TIMESTAMPTZ DEFAULT now(),
    processed_at TIMESTAMPTZ
);
```

```python
def place_order(order_data: PlaceOrderDTO) -> Order:
    with transaction():
        order = Order.create(order_data)
        db.save(order)

        # Written in the SAME transaction as the business data
        db.insert_outbox(OutboxMessage(
            event_type="order.placed",
            payload=OrderPlacedEvent.from_order(order).to_dict()
        ))
        # Commit is atomic — either both succeed or both fail

# Separate relay process polls outbox and publishes to message broker
async def outbox_relay():
    while True:
        messages = db.fetch_pending_outbox(limit=100)
        for msg in messages:
            await message_broker.publish(msg.event_type, msg.payload)
            db.mark_outbox_processed(msg.id)
        await asyncio.sleep(1)
```

---

### Idempotency Keys

```python
class IdempotentCommandHandler:
    def __init__(self, handler: ICommandHandler, idempotency_store: IIdempotencyStore):
        self._handler = handler
        self._store = idempotency_store

    def handle(self, command: Command, idempotency_key: str) -> CommandResult:
        # Check if we've seen this key before
        if existing := self._store.get(idempotency_key):
            return existing  # Return cached result, don't process again

        result = self._handler.handle(command)
        self._store.set(idempotency_key, result, ttl=86400)  # Store for 24h
        return result
```

---

## 11. CQRS & Event Sourcing

### CQRS — Command Query Responsibility Segregation

Separate the **read model** from the **write model**. Different databases optimized for different workloads.

```
                     ┌─────────────────┐
Write Side:          │   Command Bus   │
Commands ──────────▶ │                 │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐       ┌──────────────┐
                     │ Command Handler │──────▶ │  Write DB    │
                     └────────┬────────┘       │  (PostgreSQL)│
                              │                └──────┬───────┘
                     Domain Event Published           │
                              │                       │
                     ┌────────▼────────┐    ┌─────────▼────────┐
                     │  Event Handler  │───▶ │  Read DB         │
                     └─────────────────┘    │  (Elasticsearch) │
                                             └──────────────────┘
Read Side:
Queries ───────────────────────────────────▶ Read DB (direct)
```

```python
# COMMAND SIDE
@dataclass(frozen=True)
class CreateProductCommand:
    name: str
    price: Decimal
    category_id: UUID

class CreateProductHandler:
    def handle(self, cmd: CreateProductCommand) -> UUID:
        product = Product.create(name=cmd.name, price=Money(cmd.price))
        self._repo.save(product)
        self._events.publish(ProductCreatedEvent(product_id=product.id, ...))
        return product.id

# QUERY SIDE (uses a denormalized read model — much faster)
class GetProductsByCategoryQuery:
    category_id: UUID
    page: int
    page_size: int

class GetProductsByCategoryHandler:
    def handle(self, query: GetProductsByCategoryQuery) -> ProductListReadModel:
        return self._read_db.query(
            "SELECT * FROM products_read_model WHERE category_id = %s LIMIT %s OFFSET %s",
            [query.category_id, query.page_size, query.page * query.page_size]
        )
```

---

### Event Sourcing

Store **the sequence of events** that led to the current state, not the state itself.

```python
@dataclass
class BankAccount:
    id: UUID
    owner_id: UUID
    balance: Decimal = Decimal("0.00")
    _events: list[DomainEvent] = field(default_factory=list)

    def deposit(self, amount: Money) -> None:
        if amount.value <= 0:
            raise InvalidAmountError()
        self._apply(MoneyDeposited(account_id=self.id, amount=amount))

    def withdraw(self, amount: Money) -> None:
        if amount.value > self.balance:
            raise InsufficientFundsError()
        self._apply(MoneyWithdrawn(account_id=self.id, amount=amount))

    def _apply(self, event: DomainEvent) -> None:
        # Mutate state based on event type
        if isinstance(event, MoneyDeposited):
            self.balance += event.amount.value
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount.value
        self._events.append(event)

    @classmethod
    def reconstruct_from_events(cls, events: list[DomainEvent]) -> "BankAccount":
        account = cls(id=events[0].account_id, owner_id=events[0].owner_id)
        for event in events:
            account._apply(event)
        account._events = []  # Clear, these are already persisted
        return account
```

**Benefits of Event Sourcing:**
- Complete audit trail — every state change is recorded
- Time travel — reconstruct state at any point in history
- Event replay — rebuild projections from scratch
- Debugging power — see exactly what happened and when

---

## 12. Microservices Architecture

### Service Decomposition Principles

- **By Business Capability**: Each service owns a business domain (OrderService, InventoryService, UserService)
- **By Bounded Context (DDD)**: Each service aligns with a bounded context
- **By team ownership**: Conway's Law — system structure mirrors communication structure

### Inter-Service Communication

| Pattern | When to Use | Technology |
|---------|------------|------------|
| **Synchronous REST** | Query operations, request/response needed | HTTP/HTTPS |
| **Synchronous gRPC** | Internal services, performance-critical | gRPC/protobuf |
| **Async Events** | State changes, notifications, decoupled workflows | Kafka, RabbitMQ |
| **Async Commands** | Task delegation, fire-and-forget | SQS, Redis Queue |

### Service Mesh

For large microservice deployments, use a **service mesh** (Istio, Linkerd) for:
- mTLS between services (zero-trust networking)
- Automatic load balancing
- Circuit breaking at infrastructure level
- Distributed tracing injection

### API Gateway

```
Client
  │
  ▼
┌───────────────────────────────────┐
│            API Gateway            │
│  - Authentication                 │
│  - Rate Limiting                  │
│  - Request Routing                │
│  - SSL Termination                │
│  - Response Aggregation           │
│  - Protocol Translation           │
└─┬──────────┬──────────┬───────────┘
  │          │          │
  ▼          ▼          ▼
Order    Inventory   User
Service  Service     Service
```

---

## 13. Event-Driven Architecture (EDA)

### Event Types

| Type | Description | Example |
|------|-------------|---------|
| **Domain Event** | Something happened in the domain | `OrderPlaced`, `PaymentFailed` |
| **Integration Event** | Cross-service notification | `order-service.order.placed` |
| **Command** | Instruction to do something | `ProcessPayment`, `SendEmail` |
| **Query** | Read-only request | `GetOrderById` |

### Event Schema Design

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "order.placed",
  "event_version": "1.0",
  "aggregate_id": "order-123",
  "aggregate_type": "Order",
  "occurred_at": "2026-03-11T10:00:00Z",
  "correlation_id": "req-abc-123",
  "causation_id": "cmd-xyz-456",
  "producer_service": "order-service",
  "payload": {
    "order_id": "order-123",
    "user_id": "user-456",
    "total_amount": 99.99,
    "currency": "USD",
    "items": [...]
  },
  "metadata": {
    "schema_version": "1.0",
    "environment": "production"
  }
}
```

**Schema Evolution Rules:**
1. Never remove fields in a minor version
2. New optional fields = minor version bump
3. Breaking changes = new event type version (`order.placed.v2`)
4. Maintain backward compatibility for at least 2 major versions

---

## 14. API Design Standards

### REST API Standards

**URL Design:**
```
GET    /api/v1/orders              — List orders
POST   /api/v1/orders              — Create order
GET    /api/v1/orders/{id}         — Get order by ID
PUT    /api/v1/orders/{id}         — Full update
PATCH  /api/v1/orders/{id}         — Partial update
DELETE /api/v1/orders/{id}         — Delete order
GET    /api/v1/orders/{id}/items   — Nested resource
POST   /api/v1/orders/{id}/cancel  — Action (verb is OK here)
```

**HTTP Status Code Standards:**

| Code | When to Use |
|------|------------|
| 200 OK | Successful GET, PUT, PATCH |
| 201 Created | Successful POST |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Validation failure |
| 401 Unauthorized | Missing/invalid auth |
| 403 Forbidden | Valid auth, no permission |
| 404 Not Found | Resource doesn't exist |
| 409 Conflict | State conflict (duplicate, version mismatch) |
| 422 Unprocessable Entity | Valid syntax, invalid business rules |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server Error | Unexpected server error |
| 503 Service Unavailable | Maintenance, overload |

**Standardized Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Age must be between 18 and 120"
      }
    ],
    "trace_id": "req-abc-123",
    "timestamp": "2026-03-11T10:00:00Z"
  }
}
```

### API Versioning Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| URL path (`/v1/`) | Explicit, cacheable | URL changes |
| Header (`Api-Version: 1`) | Clean URLs | Less visible |
| Query param (`?version=1`) | Easy to test | Messy URLs |

**Recommendation:** Use URL path versioning. Simple, explicit, easy to route.

### Pagination Standard

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 1500,
    "total_pages": 75,
    "has_next": true,
    "has_prev": false,
    "next_cursor": "eyJpZCI6MTAwfQ=="
  }
}
```

---

## 15. Data Modeling & Persistence

### Value Objects vs Entities vs Aggregates

```python
# VALUE OBJECT — identified by its value, immutable
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money cannot be negative")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise CurrencyMismatchError()
        return Money(self.amount + other.amount, self.currency)

# ENTITY — identified by ID, mutable state
class Order:
    def __init__(self, order_id: UUID, user_id: UUID):
        self.id = order_id
        self.user_id = user_id
        self._items: list[OrderItem] = []
        self._status = OrderStatus.PENDING

# AGGREGATE ROOT — cluster of entities and value objects
class Order:  # Root of the Order aggregate
    def add_item(self, product_id: UUID, qty: int, price: Money) -> None:
        """All mutations go through the aggregate root."""
        item = OrderItem(product_id=product_id, quantity=qty, unit_price=price)
        self._items.append(item)
        self._recalculate_total()

    def place(self) -> list[DomainEvent]:
        """Business logic enforced here, not in the repository."""
        if not self._items:
            raise EmptyOrderError()
        self._status = OrderStatus.CONFIRMED
        return [OrderPlacedEvent(order_id=self.id, total=self.total)]
```

### Database Selection Guide

| Database | Best For | Avoid When |
|----------|---------|------------|
| **PostgreSQL** | Relational data, ACID, complex queries | Massive unstructured writes |
| **MongoDB** | Flexible schema, document hierarchies | Complex joins, ACID transactions |
| **Redis** | Cache, sessions, pub/sub, queues | Large data, complex queries |
| **Elasticsearch** | Full-text search, log aggregation | Primary data store |
| **Cassandra** | Massive write throughput, time-series | Complex queries, ACID |
| **TimescaleDB** | Time-series data, metrics | Non-temporal relational data |
| **Neo4j** | Graph relationships, recommendations | Non-graph data |

### Migration Strategy

```
migrations/
├── 001_create_users.sql
├── 002_create_orders.sql
├── 003_add_order_status_index.sql
└── 004_add_payment_method.sql
```

Rules:
- Migrations are **append-only** — never edit a committed migration
- Each migration is **idempotent** (`CREATE TABLE IF NOT EXISTS`)
- Backwards-compatible migrations (expand/contract pattern):
  1. **Expand**: Add new column (nullable)
  2. **Migrate**: Backfill data
  3. **Contract**: Remove old column (separate deploy)

---

## 16. Resilience & Fault Tolerance

### Atomic I/O (Write-Tmp-Swap)

```python
def atomic_write(file_path: Path, data: bytes) -> None:
    """Write atomically using temp file + rename.
    Rename is atomic on POSIX — no partial writes possible.
    """
    tmp_path = file_path.with_suffix(".tmp")
    try:
        tmp_path.write_bytes(data)
        tmp_path.rename(file_path)  # Atomic on same filesystem
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
```

### Checkpoint & Resume Pattern

```python
@dataclass
class ProcessingState:
    job_id: str
    last_processed_offset: int
    total_items: int
    checksum: str
    status: str

class ResumableProcessor:
    def process(self, job_id: str, items: list) -> ProcessingResult:
        state = self._load_checkpoint(job_id) or ProcessingState(
            job_id=job_id, last_processed_offset=0, total_items=len(items),
            checksum=compute_checksum(items), status="running"
        )

        # Integrity check
        if compute_checksum(items) != state.checksum:
            raise DataIntegrityError("Input data has changed since last checkpoint")

        # Resume from where we left off
        for i, item in enumerate(items[state.last_processed_offset:], start=state.last_processed_offset):
            self._process_item(item)

            # Save checkpoint every N items
            if i % 100 == 0:
                state.last_processed_offset = i + 1
                self._save_checkpoint(state)

        state.status = "completed"
        self._save_checkpoint(state)
        return ProcessingResult(processed=len(items))
```

### Health Check Endpoint

```python
class HealthCheckService:
    def check(self) -> HealthReport:
        checks = {
            "database": self._check_database(),
            "cache": self._check_redis(),
            "message_broker": self._check_kafka(),
            "disk_space": self._check_disk(),
        }

        overall_status = "healthy" if all(
            c.status == "healthy" for c in checks.values()
        ) else "degraded"

        return HealthReport(status=overall_status, checks=checks)

# Liveness probe — is the process alive?
GET /health/live    → 200 if process is running

# Readiness probe — is the service ready to accept traffic?
GET /health/ready   → 200 only if all dependencies are healthy
```

### Timeout Hierarchy

Every external call MUST have a timeout. Cascading timeouts to prevent thread starvation:

```python
# Outer API request timeout
REQUEST_TIMEOUT = 30  # seconds

# Database query timeout
DB_QUERY_TIMEOUT = 5  # seconds

# Cache timeout
CACHE_TIMEOUT = 1  # second

# External API call timeout
EXTERNAL_API_TIMEOUT = 10  # seconds

# Message broker publish timeout
MQ_PUBLISH_TIMEOUT = 3  # seconds
```

---

## 17. Security Standards

### Input Validation (Trust No One)

All external input MUST be validated at the system boundary. External = HTTP, queue messages, files, CLI args, environment variables.

```python
class CreateUserRequest(BaseModel):
    """Pydantic model as the validation boundary."""
    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")]
    age: Annotated[int, Field(ge=18, le=120)]
    role: Literal["admin", "user", "moderator"]

# In the controller/adapter layer:
def create_user(raw_data: dict) -> Response:
    try:
        dto = CreateUserRequest(**raw_data)  # Validates and raises if invalid
    except ValidationError as e:
        raise BadRequestError(details=e.errors())
    return use_case.execute(dto)
```

### Authentication & Authorization

**Authentication (who are you?):**
- Use JWT with short expiry (15 min access token, 7 day refresh token)
- Store refresh tokens in httpOnly cookies
- Rotate refresh tokens on use (refresh token rotation)
- Invalidate all tokens on password change

**Authorization (what can you do?):**
```python
# RBAC — Role-Based Access Control
class Permission(Enum):
    READ_ORDERS = "orders:read"
    WRITE_ORDERS = "orders:write"
    DELETE_ORDERS = "orders:delete"
    ADMIN_USERS = "users:admin"

ROLE_PERMISSIONS = {
    "customer":  {Permission.READ_ORDERS, Permission.WRITE_ORDERS},
    "support":   {Permission.READ_ORDERS},
    "admin":     set(Permission),
}

def require_permission(permission: Permission):
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            if not has_permission(request.user, permission):
                raise ForbiddenError(f"Requires permission: {permission.value}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### OWASP Top 10 Mitigations

| Threat | Mitigation |
|--------|-----------|
| **Injection (SQLi, NoSQLi)** | Parameterized queries ALWAYS. Never string concat SQL. |
| **Broken Auth** | JWT rotation, secure cookie flags, brute force protection |
| **Sensitive Data Exposure** | Encrypt at rest (AES-256), in transit (TLS 1.3), never log PII |
| **XXE** | Disable XML external entity processing |
| **IDOR** | Verify object ownership on EVERY request |
| **Security Misconfiguration** | Infra-as-code, secrets in vault, disable debug in prod |
| **XSS** | Output encoding, CSP headers, sanitize HTML input |
| **Insecure Deserialization** | Validate all deserialized data, don't deserialize untrusted data |
| **Vulnerable Dependencies** | `dependabot`, `snyk`, regular `pip audit` / `npm audit` |
| **Insufficient Logging** | Log all auth events, access denials, input validation failures |

### Secrets Management

```python
# FORBIDDEN — hardcoded secrets
DB_PASSWORD = "mysecretpassword123"
API_KEY = "sk-1234567890abcdef"

# FORBIDDEN — secrets in environment variables in code
DB_PASSWORD = os.getenv("DB_PASSWORD")  # OK for non-prod, risky for prod

# CORRECT — use a secrets manager
from vault_client import VaultClient

class SecretsProvider:
    def __init__(self):
        self._vault = VaultClient(vault_addr=os.getenv("VAULT_ADDR"))

    def get_db_password(self) -> str:
        return self._vault.read("secret/database/password")
```

---

## 18. Observability: Logs, Metrics, Traces

The **three pillars of observability**: Logs, Metrics, Distributed Traces.

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# WRONG — unstructured, unsearchable
print(f"Order {order_id} placed by user {user_id}")

# CORRECT — structured, queryable JSON
logger.info(
    "order.placed",
    order_id=str(order_id),
    user_id=str(user_id),
    total_amount=str(total.amount),
    currency=total.currency,
    items_count=len(items),
    trace_id=request.trace_id,
)
```

**Log Levels — when to use each:**

| Level | Use For |
|-------|---------|
| `DEBUG` | Detailed diagnostic info (dev/staging only) |
| `INFO` | Normal business operations (order placed, user logged in) |
| `WARNING` | Unexpected but recoverable (retry attempt, cache miss) |
| `ERROR` | Operation failed, requires attention |
| `CRITICAL` | System-wide failure, immediate action required |

**Never log:**
- Passwords, tokens, API keys
- Credit card numbers (even partial)
- Personal health information
- Any field tagged as PII

---

### Metrics (RED & USE Method)

**RED Method** (for services):
- **R**ate: Requests per second
- **E**rrors: Error rate
- **D**uration: Response time (p50, p95, p99)

**USE Method** (for resources):
- **U**tilization: % of time resource is busy
- **S**aturation: Queue depth, wait time
- **E**rrors: Error events

```python
# Using prometheus_client
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    labelnames=["method", "path", "status_code"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    labelnames=["method", "path"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
)

ACTIVE_CONNECTIONS = Gauge(
    "active_connections",
    "Number of active connections"
)

def track_request(method: str, path: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            status = 200
            try:
                return func(*args, **kwargs)
            except HTTPError as e:
                status = e.status_code
                raise
            finally:
                duration = time.time() - start
                REQUEST_COUNT.labels(method, path, status).inc()
                REQUEST_DURATION.labels(method, path).observe(duration)
        return wrapper
    return decorator
```

---

### Distributed Tracing

Every request gets a `trace_id`. Every service call gets a `span_id`. Propagate via headers.

```python
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace.get_tracer("order-service")

def place_order(command: PlaceOrderCommand, headers: dict) -> OrderResult:
    # Extract trace context from incoming request
    context = TraceContextTextMapPropagator().extract(headers)

    with tracer.start_as_current_span("place_order", context=context) as span:
        span.set_attribute("order.user_id", str(command.user_id))
        span.set_attribute("order.items_count", len(command.items))

        with tracer.start_as_current_span("validate_inventory"):
            inventory_result = inventory_client.check(command.items)

        with tracer.start_as_current_span("process_payment"):
            payment_result = payment_client.charge(command.payment)

        return OrderResult(...)
```

---

## 19. Testing Strategy

### The Testing Pyramid

```
            ▲
           /E\
          / 2E\        E2E Tests (5%)
         /  E  \       — Full system, browser tests, API integration
        /───────\
       /Integration\   Integration Tests (15%)
      /   Tests     \  — DB + service tests, message broker
     /───────────────\
    /   Unit Tests    \ Unit Tests (80%)
   /                   \ — Pure logic, no I/O, fast, many
  /─────────────────────\
```

### Unit Tests

```python
class TestOrderPlacement:
    def test_order_placed_successfully(self):
        # ARRANGE
        user_id = uuid4()
        items = [OrderItem(product_id=uuid4(), qty=2, price=Money("9.99", "USD"))]
        order = Order(user_id=user_id)

        # ACT
        events = order.place(items)

        # ASSERT
        assert order.status == OrderStatus.CONFIRMED
        assert len(events) == 1
        assert isinstance(events[0], OrderPlacedEvent)
        assert events[0].user_id == user_id

    def test_empty_order_raises(self):
        order = Order(user_id=uuid4())
        with pytest.raises(EmptyOrderError):
            order.place([])

    def test_order_total_calculated_correctly(self):
        items = [
            OrderItem(product_id=uuid4(), qty=3, price=Money("10.00", "USD")),
            OrderItem(product_id=uuid4(), qty=1, price=Money("5.00", "USD")),
        ]
        order = Order(user_id=uuid4())
        order.place(items)
        assert order.total == Money("35.00", "USD")
```

### Integration Tests

```python
@pytest.mark.integration
class TestOrderRepository:
    def test_save_and_retrieve_order(self, db_session):
        # ARRANGE
        order = Order.create(user_id=uuid4(), items=[...])
        repo = PostgresOrderRepository(db_session)

        # ACT
        repo.save(order)
        retrieved = repo.find_by_id(order.id)

        # ASSERT
        assert retrieved is not None
        assert retrieved.id == order.id
        assert retrieved.status == order.status
```

### Contract Tests (Pact)

For microservices, verify that the API contract between consumer and provider is upheld.

```python
# Consumer defines expected contract
@pytest.fixture
def order_contract(pact):
    return (
        pact
        .given("Order #123 exists")
        .upon_receiving("a request for order #123")
        .with_request("GET", "/api/v1/orders/123")
        .will_respond_with(200, body={
            "id": "123",
            "status": "confirmed",
            "total": Like({"amount": "99.99", "currency": "USD"})
        })
    )
```

### Test Rules

- Test behavior, not implementation (test *what*, not *how*)
- One assertion per logical concept (not necessarily one per test function)
- Tests must be **FAST** (unit < 1ms, integration < 1s)
- Tests must be **ISOLATED** (no shared mutable state between tests)
- Tests must be **DETERMINISTIC** (same result every run)
- Mock only what you own (use fakes for 3rd-party systems)
- Test names: `test_{what}_{when}_{expected}`

---

## 20. Performance Engineering

### Caching Strategy

**Cache Patterns:**

| Pattern | How | Best For |
|---------|-----|---------|
| **Cache-Aside** | App checks cache, loads from DB on miss | Read-heavy, variable data |
| **Write-Through** | Write to cache AND DB simultaneously | Consistency important |
| **Write-Behind** | Write to cache, async write to DB | Write-heavy, eventual consistency OK |
| **Read-Through** | Cache handles DB fetch automatically | Transparent caching |

```python
class CachingOrderRepository(IOrderRepository):
    def __init__(self, repo: IOrderRepository, cache: ICache):
        self._repo = repo
        self._cache = cache

    def find_by_id(self, order_id: UUID) -> Order | None:
        cache_key = f"order:{order_id}"

        # Cache-aside pattern
        if cached := self._cache.get(cache_key):
            return Order.deserialize(cached)

        order = self._repo.find_by_id(order_id)
        if order:
            self._cache.set(cache_key, order.serialize(), ttl=300)
        return order

    def save(self, order: Order) -> None:
        self._repo.save(order)
        self._cache.delete(f"order:{order.id}")  # Invalidate on write
```

### Database Query Optimization

```sql
-- Explain your queries in production
EXPLAIN ANALYZE
SELECT o.*, u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending'
  AND o.created_at > NOW() - INTERVAL '7 days'
ORDER BY o.created_at DESC
LIMIT 100;

-- Create targeted indexes
CREATE INDEX CONCURRENTLY idx_orders_status_created
    ON orders(status, created_at DESC)
    WHERE status = 'pending';  -- Partial index = smaller, faster

-- Use covering indexes for read-heavy queries
CREATE INDEX idx_orders_user_covering
    ON orders(user_id) INCLUDE (id, status, total_amount, created_at);
```

### Async I/O

```python
async def fetch_order_data(order_id: UUID) -> OrderDetailDTO:
    """Fetch related data concurrently, not sequentially."""
    order, user, payment, shipment = await asyncio.gather(
        order_repo.find_by_id_async(order_id),
        user_repo.find_by_order_async(order_id),
        payment_repo.find_by_order_async(order_id),
        shipment_repo.find_by_order_async(order_id),
    )
    return OrderDetailDTO.assemble(order, user, payment, shipment)
```

---

## 21. CI/CD & DevOps Pipeline

### Pipeline Stages

```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  # Stage 1: Fast feedback (< 2 min)
  lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .
      - run: mypy src/

  # Stage 2: Unit tests (< 5 min)
  unit-tests:
    runs-on: ubuntu-latest
    needs: lint-and-type-check
    steps:
      - run: pytest tests/unit/ -x --tb=short

  # Stage 3: Integration tests (< 15 min)
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    services:
      postgres:
        image: postgres:16
      redis:
        image: redis:7
    steps:
      - run: pytest tests/integration/ --tb=short

  # Stage 4: Security scan
  security-scan:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - run: pip-audit
      - run: bandit -r src/
      - uses: snyk/actions/python@master

  # Stage 5: Build and push Docker image
  build:
    needs: [integration-tests, security-scan]
    if: github.ref == 'refs/heads/main'
    steps:
      - run: docker build -t myapp:${{ github.sha }} .
      - run: docker push registry/myapp:${{ github.sha }}

  # Stage 6: Deploy to staging, run E2E
  deploy-staging:
    needs: build
    steps:
      - run: kubectl set image deployment/myapp app=registry/myapp:${{ github.sha }} -n staging
      - run: pytest tests/e2e/ --base-url=https://staging.myapp.com

  # Stage 7: Deploy to production (manual approval gate)
  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://myapp.com
    steps:
      - run: kubectl set image deployment/myapp app=registry/myapp:${{ github.sha }} -n production
```

### Deployment Strategies

| Strategy | Description | Rollback Speed | Risk |
|----------|-------------|---------------|------|
| **Recreate** | Kill old, start new | Slow | High (downtime) |
| **Rolling** | Replace instances gradually | Medium | Low |
| **Blue/Green** | Two identical envs, switch traffic | Instant | Low (double cost) |
| **Canary** | Route % traffic to new version | Instant | Very Low |
| **Feature Flags** | Deploy code, toggle in runtime | Instant | Lowest |

---

## 22. Infrastructure as Code (IaC)

### Principles

- All infrastructure is defined in version-controlled code (Terraform, Pulumi, CloudFormation)
- Environments are created/destroyed via code, not manual clicks
- No manual changes to production infrastructure
- Infrastructure changes go through the same PR/review process as application code

```hcl
# terraform/modules/service/main.tf
resource "aws_ecs_service" "order_service" {
  name            = "order-service-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.order_service.arn
  desired_count   = var.instance_count

  deployment_configuration {
    minimum_healthy_percent = 50
    maximum_percent         = 200
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.order_service.arn
    container_name   = "order-service"
    container_port   = 8080
  }
}
```

### Docker Best Practices

```dockerfile
# Multi-stage build — minimal production image
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS production
# Security: run as non-root
RUN useradd --create-home --no-log-init appuser
USER appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser src/ ./src/

# Health check built into image
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health/live || exit 1

EXPOSE 8080
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 23. Domain-Driven Design (DDD)

### Strategic DDD

**Bounded Context**: A linguistic boundary within which a specific domain model applies and is consistent.

```
┌──────────────────────┐    ┌──────────────────────┐
│   ORDERING CONTEXT   │    │  INVENTORY CONTEXT   │
│                      │    │                      │
│  Order               │    │  StockItem           │
│  LineItem            │    │  Warehouse           │
│  Customer (→ userId) │    │  Product (→ sku)     │
│                      │    │                      │
└──────────────────────┘    └──────────────────────┘
         │                             │
         │    Context Map              │
         └─────────── ACL ─────────────┘
                 (Anti-Corruption Layer)
```

**Context Map Relationships:**
- **Shared Kernel**: Two contexts share a subset of the model
- **Customer/Supplier**: Downstream team depends on upstream team
- **Conformist**: Downstream adopts upstream model as-is
- **ACL (Anti-Corruption Layer)**: Downstream translates from upstream model

### Tactical DDD Building Blocks

| Block | Purpose |
|-------|---------|
| **Entity** | Has identity (ID), mutable |
| **Value Object** | Has no identity, defined by value, immutable |
| **Aggregate** | Cluster of entities/VOs, consistency boundary |
| **Domain Event** | Something that happened, immutable fact |
| **Repository** | Abstracts persistence for aggregates |
| **Domain Service** | Business logic that doesn't belong to any entity |
| **Application Service** | Orchestrates use cases, no business logic |
| **Factory** | Complex aggregate/entity construction |

### Domain Events in Practice

```python
class Order:
    def __init__(self, ...):
        self._uncommitted_events: list[DomainEvent] = []

    def cancel(self, reason: str) -> None:
        if self._status == OrderStatus.SHIPPED:
            raise CannotCancelShippedOrderError()

        self._status = OrderStatus.CANCELLED
        self._uncommitted_events.append(
            OrderCancelledEvent(
                order_id=self.id,
                reason=reason,
                cancelled_at=datetime.now(UTC)
            )
        )

    def pull_events(self) -> list[DomainEvent]:
        """Application layer collects events after aggregate operations."""
        events = list(self._uncommitted_events)
        self._uncommitted_events.clear()
        return events

# Application Service
def cancel_order(order_id: UUID, reason: str) -> None:
    with uow:
        order = uow.orders.find_by_id(order_id)
        order.cancel(reason)
        uow.orders.save(order)
        for event in order.pull_events():
            event_bus.publish(event)
```

---

## 24. Concurrency & Async Patterns

### Optimistic Locking

```python
class Order:
    version: int = 0  # Incremented on each save

class PostgresOrderRepository:
    def save(self, order: Order) -> None:
        result = self._db.execute("""
            UPDATE orders
            SET status = %s, version = version + 1
            WHERE id = %s AND version = %s
        """, [order.status, order.id, order.version])

        if result.rowcount == 0:
            raise ConcurrentModificationError(
                f"Order {order.id} was modified by another process"
            )
```

### Async Task Queue Pattern

```python
# Producer
async def place_order(command: PlaceOrderCommand) -> UUID:
    order = Order.create(command)
    await order_repo.save(order)

    # Dispatch heavy work to queue, respond immediately
    await task_queue.enqueue(
        "send_order_confirmation",
        {"order_id": str(order.id), "user_email": command.user_email},
        priority="high"
    )
    return order.id

# Consumer (separate worker process)
@task_queue.worker("send_order_confirmation")
async def handle_send_confirmation(payload: dict) -> None:
    order = await order_repo.find_by_id(UUID(payload["order_id"]))
    await email_service.send_confirmation(
        to=payload["user_email"],
        order=order
    )
```

### Thread Safety Checklist

- [ ] Shared mutable state is protected by locks
- [ ] Database connections are not shared across threads
- [ ] Singletons are thread-safe (double-checked locking)
- [ ] No global mutable variables
- [ ] Async code doesn't block the event loop (no `time.sleep` in async)
- [ ] Connection pools are sized appropriately for concurrency level

---

## 25. Documentation Standards

### Code Documentation

```python
def calculate_compound_interest(
    principal: Money,
    annual_rate: Decimal,
    periods_per_year: int,
    years: int,
) -> Money:
    """
    Calculate compound interest using the standard formula.

    Formula: A = P(1 + r/n)^(nt)
    Where:
        A = final amount
        P = principal
        r = annual rate (as decimal, e.g. 0.05 for 5%)
        n = compounding periods per year
        t = time in years

    Args:
        principal:         Initial investment amount
        annual_rate:       Annual interest rate (0.05 = 5%)
        periods_per_year:  Number of compounding periods per year
                           (1=annually, 4=quarterly, 12=monthly, 365=daily)
        years:             Investment duration in years

    Returns:
        Final amount including principal and interest

    Raises:
        NegativePrincipalError:  If principal is negative
        InvalidRateError:        If annual_rate is not in range [0, 1]
        InvalidPeriodsError:     If periods_per_year < 1

    Example:
        >>> calculate_compound_interest(
        ...     principal=Money("1000.00", "USD"),
        ...     annual_rate=Decimal("0.05"),
        ...     periods_per_year=12,
        ...     years=10
        ... )
        Money("1647.01", "USD")
    """
```

### Architecture Decision Records (ADR)

Store architectural decisions in version control. Template:

```markdown
# ADR-042: Use Kafka for Inter-Service Events

**Date:** 2026-03-11
**Status:** Accepted
**Deciders:** @arch-team

## Context
We need reliable async communication between 12 microservices.
Current approach (direct HTTP) creates tight coupling and loses events on failure.

## Decision
Use Apache Kafka as the central event bus for all inter-service communication.

## Consequences
**Positive:**
- Decoupled services — publisher doesn't need consumers to be up
- Event replay capability
- Horizontal scaling of consumers

**Negative:**
- Operational complexity of managing Kafka cluster
- Eventual consistency (not immediate)
- Requires consumer idempotency

## Alternatives Considered
- **RabbitMQ**: Simpler ops, but no log retention / replay
- **AWS SNS/SQS**: Managed, but vendor lock-in, higher latency
- **Direct HTTP**: Zero infra, but tight coupling, no durability
```

---

## 26. Team Process & Code Culture

### Git Workflow

**Branch naming:**
```
feature/TICKET-123-add-payment-method
bugfix/TICKET-456-fix-order-total-calculation
hotfix/TICKET-789-critical-payment-failure
chore/TICKET-012-upgrade-dependencies
```

**Commit messages (Conventional Commits):**
```
feat(orders): add bulk order cancellation
fix(payments): prevent double charge on retry
docs(api): update order endpoint examples
refactor(auth): extract token validation logic
test(inventory): add concurrent reservation tests
chore(deps): upgrade django from 4.2 to 5.0
perf(queries): add covering index for order listing
```

### Code Review Standards

**What reviewers check:**
- [ ] Does the code do what the ticket says?
- [ ] Are there sufficient tests?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?
- [ ] Are there any security concerns?
- [ ] Is the code readable without needing explanation?
- [ ] Are there any SOLID violations?
- [ ] Is there unnecessary complexity?
- [ ] Are logs meaningful and not leaking PII?

**Review etiquette:**
- Nitpicks must be labeled `[nit]` — author can ignore
- Blocking comments require explanation
- Approve with requested changes when concerns are minor
- Never approve without reading

### Definition of Done

A feature is DONE when:
- [ ] Code is written and reviewed
- [ ] Unit tests pass (coverage ≥ 80% on new code)
- [ ] Integration tests pass
- [ ] Documentation updated (API docs, ADR if architectural change)
- [ ] Feature flags configured if needed
- [ ] Monitoring/alerts configured
- [ ] Deployed to staging and verified
- [ ] Product Owner acceptance

---

## 27. Anti-Patterns — What to Avoid

| Anti-Pattern | Description | Solution |
|-------------|-------------|---------|
| **God Object** | One class that knows/does everything | Split by SRP |
| **Magic Numbers** | `if status == 3` | Use named constants/enums |
| **Shotgun Surgery** | One change requires edits in many places | Encapsulate related logic |
| **Primitive Obsession** | Using `str` for email, `int` for money | Use Value Objects |
| **Feature Envy** | Method uses another class's data more than its own | Move to appropriate class |
| **Data Clumps** | Same 3 parameters always together | Create a data object |
| **Divergent Change** | Class changes for multiple different reasons | Split class |
| **Lazy Class** | Class does almost nothing | Merge or delete |
| **Speculative Generality** | Abstractions with no current concrete need | YAGNI |
| **Temporal Coupling** | `A.init()` must be called before `A.process()` | Use constructor injection |
| **Service Locator** | Global registry for dependencies | Proper DI container |
| **Anemic Domain Model** | Domain objects are just data bags, logic in services | Move logic to entities |
| **Distributed Monolith** | Microservices that deploy together | Fix service boundaries |
| **N+1 Query** | Loop makes DB query per iteration | Use JOIN or eager loading |
| **Spaghetti Code** | No structure, everything calls everything | Apply Clean Architecture |

---

## 28. Checklists — Pre-Deploy & Architecture Review

### Pre-Deploy Checklist

```
SECURITY
─────────────────────────────────────────────────────────
[ ] No secrets committed to repository
[ ] All external input is validated
[ ] Authentication and authorization verified
[ ] Dependencies scanned for vulnerabilities (pip-audit / npm audit)
[ ] SQL injection impossible (parameterized queries everywhere)

RELIABILITY
─────────────────────────────────────────────────────────
[ ] All external calls have timeouts configured
[ ] Retry logic implemented for transient failures
[ ] Circuit breakers in place for critical dependencies
[ ] Graceful shutdown implemented (SIGTERM handler)
[ ] Database migrations are backwards-compatible

OBSERVABILITY
─────────────────────────────────────────────────────────
[ ] Structured logging in place
[ ] Key business events are logged
[ ] Metrics exposed on /metrics endpoint
[ ] Distributed tracing headers propagated
[ ] Health check endpoints respond correctly
[ ] Alerts configured for error rate and latency

PERFORMANCE
─────────────────────────────────────────────────────────
[ ] Database queries are indexed (EXPLAIN ANALYZE reviewed)
[ ] No N+1 queries
[ ] Appropriate caching in place
[ ] Load tested under expected peak traffic

DATA
─────────────────────────────────────────────────────────
[ ] Database migrations tested on staging with production data size
[ ] Rollback plan exists for data migrations
[ ] PII is identified and handled per data policy
[ ] Backups tested and recovery time measured
```

### Architecture Review Checklist

```
DESIGN
─────────────────────────────────────────────────────────
[ ] Bounded contexts are clearly defined
[ ] Dependencies flow inward (Clean Architecture)
[ ] Aggregates enforce invariants
[ ] Domain model is free of framework dependencies
[ ] APIs follow versioning standard

SCALABILITY
─────────────────────────────────────────────────────────
[ ] Stateless service design (state externalized)
[ ] Horizontal scaling possible without rearchitecting
[ ] Database is not the bottleneck (read replicas, sharding plan)
[ ] Caching strategy documented

OPERATIONAL
─────────────────────────────────────────────────────────
[ ] Deployment strategy defined (rolling/canary/blue-green)
[ ] Feature flags in place for risky changes
[ ] Runbook exists for common failure scenarios
[ ] On-call escalation path documented
[ ] Disaster recovery plan tested
```

---

## APPENDIX: Quick Reference

### Complexity vs Benefit Trade-Off

```
Use Clean Architecture when:         Skip it when:
─ Team > 3 devs                      ─ Weekend project
─ Multiple integration points        ─ Script/CLI tool
─ Long-lived codebase                ─ Pure data pipeline
─ Multiple teams working on it       ─ Prototype (until it isn't)

Use Microservices when:              Skip it when:
─ Teams need independent deploys     ─ Team < 10 devs
─ Services scale differently         ─ Business domain still fuzzy
─ Different tech stacks needed       ─ Starting a new product

Use Event Sourcing when:             Skip it when:
─ Audit trail is a core requirement  ─ No audit requirements
─ Time travel debugging needed       ─ Simple CRUD app
─ Complex projections required       ─ Team unfamiliar with the pattern
```

### The Golden Rules Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                  THE 10 COMMANDMENTS                            │
├─────────────────────────────────────────────────────────────────┤
│  I.   Thou shalt not duplicate logic                            │
│  II.  Thou shalt write only what is needed, no more             │
│  III. Thou shalt name things as if thy life depends on it       │
│  IV.  Thou shalt invert thy dependencies                        │
│  V.   Thou shalt validate all external input                    │
│  VI.  Thou shalt make all I/O atomic                            │
│  VII. Thou shalt log with structure and purpose                 │
│  VIII.Thou shalt test behavior, not implementation              │
│  IX.  Thou shalt never store secrets in code                    │
│  X.   Thou shalt always have a rollback plan                    │
└─────────────────────────────────────────────────────────────────┘
```

---

*ASGUARD01 SYSTEM STANDARDS — Full Architect's Guide*
*Version 3.0 · Last updated: 2026 · Classification: Internal Reference*

> *"Make it work. Make it right. Make it fast."*
> — Kent Beck
