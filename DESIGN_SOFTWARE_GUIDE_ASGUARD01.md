# ASGUARD01 SOFTWARE DESIGN GUIDE

```
   ___   ____  _____ _   _   ___  ____  ____   ___  _ 
  / _ \ / ___||  ___| | | | / _ \|  _ \|  _ \ / _ \/ |
 | |_| |\___ \| |_  | | | |/ /_\ \ |_) | | | | | | | |
 |  _  | ___) |  _| | |_| |  _  |  _ <| |_| | |_| | |
 |_| |_||____/|_|    \___/|_| |_|_| \_\____/ \___/|_|
                                                       
```

**Version 3.0** | *Enterprise Software Development Standards*  
© 1985-2026 Asguard01 Corp. | Last Updated: February 2026

---

## 📋 TABLE OF CONTENTS

1. [Core Principles](#1-core-principles-code-integrity)
2. [System Architecture (SOLID)](#2-system-architecture-solid)
3. [Layered Topology (Clean Architecture)](#3-layered-topology-clean-architecture)
4. [Design Patterns](#4-design-patterns)
5. [Low-Level Standards](#5-low-level-standards)
6. [Resilience Protocol](#6-resilience-protocol-fault-tolerance)
7. [Testing Strategy](#7-testing-strategy-quality-assurance)
8. [Security Standards](#8-security-standards-defense-in-depth)
9. [Performance Engineering](#9-performance-engineering)
10. [Documentation & Maintainability](#10-documentation--maintainability)
11. [DevOps & Deployment](#11-devops--deployment)
12. [Code Review Checklist](#12-code-review-checklist)

---

## 1. CORE PRINCIPLES (Code Integrity)

### `[DRY]` Don't Repeat Yourself
**NEVER DUPLICATE LOGIC. REDUNDANCY IS THE ENEMY OF STABILITY.**

- Extract common logic into reusable functions/classes
- Use inheritance, composition, or mixins to share behavior
- Single source of truth for business rules

**❌ Bad:**
```python
def calculate_user_discount(user):
    if user.membership == "gold":
        return 0.20
    return 0.10

def calculate_order_discount(order):
    if order.user.membership == "gold":
        return 0.20
    return 0.10
```

**✅ Good:**
```python
class DiscountCalculator:
    MEMBERSHIP_DISCOUNTS = {"gold": 0.20, "silver": 0.10}
    
    @staticmethod
    def get_discount(membership: str) -> float:
        return DiscountCalculator.MEMBERSHIP_DISCOUNTS.get(membership, 0.0)
```

---

### `[KISS]` Keep It Simple, Stupid
**SIMPLICITY OVER COMPLEXITY. AVOID OVER-ENGINEERING.**

- Choose the simplest solution that solves the problem
- Avoid premature optimization
- Complexity should be justified by requirements

**❌ Bad:**
```python
class AbstractFactoryProducerSingletonManager:
    """Over-engineered solution for simple config"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**✅ Good:**
```python
# Simple module-level config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/db")
```

---

### `[YAGNI]` You Aren't Gonna Need It
**CODE ONLY WHAT IS MANDATED. NO GHOST FEATURES.**

- Implement features when they are actually needed
- Remove unused code immediately
- Don't build for hypothetical future requirements

---

### `[NAME]` Naming Conventions
**NOUNS FOR DATA, VERBS FOR ACTIONS. BE EXPLICIT.**

| Type | Convention | Example |
|------|-----------|---------|
| Classes | PascalCase nouns | `UserAccount`, `OrderProcessor` |
| Functions | snake_case verbs | `calculate_total()`, `send_email()` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_TIMEOUT` |
| Variables | snake_case descriptive | `user_email`, `order_total` |
| Booleans | is/has/can prefix | `is_valid`, `has_permission`, `can_edit` |

---

### `[UNIT]` Single Responsibility
**KEEP FUNCTIONS ATOMIC. ONE TASK PER SUBROUTINE.**

- Function should do one thing and do it well
- If function name contains "and", it's doing too much
- Aim for functions under 20 lines

**❌ Bad:**
```python
def process_order_and_send_email_and_update_inventory(order):
    # Validates, processes payment, updates DB, sends email
    # 150 lines of mixed responsibilities
    pass
```

**✅ Good:**
```python
def process_order(order: Order) -> OrderResult:
    validate_order(order)
    result = charge_payment(order)
    update_inventory(order.items)
    send_confirmation_email(order.user, result)
    return result
```

---

### `[INFO]` Self-Documenting Code
**CODE MUST BE READABLE. COMMENTS JUSTIFY INTENT, NOT SYNTAX.**

- Code explains **what**, comments explain **why**
- Avoid obvious comments
- Use docstrings for public APIs

**❌ Bad:**
```python
# Increment i by 1
i = i + 1

# Loop through users
for user in users:
    # Process user
    process(user)
```

**✅ Good:**
```python
def calculate_compound_interest(principal, rate, years):
    """
    Calculate compound interest using daily compounding.
    
    We use daily compounding (365) instead of annual because
    our financial regulations require daily accrual reporting.
    """
    return principal * (1 + rate/365) ** (365 * years)
```

---

## 2. SYSTEM ARCHITECTURE (SOLID)

### `[S]` Single Responsibility Principle
**ONE MODULE, ONE REASON TO CHANGE.**

Each class should have only one reason to change (one responsibility).

**❌ Violates SRP:**
```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):  # ❌ Persistence responsibility
        pass
    
    def send_welcome_email(self):  # ❌ Notification responsibility
        pass
    
    def generate_pdf_report(self):  # ❌ Reporting responsibility
        pass
```

**✅ Follows SRP:**
```python
class User:
    """Domain model - only user data and behavior"""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def get_full_name(self) -> str:
        return self.name

class UserRepository:
    """Persistence layer"""
    def save(self, user: User) -> None:
        pass

class EmailService:
    """Notification layer"""
    def send_welcome_email(self, user: User) -> None:
        pass

class ReportGenerator:
    """Reporting layer"""
    def generate_user_report(self, user: User) -> bytes:
        pass
```

---

### `[O]` Open/Closed Principle
**EXTEND SYSTEM VIA NEW CODE, NOT MODIFICATION.**

Software entities should be open for extension but closed for modification.

**❌ Requires modification:**
```python
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    # Adding triangle requires modifying this function ❌
```

**✅ Open for extension:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def calculate_area(self) -> float:
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def calculate_area(self) -> float:
        return self.width * self.height

# Adding Triangle requires no changes to existing code ✅
class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    
    def calculate_area(self) -> float:
        return 0.5 * self.base * self.height
```

---

### `[L]` Liskov Substitution Principle
**SUBTYPES MUST BE INTERCHANGEABLE.**

Objects of a superclass should be replaceable with objects of a subclass without breaking the application.

**❌ Violates LSP:**
```python
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly")  # ❌ Breaks contract
```

**✅ Follows LSP:**
```python
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        return self.fly()
    
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def move(self):
        return self.swim()
    
    def swim(self):
        return "Swimming"
```

---

### `[I]` Interface Segregation Principle
**PREFER GRANULAR INTERFACES OVER BULK OBJECTS.**

Clients should not be forced to depend on interfaces they don't use.

**❌ Fat interface:**
```python
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    
    @abstractmethod
    def eat(self): pass
    
    @abstractmethod
    def sleep(self): pass

class Robot(Worker):
    def work(self): return "Working"
    def eat(self): raise NotImplementedError  # ❌ Robots don't eat
    def sleep(self): raise NotImplementedError  # ❌ Robots don't sleep
```

**✅ Segregated interfaces:**
```python
class Workable(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC):
    @abstractmethod
    def eat(self): pass

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): pass

class Human(Workable, Eatable, Sleepable):
    def work(self): return "Working"
    def eat(self): return "Eating"
    def sleep(self): return "Sleeping"

class Robot(Workable):
    def work(self): return "Working 24/7"
```

---

### `[D]` Dependency Inversion Principle
**DEPEND ON ABSTRACTIONS, NOT IMPLEMENTATIONS.**

High-level modules should not depend on low-level modules. Both should depend on abstractions.

**❌ Direct dependency:**
```python
class MySQLDatabase:
    def save(self, data): pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # ❌ Tight coupling to MySQL
    
    def create_user(self, user):
        self.db.save(user)
```

**✅ Dependency injection:**
```python
class Database(ABC):
    @abstractmethod
    def save(self, data): pass

class MySQLDatabase(Database):
    def save(self, data): pass

class PostgreSQLDatabase(Database):
    def save(self, data): pass

class UserService:
    def __init__(self, database: Database):  # ✅ Depends on abstraction
        self.db = database
    
    def create_user(self, user):
        self.db.save(user)

# Inject dependency
service = UserService(PostgreSQLDatabase())
```

---

## 3. LAYERED TOPOLOGY (Clean Architecture)

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTERFACES                      │
│  (UI, Web Frameworks, Databases, External APIs, Devices)   │
│                     ↓ Adapters ↓                            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              INTERFACE ADAPTERS LAYER                      │
│    (Controllers, Presenters, Gateways, View Models)       │
│                   ↓ Use Cases ↓                            │
└────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              APPLICATION BUSINESS RULES                    │
│           (Use Cases, Application Services)                │
│                ↓ Domain Entities ↓                         │
└────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│           ENTERPRISE BUSINESS RULES (CORE)                 │
│              (Entities, Domain Models)                     │
│              ← CENTER OF THE UNIVERSE →                    │
└────────────────────────────────────────────────────────────┘
```

### `[LAYER]` Core Principles

**CORE LOGIC (BUSINESS RULES) IS THE CENTER OF THE UNIVERSE.**

- **Domain Layer**: Pure business logic, no dependencies
- **Application Layer**: Use cases, orchestration
- **Infrastructure Layer**: Databases, APIs, frameworks
- **Presentation Layer**: UI, controllers, views

---

### `[DIR]` Dependency Rule

**DEPENDENCIES FLOW INWARD. KERNEL KNOWS NOTHING OF PERIPHERALS.**

```
Outer layers can depend on inner layers ✅
Inner layers CANNOT depend on outer layers ❌

UI → Application → Domain ✅
Domain → Application ❌
Domain → UI ❌
```

---

### `[DB/UI]` Hardware Independence

**DATABASE AND INTERFACE ARE PLUGINS.**

Your business logic should work with:
- Any database (PostgreSQL, MySQL, MongoDB, in-memory)
- Any UI (Web, Mobile, CLI, API)
- Any framework (FastAPI, Django, Flask, etc.)

**Example Structure:**

```python
# CORE DOMAIN (innermost layer)
class User:
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name
    
    def is_valid(self) -> bool:
        return "@" in self.email and len(self.name) > 0

# APPLICATION LAYER
class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def execute(self, email: str, name: str) -> User:
        user = User(email, name)
        if not user.is_valid():
            raise ValueError("Invalid user data")
        return self.user_repo.save(user)

# INFRASTRUCTURE LAYER (outermost)
class PostgreSQLUserRepository(UserRepository):
    def save(self, user: User) -> User:
        # PostgreSQL-specific implementation
        pass

class MongoUserRepository(UserRepository):
    def save(self, user: User) -> User:
        # MongoDB-specific implementation
        pass
```

---

### `[DTO]` Data Transfer Objects

**CROSS BOUNDARIES USING DATA TRANSFER OBJECTS ONLY.**

Never pass entities directly across architectural boundaries. Use DTOs/View Models.

```python
# ❌ BAD: Exposing domain entity to UI
@app.get("/users/{id}")
def get_user(id: int) -> User:  # Domain entity leaked to API
    return user_repository.find_by_id(id)

# ✅ GOOD: Using DTO
class UserDTO:
    def __init__(self, id: int, email: str, name: str):
        self.id = id
        self.email = email
        self.name = name

@app.get("/users/{id}")
def get_user(id: int) -> UserDTO:
    user = user_repository.find_by_id(id)
    return UserDTO(user.id, user.email, user.name)
```

---

## 4. DESIGN PATTERNS

### `[FACTORY]` Factory Pattern
**DYNAMIC INSTANTIATION WITHOUT HARD-CODING TYPES.**

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class StripeProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f"Processing ${amount} via Stripe")
        return True

class PayPalProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f"Processing ${amount} via PayPal")
        return True

class PaymentProcessorFactory:
    @staticmethod
    def create(processor_type: str) -> PaymentProcessor:
        processors = {
            "stripe": StripeProcessor,
            "paypal": PayPalProcessor
        }
        
        processor_class = processors.get(processor_type.lower())
        if not processor_class:
            raise ValueError(f"Unknown processor: {processor_type}")
        
        return processor_class()

# Usage
processor = PaymentProcessorFactory.create("stripe")
processor.process(99.99)
```

---

### `[STRATEGY]` Strategy Pattern
**SWAPPABLE ALGORITHMS DURING RUNTIME.**

```python
class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: str) -> bytes:
        pass

class ZipCompression(CompressionStrategy):
    def compress(self, data: str) -> bytes:
        return data.encode('zip')

class RarCompression(CompressionStrategy):
    def compress(self, data: str) -> bytes:
        return data.encode('rar')

class FileCompressor:
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: CompressionStrategy):
        self._strategy = strategy
    
    def compress_file(self, data: str) -> bytes:
        return self._strategy.compress(data)

# Usage
compressor = FileCompressor(ZipCompression())
result = compressor.compress_file("data")

# Change strategy at runtime
compressor.set_strategy(RarCompression())
result = compressor.compress_file("data")
```

---

### `[REPOSITORY]` Repository Pattern
**DATA PERSISTENCE IS HIDDEN BEHIND A CLEAN API.**

```python
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

class PostgreSQLUserRepository(UserRepository):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        # PostgreSQL implementation
        row = self.db.execute(
            "SELECT * FROM users WHERE id = %s", (user_id,)
        )
        return User.from_db_row(row) if row else None
    
    def save(self, user: User) -> User:
        # PostgreSQL implementation
        pass

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user
```

---

### `[DECORATOR]` Decorator Pattern
**ADD WRAPPERS (LOGGING/CACHE) WITHOUT ALTERING SOURCE.**

```python
class DataSource(ABC):
    @abstractmethod
    def read_data(self) -> str:
        pass

class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self.filename = filename
    
    def read_data(self) -> str:
        with open(self.filename) as f:
            return f.read()

class CachedDataSource(DataSource):
    def __init__(self, source: DataSource):
        self._source = source
        self._cache = None
    
    def read_data(self) -> str:
        if self._cache is None:
            self._cache = self._source.read_data()
        return self._cache

class LoggedDataSource(DataSource):
    def __init__(self, source: DataSource):
        self._source = source
    
    def read_data(self) -> str:
        print(f"Reading data from {self._source.__class__.__name__}")
        data = self._source.read_data()
        print(f"Read {len(data)} bytes")
        return data

# Usage - stack decorators
source = FileDataSource("data.txt")
source = CachedDataSource(source)
source = LoggedDataSource(source)
data = source.read_data()
```

---

### `[OBSERVER]` Observer Pattern
**EVENT-DRIVEN COMMUNICATION BETWEEN MODULES.**

```python
class EventPublisher:
    def __init__(self):
        self._subscribers = []
    
    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)
    
    def notify(self, event: dict):
        for subscriber in self._subscribers:
            subscriber.update(event)

class EmailNotifier:
    def update(self, event: dict):
        print(f"Sending email: {event}")

class SMSNotifier:
    def update(self, event: dict):
        print(f"Sending SMS: {event}")

class AuditLogger:
    def update(self, event: dict):
        print(f"Logging to audit: {event}")

# Usage
publisher = EventPublisher()
publisher.subscribe(EmailNotifier())
publisher.subscribe(SMSNotifier())
publisher.subscribe(AuditLogger())

publisher.notify({"type": "user_created", "user_id": 123})
```

---

## 5. LOW-LEVEL STANDARDS

### `[TYPE]` Strict Type Hinting
**CONTRACTS MUST BE ENFORCED.**

```python
from typing import List, Dict, Optional, Union
from decimal import Decimal

# ❌ BAD: No type hints
def calculate_total(items, tax_rate):
    return sum(item.price for item in items) * (1 + tax_rate)

# ✅ GOOD: Strict type hints
def calculate_total(
    items: List[OrderItem],
    tax_rate: Decimal
) -> Decimal:
    subtotal = sum(item.price for item in items)
    return subtotal * (Decimal('1') + tax_rate)

# Use type aliases for complex types
UserId = int
OrderId = int
UserCache = Dict[UserId, User]

def get_user_from_cache(
    cache: UserCache,
    user_id: UserId
) -> Optional[User]:
    return cache.get(user_id)
```

**Enable static type checking:**
```bash
# mypy configuration
pip install mypy
mypy --strict your_module.py
```

---

### `[LOGS]` Structured Logging
**SYSTEM LOGGING ONLY. "PRINT" IS FOR DEBUGGING, NOT PRODUCTION.**

```python
import logging
import json
from datetime import datetime

# ❌ BAD: Print statements
def process_payment(order_id, amount):
    print(f"Processing payment for order {order_id}")
    # ...
    print(f"Payment successful: ${amount}")

# ✅ GOOD: Structured logging
logger = logging.getLogger(__name__)

def process_payment(order_id: int, amount: Decimal) -> PaymentResult:
    logger.info(
        "payment.processing",
        extra={
            "order_id": order_id,
            "amount": float(amount),
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    
    try:
        result = charge_payment(order_id, amount)
        
        logger.info(
            "payment.success",
            extra={
                "order_id": order_id,
                "transaction_id": result.transaction_id,
                "amount": float(amount)
            }
        )
        return result
        
    except PaymentError as e:
        logger.error(
            "payment.failed",
            extra={
                "order_id": order_id,
                "error": str(e),
                "error_code": e.code
            },
            exc_info=True
        )
        raise
```

**Logging Levels:**
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages for potentially harmful situations
- `ERROR`: Error events that might still allow the application to continue
- `CRITICAL`: Very severe error events that might cause the application to abort

---

### `[EXCEPT]` Custom Error Classes
**BUSINESS-SPECIFIC FAILURES.**

```python
# Base exception hierarchy
class ApplicationError(Exception):
    """Base class for all application errors"""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationError(ApplicationError):
    """Raised when data validation fails"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field

class NotFoundError(ApplicationError):
    """Raised when resource is not found"""
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} not found: {identifier}"
        super().__init__(message, "NOT_FOUND")
        self.resource = resource
        self.identifier = identifier

class PermissionDeniedError(ApplicationError):
    """Raised when user lacks permissions"""
    def __init__(self, action: str, resource: str):
        message = f"Permission denied: {action} on {resource}"
        super().__init__(message, "PERMISSION_DENIED")

# Usage
def get_user(user_id: int) -> User:
    user = repository.find(user_id)
    if not user:
        raise NotFoundError("User", str(user_id))
    return user

def update_user(user_id: int, data: dict) -> User:
    if not data.get("email"):
        raise ValidationError("Email is required", field="email")
    
    user = get_user(user_id)
    if not current_user.can_edit(user):
        raise PermissionDeniedError("update", f"User({user_id})")
    
    return repository.update(user, data)
```

---

### `[VALID]` Input Validation
**VALIDATE ALL EXTERNAL INPUT AT THE SYSTEM FRONTIER.**

```python
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    
    @validator('name')
    def name_must_not_contain_numbers(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError('Name cannot contain numbers')
        return v.strip()
    
    @validator('age')
    def age_must_be_reasonable(cls, v):
        if v is not None and v < 13:
            raise ValueError('User must be at least 13 years old')
        return v

# API endpoint
@app.post("/users")
def create_user(request: CreateUserRequest):
    # request is already validated by Pydantic
    user = user_service.create(
        email=request.email,
        name=request.name,
        age=request.age
    )
    return {"id": user.id}

# SQL Injection Prevention
def get_user_by_email(email: str) -> Optional[User]:
    # ❌ NEVER DO THIS (SQL injection vulnerability)
    # query = f"SELECT * FROM users WHERE email = '{email}'"
    
    # ✅ ALWAYS use parameterized queries
    query = "SELECT * FROM users WHERE email = %s"
    result = db.execute(query, (email,))
    return User.from_row(result) if result else None
```

---

## 6. RESILIENCE PROTOCOL (Fault Tolerance)

### `[STATE]` State Externalization
**STATE IS EXTERNALIZED. TRACK OFFSET, STATUS, AND CHECKSUMS.**

```python
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ProcessingState:
    job_id: str
    current_offset: int
    total_records: int
    status: str  # 'pending', 'processing', 'completed', 'failed'
    last_checkpoint: datetime
    error_count: int = 0
    checksum: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps({
            'job_id': self.job_id,
            'current_offset': self.current_offset,
            'total_records': self.total_records,
            'status': self.status,
            'last_checkpoint': self.last_checkpoint.isoformat(),
            'error_count': self.error_count,
            'checksum': self.checksum
        })
    
    @staticmethod
    def from_json(data: str) -> 'ProcessingState':
        obj = json.loads(data)
        obj['last_checkpoint'] = datetime.fromisoformat(obj['last_checkpoint'])
        return ProcessingState(**obj)

class StateManager:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
    
    def save_state(self, state: ProcessingState):
        with open(f"{self.storage_path}/{state.job_id}.state", 'w') as f:
            f.write(state.to_json())
    
    def load_state(self, job_id: str) -> Optional[ProcessingState]:
        try:
            with open(f"{self.storage_path}/{job_id}.state", 'r') as f:
                return ProcessingState.from_json(f.read())
        except FileNotFoundError:
            return None
```

---

### `[RESUME]` Auto-Recovery
**RESUME FROM LAST CHECKPOINT AFTER POWER LOSS.**

```python
class DataProcessor:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
    
    def process_large_file(self, job_id: str, filename: str):
        # Try to resume from checkpoint
        state = self.state_manager.load_state(job_id)
        
        if state and state.status == 'processing':
            logger.info(f"Resuming job {job_id} from offset {state.current_offset}")
            start_offset = state.current_offset
        else:
            logger.info(f"Starting new job {job_id}")
            start_offset = 0
            state = ProcessingState(
                job_id=job_id,
                current_offset=0,
                total_records=self._count_records(filename),
                status='processing',
                last_checkpoint=datetime.utcnow()
            )
        
        try:
            with open(filename, 'r') as file:
                # Skip to checkpoint
                for _ in range(start_offset):
                    next(file)
                
                # Process remaining records
                for i, line in enumerate(file, start=start_offset):
                    self._process_record(line)
                    
                    # Checkpoint every 1000 records
                    if (i + 1) % 1000 == 0:
                        state.current_offset = i + 1
                        state.last_checkpoint = datetime.utcnow()
                        self.state_manager.save_state(state)
                        logger.debug(f"Checkpoint: {i + 1}/{state.total_records}")
            
            # Mark as completed
            state.status = 'completed'
            state.current_offset = state.total_records
            self.state_manager.save_state(state)
            
        except Exception as e:
            state.status = 'failed'
            state.error_count += 1
            self.state_manager.save_state(state)
            logger.error(f"Job {job_id} failed: {e}")
            raise
    
    def _count_records(self, filename: str) -> int:
        with open(filename, 'r') as f:
            return sum(1 for _ in f)
    
    def _process_record(self, record: str):
        # Process individual record
        pass
```

---

### `[ATOM]` Atomic I/O
**WRITE TO TMP, THEN SWAP. NO CORRUPT FILES.**

```python
import os
import tempfile
import shutil

def atomic_write(filename: str, content: str):
    """
    Write file atomically to prevent corruption.
    
    If process crashes mid-write, original file remains intact.
    """
    # Write to temporary file first
    dir_name = os.path.dirname(filename)
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, text=True)
    
    try:
        with os.fdopen(fd, 'w') as tmp_file:
            tmp_file.write(content)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())  # Force write to disk
        
        # Atomic rename (OS-level operation)
        shutil.move(tmp_path, filename)
        
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise

# Usage
atomic_write('/var/data/critical.json', json.dumps(data))
```

---

### `[IDEM]` Idempotency
**RE-RUNNING A TASK PRODUCES THE SAME RESULT.**

```python
class PaymentService:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo
    
    def process_payment(self, idempotency_key: str, order_id: int, amount: Decimal):
        """
        Idempotent payment processing.
        
        Calling this multiple times with same idempotency_key
        will only charge once.
        """
        # Check if payment already processed
        existing = self.payment_repo.find_by_idempotency_key(idempotency_key)
        if existing:
            logger.info(f"Payment already processed: {idempotency_key}")
            return existing
        
        # Process new payment
        try:
            result = self._charge_payment_gateway(order_id, amount)
            
            # Store with idempotency key
            payment = Payment(
                idempotency_key=idempotency_key,
                order_id=order_id,
                amount=amount,
                transaction_id=result.transaction_id,
                status='completed'
            )
            
            self.payment_repo.save(payment)
            return payment
            
        except PaymentGatewayError as e:
            # Store failed attempt to prevent retries
            payment = Payment(
                idempotency_key=idempotency_key,
                order_id=order_id,
                amount=amount,
                status='failed',
                error_message=str(e)
            )
            self.payment_repo.save(payment)
            raise

# API usage with idempotency
@app.post("/payments")
def create_payment(
    request: PaymentRequest,
    idempotency_key: str = Header(...)
):
    return payment_service.process_payment(
        idempotency_key=idempotency_key,
        order_id=request.order_id,
        amount=request.amount
    )
```

---

### `[HEALTH]` Self-Diagnosis
**VERIFY INTEGRITY BEFORE EXECUTION.**

```python
from enum import Enum
from typing import List

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class HealthCheck:
    def __init__(self, name: str, check_func):
        self.name = name
        self.check_func = check_func
    
    def execute(self) -> tuple[HealthStatus, str]:
        try:
            return self.check_func()
        except Exception as e:
            return HealthStatus.UNHEALTHY, str(e)

class SystemHealth:
    def __init__(self):
        self.checks: List[HealthCheck] = []
    
    def register_check(self, name: str, check_func):
        self.checks.append(HealthCheck(name, check_func))
    
    def run_diagnostics(self) -> dict:
        results = {}
        overall_status = HealthStatus.HEALTHY
        
        for check in self.checks:
            status, message = check.execute()
            results[check.name] = {
                "status": status.value,
                "message": message
            }
            
            if status == HealthStatus.UNHEALTHY:
                overall_status = HealthStatus.UNHEALTHY
            elif status == HealthStatus.DEGRADED and overall_status == HealthStatus.HEALTHY:
                overall_status = HealthStatus.DEGRADED
        
        return {
            "status": overall_status.value,
            "checks": results
        }

# Register health checks
health = SystemHealth()

def check_database():
    try:
        db.execute("SELECT 1")
        return HealthStatus.HEALTHY, "Database connected"
    except Exception as e:
        return HealthStatus.UNHEALTHY, f"Database error: {e}"

def check_redis():
    try:
        redis.ping()
        return HealthStatus.HEALTHY, "Redis connected"
    except Exception as e:
        return HealthStatus.DEGRADED, f"Redis unavailable: {e}"

def check_disk_space():
    usage = shutil.disk_usage("/")
    percent_used = (usage.used / usage.total) * 100
    
    if percent_used > 90:
        return HealthStatus.UNHEALTHY, f"Disk {percent_used:.1f}% full"
    elif percent_used > 80:
        return HealthStatus.DEGRADED, f"Disk {percent_used:.1f}% full"
    return HealthStatus.HEALTHY, f"Disk {percent_used:.1f}% used"

health.register_check("database", check_database)
health.register_check("redis", check_redis)
health.register_check("disk", check_disk_space)

# API endpoint
@app.get("/health")
def health_check():
    return health.run_diagnostics()
```

---

## 7. TESTING STRATEGY (Quality Assurance)

### `[TDD]` Test-Driven Development
**RED → GREEN → REFACTOR. TESTS BEFORE IMPLEMENTATION.**

```python
# Step 1: Write failing test (RED)
def test_calculate_discount_for_gold_member():
    calculator = DiscountCalculator()
    discount = calculator.calculate("gold", 100.0)
    assert discount == 20.0

# Step 2: Write minimum code to pass (GREEN)
class DiscountCalculator:
    def calculate(self, membership: str, amount: float) -> float:
        if membership == "gold":
            return amount * 0.20
        return 0.0

# Step 3: Refactor while keeping tests green
class DiscountCalculator:
    RATES = {"gold": 0.20, "silver": 0.10, "bronze": 0.05}
    
    def calculate(self, membership: str, amount: float) -> float:
        rate = self.RATES.get(membership, 0.0)
        return amount * rate
```

---

### `[COV]` Code Coverage
**MINIMUM 80% COVERAGE FOR CORE LOGIC.**

```bash
# pytest with coverage
pip install pytest pytest-cov

pytest --cov=src --cov-report=html --cov-report=term
```

**Coverage Guidelines:**
- Core business logic: **90-100%**
- Application services: **80-90%**
- Infrastructure/adapters: **60-80%**
- UI/presentation: **50-70%**

---

### `[MUT]` Mutation Testing
**VERIFY THAT TESTS ACTUALLY TEST.**

Mutation testing changes your code and checks if tests catch the changes.

```bash
# Install mutmut
pip install mutmut

# Run mutation tests
mutmut run

# Show results
mutmut results
mutmut show
```

**Example:**
```python
# Original code
def is_adult(age: int) -> bool:
    return age >= 18

# Mutant 1: Changed >= to >
def is_adult(age: int) -> bool:
    return age > 18  # Should fail test for age=18

# Mutant 2: Changed 18 to 17
def is_adult(age: int) -> bool:
    return age >= 17  # Should fail boundary test
```

---

### `[UNIT]` Unit Tests
**ISOLATED TESTS FOR INDIVIDUAL COMPONENTS.**

```python
import pytest
from unittest.mock import Mock, patch

class TestUserService:
    def setup_method(self):
        self.user_repo = Mock(spec=UserRepository)
        self.email_service = Mock(spec=EmailService)
        self.service = UserService(self.user_repo, self.email_service)
    
    def test_create_user_success(self):
        # Arrange
        user = User(email="test@example.com", name="Test User")
        self.user_repo.save.return_value = user
        
        # Act
        result = self.service.create_user("test@example.com", "Test User")
        
        # Assert
        assert result.email == "test@example.com"
        self.user_repo.save.assert_called_once()
        self.email_service.send_welcome.assert_called_once_with(user)
    
    def test_create_user_duplicate_email(self):
        # Arrange
        self.user_repo.find_by_email.return_value = User(...)
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Email already exists"):
            self.service.create_user("test@example.com", "Test User")
```

---

### `[INTEGRATION]` Integration Tests
**TEST COMPONENT INTERACTIONS.**

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session():
    # Create test database
    engine = create_engine("postgresql://test:test@localhost/test_db")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Setup schema
    Base.metadata.create_all(engine)
    
    yield session
    
    # Teardown
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

def test_user_repository_integration(db_session):
    # Test with real database
    repo = PostgreSQLUserRepository(db_session)
    
    # Create user
    user = User(email="integration@test.com", name="Integration Test")
    saved_user = repo.save(user)
    
    # Verify persistence
    found_user = repo.find_by_id(saved_user.id)
    assert found_user.email == "integration@test.com"
    
    # Verify query
    found_by_email = repo.find_by_email("integration@test.com")
    assert found_by_email.id == saved_user.id
```

---

### `[E2E]` End-to-End Tests
**TEST ENTIRE USER WORKFLOWS.**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_user_registration_flow(browser):
    # Navigate to registration page
    browser.get("http://localhost:8000/register")
    
    # Fill form
    browser.find_element(By.ID, "email").send_keys("e2e@test.com")
    browser.find_element(By.ID, "name").send_keys("E2E Test")
    browser.find_element(By.ID, "password").send_keys("SecurePass123")
    
    # Submit
    browser.find_element(By.ID, "submit").click()
    
    # Verify redirect to dashboard
    assert "dashboard" in browser.current_url
    
    # Verify welcome message
    welcome = browser.find_element(By.CLASS_NAME, "welcome-message")
    assert "Welcome, E2E Test" in welcome.text
```

---

## 8. SECURITY STANDARDS (Defense in Depth)

### `[AUTH]` Authentication & Authorization

```python
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import jwt

class AuthService:
    SECRET_KEY = "your-secret-key-from-env"
    ALGORITHM = "HS256"
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hash(password)
    
    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.verify(plain, hashed)
    
    @staticmethod
    def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
        """Generate JWT token"""
        if expires_delta is None:
            expires_delta = timedelta(hours=24)
        
        expire = datetime.utcnow() + expires_delta
        payload = {
            "user_id": user_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                AuthService.SECRET_KEY,
                algorithms=[AuthService.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

# Role-Based Access Control
class Permission(Enum):
    READ_USER = "read:user"
    WRITE_USER = "write:user"
    DELETE_USER = "delete:user"
    ADMIN = "admin"

class Role:
    def __init__(self, name: str, permissions: List[Permission]):
        self.name = name
        self.permissions = set(permissions)
    
    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions or Permission.ADMIN in self.permissions

# Roles
ROLES = {
    "admin": Role("admin", [Permission.ADMIN]),
    "user": Role("user", [Permission.READ_USER, Permission.WRITE_USER]),
    "guest": Role("guest", [Permission.READ_USER])
}

def require_permission(permission: Permission):
    """Decorator for permission checking"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if not current_user.role.has_permission(permission):
                raise PermissionDeniedError(func.__name__, permission.value)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_permission(Permission.DELETE_USER)
def delete_user(user_id: int):
    # Only users with delete permission can execute
    pass
```

---

### `[OWASP]` OWASP Top 10 Protection

**1. Injection Prevention**
```python
# ❌ SQL Injection vulnerability
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ Parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))

# ❌ Command Injection
os.system(f"ping {user_input}")

# ✅ Safe execution
import subprocess
subprocess.run(["ping", "-c", "1", user_input], check=True)
```

**2. XSS Prevention**
```python
from html import escape

# ✅ Escape user input in HTML
def render_comment(comment: str) -> str:
    return f"<p>{escape(comment)}</p>"

# Use Content Security Policy
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = \
        "default-src 'self'; script-src 'self' 'unsafe-inline'"
    return response
```

**3. CSRF Protection**
```python
from secrets import token_urlsafe

class CSRFProtection:
    @staticmethod
    def generate_token() -> str:
        return token_urlsafe(32)
    
    @staticmethod
    def validate_token(session_token: str, request_token: str) -> bool:
        return session_token == request_token

# In form
@app.get("/form")
def show_form():
    csrf_token = CSRFProtection.generate_token()
    session['csrf_token'] = csrf_token
    return render_template("form.html", csrf_token=csrf_token)

# Validate on submission
@app.post("/submit")
def handle_submit():
    if not CSRFProtection.validate_token(
        session.get('csrf_token'),
        request.form.get('csrf_token')
    ):
        raise SecurityError("Invalid CSRF token")
```

**4. Secure Data Storage**
```python
from cryptography.fernet import Fernet
import os

class DataEncryption:
    def __init__(self):
        # Load key from environment, not code
        key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted: bytes) -> str:
        return self.cipher.decrypt(encrypted).decode()

# Store sensitive data encrypted
class User:
    def set_ssn(self, ssn: str):
        encryption = DataEncryption()
        self.ssn_encrypted = encryption.encrypt(ssn)
    
    def get_ssn(self) -> str:
        encryption = DataEncryption()
        return encryption.decrypt(self.ssn_encrypted)
```

---

### `[SECRETS]` Secret Management

```python
import os
from typing import Optional

class Config:
    """Centralized configuration from environment"""
    
    @staticmethod
    def get_required(key: str) -> str:
        """Get required environment variable"""
        value = os.getenv(key)
        if value is None:
            raise ConfigurationError(f"Missing required config: {key}")
        return value
    
    @staticmethod
    def get_optional(key: str, default: str = None) -> Optional[str]:
        """Get optional environment variable"""
        return os.getenv(key, default)
    
    # Database
    DATABASE_URL = get_required.__func__("DATABASE_URL")
    
    # Security
    SECRET_KEY = get_required.__func__("SECRET_KEY")
    ENCRYPTION_KEY = get_required.__func__("ENCRYPTION_KEY")
    
    # External APIs
    STRIPE_API_KEY = get_required.__func__("STRIPE_API_KEY")
    
    # Features
    DEBUG_MODE = get_optional.__func__("DEBUG", "false").lower() == "true"

# ❌ NEVER commit secrets to code
API_KEY = "sk_live_abc123..."  # ❌ WRONG

# ✅ Use environment variables
API_KEY = os.getenv("STRIPE_API_KEY")  # ✅ CORRECT

# Use .env for local development (add to .gitignore)
# Use secret managers for production (AWS Secrets Manager, Vault, etc.)
```

---

## 9. PERFORMANCE ENGINEERING

### `[PERF]` Performance Budgets

```python
from functools import wraps
import time
from typing import Callable

def performance_monitor(max_duration_ms: float):
    """Decorator to monitor function execution time"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            
            if duration > max_duration_ms:
                logger.warning(
                    f"Performance budget exceeded: {func.__name__} "
                    f"took {duration:.2f}ms (budget: {max_duration_ms}ms)"
                )
            
            return result
        return wrapper
    return decorator

# Usage
@performance_monitor(max_duration_ms=100)
def fetch_user_data(user_id: int) -> User:
    # Should complete in < 100ms
    pass
```

**Performance Targets:**
- API Response Time (P95): < 200ms
- Database Query: < 50ms
- Cache Hit: < 10ms
- Page Load (First Contentful Paint): < 1.5s

---

### `[CACHE]` Caching Strategy

```python
from functools import lru_cache
import redis
import pickle
from typing import Optional, Callable

class CacheManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    def get(self, key: str) -> Optional[any]:
        """Get value from cache"""
        data = self.redis.get(key)
        return pickle.loads(data) if data else None
    
    def set(self, key: str, value: any, ttl: int = None):
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        self.redis.setex(key, ttl, pickle.dumps(value))
    
    def delete(self, key: str):
        """Invalidate cache entry"""
        self.redis.delete(key)
    
    def cached(self, key_prefix: str, ttl: int = None):
        """Decorator for caching function results"""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from arguments
                cache_key = f"{key_prefix}:{str(args)}:{str(kwargs)}"
                
                # Try cache first
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # Compute and cache
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            return wrapper
        return decorator

# Usage
cache = CacheManager(redis.Redis())

@cache.cached("user", ttl=600)
def get_user(user_id: int) -> User:
    # Expensive database query
    return db.query(User).filter_by(id=user_id).first()

# In-memory cache for pure functions
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

---

### `[N+1]` Avoiding N+1 Queries

```python
# ❌ N+1 Query Problem
def get_users_with_orders():
    users = db.query(User).all()  # 1 query
    for user in users:
        user.orders = db.query(Order).filter_by(user_id=user.id).all()  # N queries
    return users

# ✅ Solution: Eager Loading
def get_users_with_orders():
    # Single query with JOIN
    users = db.query(User).options(
        joinedload(User.orders)
    ).all()
    return users

# ✅ Alternative: Batch Loading
def get_users_with_orders():
    users = db.query(User).all()
    user_ids = [u.id for u in users]
    
    # Single query for all orders
    orders = db.query(Order).filter(Order.user_id.in_(user_ids)).all()
    
    # Group by user
    orders_by_user = {}
    for order in orders:
        orders_by_user.setdefault(order.user_id, []).append(order)
    
    for user in users:
        user.orders = orders_by_user.get(user.id, [])
    
    return users
```

---

### `[ASYNC]` Asynchronous Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

# Async I/O for concurrent operations
async def fetch_user_data(user_id: int) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/api/users/{user_id}") as response:
            data = await response.json()
            return User(**data)

async def fetch_multiple_users(user_ids: List[int]) -> List[User]:
    # Fetch all users concurrently
    tasks = [fetch_user_data(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)

# Background job processing
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def send_email_async(user_id: int, template: str):
    """Process email sending in background"""
    user = get_user(user_id)
    email_service.send(user.email, template)

# Usage
def create_user(data: dict):
    user = User(**data)
    db.save(user)
    
    # Send email asynchronously
    send_email_async.delay(user.id, "welcome")
    
    return user
```

---

## 10. DOCUMENTATION & MAINTAINABILITY

### `[DOC]` Documentation Standards

```python
from typing import List, Optional
from decimal import Decimal

class OrderService:
    """
    Service for managing customer orders.
    
    This service handles the complete order lifecycle including
    creation, validation, payment processing, and fulfillment.
    
    Attributes:
        order_repo: Repository for order persistence
        payment_service: External payment processing service
        inventory_service: Inventory management service
    
    Example:
        >>> service = OrderService(repo, payment, inventory)
        >>> order = service.create_order(user_id=1, items=[...])
        >>> result = service.process_payment(order.id)
    """
    
    def __init__(
        self,
        order_repo: OrderRepository,
        payment_service: PaymentService,
        inventory_service: InventoryService
    ):
        self.order_repo = order_repo
        self.payment_service = payment_service
        self.inventory_service = inventory_service
    
    def create_order(
        self,
        user_id: int,
        items: List[OrderItem],
        shipping_address: Address
    ) -> Order:
        """
        Create a new order for a user.
        
        Validates items, checks inventory, calculates totals,
        and persists the order in pending state.
        
        Args:
            user_id: The ID of the user placing the order
            items: List of items to order with quantities
            shipping_address: Delivery address for the order
        
        Returns:
            Created order with generated ID and calculated totals
        
        Raises:
            ValidationError: If items are invalid or out of stock
            UserNotFoundError: If user_id doesn't exist
        
        Example:
            >>> items = [OrderItem(product_id=1, quantity=2)]
            >>> address = Address(street="123 Main St", city="NYC")
            >>> order = service.create_order(
            ...     user_id=42,
            ...     items=items,
            ...     shipping_address=address
            ... )
            >>> print(order.total)
            Decimal('99.99')
        """
        # Validate user exists
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        
        # Validate inventory
        for item in items:
            if not self.inventory_service.is_available(item.product_id, item.quantity):
                raise ValidationError(f"Product {item.product_id} out of stock")
        
        # Calculate totals
        total = self._calculate_total(items)
        
        # Create order
        order = Order(
            user_id=user_id,
            items=items,
            shipping_address=shipping_address,
            total=total,
            status=OrderStatus.PENDING
        )
        
        return self.order_repo.save(order)
    
    def _calculate_total(self, items: List[OrderItem]) -> Decimal:
        """
        Calculate order total from items.
        
        Internal method - not part of public API.
        """
        return sum(item.price * item.quantity for item in items)
```

---

### `[README]` Project Documentation

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+

## Installation

\`\`\`bash
# Clone repository
git clone https://github.com/username/project.git
cd project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb project_db
alembic upgrade head
\`\`\`

## Configuration

Copy `.env.example` to `.env` and configure:

\`\`\`env
DATABASE_URL=postgresql://user:pass@localhost/project_db
SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379/0
\`\`\`

## Usage

\`\`\`bash
# Run development server
uvicorn main:app --reload

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
\`\`\`

## Project Structure

\`\`\`
project/
├── src/
│   ├── domain/          # Business entities
│   ├── application/     # Use cases
│   ├── infrastructure/  # External services
│   └── presentation/    # API endpoints
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
└── README.md
\`\`\`

## API Documentation

See [API.md](docs/API.md) or visit `/docs` when server is running.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE)
```

---

### `[ADR]` Architecture Decision Records

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to choose a database for our order management system. 
Requirements:
- ACID transactions for financial data
- Complex queries with joins
- Strong consistency
- Mature ecosystem

## Decision
We will use PostgreSQL as our primary database.

## Consequences

### Positive
- ACID compliance ensures data integrity
- Rich query capabilities with SQL
- JSON support for flexible schemas
- Excellent performance for our scale
- Strong community and tooling

### Negative
- More complex operations than NoSQL for simple CRUD
- Requires more careful schema design
- Vertical scaling limits (can be mitigated with read replicas)

## Alternatives Considered
- **MongoDB**: Rejected due to lack of ACID transactions
- **MySQL**: Considered, but PostgreSQL has better JSON support
- **DynamoDB**: Rejected due to vendor lock-in and query limitations
```

---

## 11. DEVOPS & DEPLOYMENT

### `[CI/CD]` Continuous Integration/Deployment

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run linting
        run: |
          flake8 src/
          mypy src/
      
      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:test@localhost/test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
      
      - name: Security scan
        run: |
          pip install bandit safety
          bandit -r src/
          safety check

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Your deployment script
          echo "Deploying to production"
```

---

### `[DOCKER]` Containerization

```dockerfile
# Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./src:/app/src
    restart: unless-stopped

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

---

### `[VERS]` Semantic Versioning

**Format: MAJOR.MINOR.PATCH**

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes

```
v1.0.0   Initial release
v1.0.1   Bug fix
v1.1.0   New feature (backward compatible)
v2.0.0   Breaking change
```

**Changelog Example:**
```markdown
# Changelog

## [2.0.0] - 2026-02-17

### Breaking Changes
- Changed user authentication from session to JWT tokens
- Removed deprecated `/api/v1/legacy` endpoints

### Added
- New payment processing with Stripe integration
- Real-time notifications via WebSocket

### Fixed
- Memory leak in background job processor
- Race condition in order creation

### Deprecated
- `/api/users/old` endpoint (use `/api/v2/users` instead)
```

---

## 12. CODE REVIEW CHECKLIST

### Pre-Commit Checklist

```markdown
## Code Quality
- [ ] Follows naming conventions (PascalCase, snake_case)
- [ ] No code duplication (DRY principle)
- [ ] Functions are small and focused (< 20 lines)
- [ ] No magic numbers (use named constants)
- [ ] Comments explain "why", not "what"

## Architecture
- [ ] Follows SOLID principles
- [ ] Dependencies point inward (Clean Architecture)
- [ ] No circular dependencies
- [ ] Proper separation of concerns

## Testing
- [ ] Unit tests added/updated
- [ ] Tests cover edge cases
- [ ] Code coverage > 80% for new code
- [ ] Integration tests if touching data layer
- [ ] All tests pass locally

## Security
- [ ] No hardcoded secrets or passwords
- [ ] Input validation on all external data
- [ ] SQL queries use parameterization
- [ ] XSS/CSRF protections in place
- [ ] Proper error handling (no sensitive data in errors)

## Performance
- [ ] No N+1 queries
- [ ] Proper indexing for database queries
- [ ] Caching used where appropriate
- [ ] No blocking operations in async code
- [ ] Resource cleanup (file handles, connections)

## Documentation
- [ ] Public APIs have docstrings
- [ ] README updated if needed
- [ ] ADR created for architectural decisions
- [ ] API documentation updated

## Git Hygiene
- [ ] Commits are atomic and well-described
- [ ] Branch name follows convention (feature/*, bugfix/*)
- [ ] No merge commits (rebase preferred)
- [ ] All TODOs have tickets
```

---

## APPENDIX A: Quick Reference Card

```
┌────────────────────────────────────────────────────────────────┐
│                    ASGUARD01 QUICK REFERENCE                   │
└────────────────────────────────────────────────────────────────┘

CODE PRINCIPLES          SOLID PRINCIPLES         PATTERNS
──────────────          ────────────────         ────────
[DRY]   No duplication  [S] Single Responsibility [FACTORY]  Creation
[KISS]  Keep it simple  [O] Open/Closed          [STRATEGY] Algorithms
[YAGNI] No speculation  [L] Liskov Substitution  [REPOSITORY] Data
[NAME]  Clear naming    [I] Interface Segregation [DECORATOR] Wrappers
[UNIT]  One purpose     [D] Dependency Inversion [OBSERVER] Events
[INFO]  Self-documenting

ARCHITECTURE            RESILIENCE                SECURITY
────────────           ──────────                ────────
[LAYER] Core is center  [STATE]  External state   [AUTH] Authentication
[DIR]   Inward deps     [RESUME] Auto-recovery   [OWASP] Top 10
[DB/UI] Plugins         [ATOM]   Atomic writes   [SECRETS] No hardcode
[DTO]   Clean boundaries [IDEM]  Idempotent ops  [VALID] Input checks
                        [HEALTH] Self-diagnosis

TESTING                 PERFORMANCE              DEVOPS
───────                ───────────              ──────
[TDD]   Test first     [PERF]  Budgets         [CI/CD] Automation
[COV]   80% minimum    [CACHE] Smart caching   [DOCKER] Containers
[MUT]   Kill mutations  [N+1]   Batch queries   [VERS] Semver
[E2E]   Full workflows  [ASYNC] Non-blocking    [MONITOR] Observability
```

---

## APPENDIX B: Language-Specific Examples

### Python Best Practices
```python
# Use context managers
with open('file.txt') as f:
    data = f.read()

# Use comprehensions (but keep readable)
squares = [x**2 for x in range(10)]

# Use generators for large datasets
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()

# Use dataclasses
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    
    def distance(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
```

### TypeScript Best Practices
```typescript
// Use strict types
interface User {
  id: number;
  email: string;
  name: string;
}

// Use generics
function identity<T>(arg: T): T {
  return arg;
}

// Use readonly
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// Use discriminated unions
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: string };

function handleResult<T>(result: Result<T>): void {
  if (result.success) {
    console.log(result.data);
  } else {
    console.error(result.error);
  }
}
```

---

## CONCLUSION

This guide represents battle-tested principles for building robust, maintainable software systems. The standards outlined here are not theoretical—they emerge from decades of collective experience in software engineering.

### Remember:
1. **Principles over patterns**: Understand the "why" behind each rule
2. **Context matters**: Adapt guidelines to your specific needs
3. **Pragmatism wins**: Perfect is the enemy of good
4. **Continuous improvement**: Review and update these standards regularly

### The ASGUARD01 Philosophy:
> "Write code that your future self will thank you for."

**Stability over speed. Clarity over brevity. Resilience over features.**

---

**Version:** 3.0  
**Last Updated:** February 17, 2026  
**Maintained by:** ASGUARD01 Engineering Team  
**License:** MIT

For questions, suggestions, or contributions, please open an issue or submit a pull request.

```
END OF DOCUMENT
```
