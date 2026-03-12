# ASGUARD01 — СТАНДАРТЫ СИСТЕМЫ: ПОЛНОЕ РУКОВОДСТВО АРХИТЕКТОРА
**Версия 3.0 · God-Tier Edition**
*(C) Copyright 1985–2026 Asguard01 Corp.*

> *«Любой дурак может написать код, понятный компьютеру.*
> *Хорошие программисты пишут код, понятный людям.»*
> — Мартин Фаулер

---

## СОДЕРЖАНИЕ

1. [Целостность кода — Фундамент](#1-целостность-кода--фундамент)
2. [Соглашения об именовании и читаемость](#2-соглашения-об-именовании-и-читаемость)
3. [Принципы SOLID](#3-принципы-solid)
4. [Чистая архитектура и слоистая топология](#4-чистая-архитектура-и-слоистая-топология)
5. [Гексагональная архитектура (Порты и Адаптеры)](#5-гексагональная-архитектура-порты-и-адаптеры)
6. [Паттерны GoF — Порождающие](#6-паттерны-gof--порождающие)
7. [Паттерны GoF — Структурные](#7-паттерны-gof--структурные)
8. [Паттерны GoF — Поведенческие](#8-паттерны-gof--поведенческие)
9. [Корпоративные и архитектурные паттерны](#9-корпоративные-и-архитектурные-паттерны)
10. [Паттерны распределённых систем](#10-паттерны-распределённых-систем)
11. [CQRS и Event Sourcing](#11-cqrs-и-event-sourcing)
12. [Архитектура микросервисов](#12-архитектура-микросервисов)
13. [Событийно-ориентированная архитектура (EDA)](#13-событийно-ориентированная-архитектура-eda)
14. [Стандарты проектирования API](#14-стандарты-проектирования-api)
15. [Моделирование данных и персистентность](#15-моделирование-данных-и-персистентность)
16. [Отказоустойчивость и надёжность](#16-отказоустойчивость-и-надёжность)
17. [Стандарты безопасности](#17-стандарты-безопасности)
18. [Наблюдаемость: Логи, Метрики, Трассировки](#18-наблюдаемость-логи-метрики-трассировки)
19. [Стратегия тестирования](#19-стратегия-тестирования)
20. [Инжиниринг производительности](#20-инжиниринг-производительности)
21. [CI/CD и DevOps пайплайн](#21-cicd-и-devops-пайплайн)
22. [Инфраструктура как код (IaC)](#22-инфраструктура-как-код-iac)
23. [Предметно-ориентированное проектирование (DDD)](#23-предметно-ориентированное-проектирование-ddd)
24. [Конкурентность и асинхронные паттерны](#24-конкурентность-и-асинхронные-паттерны)
25. [Стандарты документации](#25-стандарты-документации)
26. [Командный процесс и культура кода](#26-командный-процесс-и-культура-кода)
27. [Антипаттерны — чего избегать](#27-антипаттерны--чего-избегать)
28. [Чеклисты — перед деплоем и ревью архитектуры](#28-чеклисты--перед-деплоем-и-ревью-архитектуры)

---

## 1. Целостность кода — Фундамент

Это не рекомендации. Это законы.

### [DRY] — Не повторяйся

Каждый фрагмент знания должен иметь **единственное, однозначное, авторитетное представление** в системе.

**ПЛОХО:**
```python
# Регистрация пользователя
user_age = int(input_data["age"])
if user_age < 0 or user_age > 150:
    raise ValueError("Invalid age")

# Обновление профиля
user_age = int(profile_data["age"])
if user_age < 0 or user_age > 150:
    raise ValueError("Invalid age")
```

**ХОРОШО:**
```python
def validate_age(age: int) -> int:
    """Проверяет допустимый диапазон возраста. Единственный источник истины."""
    if not (0 <= age <= 150):
        raise InvalidAgeError(f"Возраст {age} вне допустимого диапазона [0, 150]")
    return age

# Регистрация
validate_age(int(input_data["age"]))

# Обновление профиля
validate_age(int(profile_data["age"]))
```

> Нарушение DRY — это не просто дублирование *текста*, это дублирование *намерения* и *логики*. Если при изменении одного места нужно искать другое — это нарушение DRY.

---

### [KISS] — Будь проще

Сложность — враг. **Решай задачу, которая стоит перед тобой**, а не воображаемую.

**Метрики сложности для контроля:**
- Цикломатическая сложность функции: **максимум 10**
- Длина функции: **максимум 40 строк**
- Глубина вложенности: **максимум 3 уровня**
- Количество параметров: **максимум 4** (свыше — объект параметров)

**ПЛОХО:**
```python
def process(data, mode, flag1, flag2, flag3, extra=None, callback=None):
    if mode == 1:
        if flag1:
            if flag2 and not flag3:
                ...
```

**ХОРОШО:**
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

### [YAGNI] — Тебе это не понадобится

Не строй функции на основе предположений. **Каждая строка кода — это обязательство.** Неиспользуемый код — это технический долг без отдачи.

Правила:
- Никаких `# TODO: реализовать позже` без тикета
- Никаких «перспективных» абстракций без конкретного сценария использования
- Никакого настраиваемого поведения, если у него только одно значение
- Никаких обобщённых фреймворков для задачи с одним клиентом

---

### [UNIT] — Единственная ответственность на уровне функции

Функция, которая делает одно дело, легче:
- именовать
- тестировать
- переиспользовать
- отлаживать

**Сигнал нарушения UNIT:** если имя функции содержит «и», «или», «также», «затем» — раздели её.

---

### [INFO] — Комментарии объясняют *почему*, а не *что*

```python
# ПЛОХО: объясняет ЧТО (код уже это показывает)
# увеличить счётчик на 1
counter += 1

# ХОРОШО: объясняет ПОЧЕМУ
# Пропускаем нулевой индекс: заголовок протокола занимает слот 0, данные начинаются с 1
for i in range(1, len(packets)):
    ...

# ХОРОШО: объясняет неочевидное бизнес-правило
# Льготный период 3 дня определён в договоре §4.2
if days_overdue <= 3:
    apply_soft_warning(account)
```

---

## 2. Соглашения об именовании и читаемость

Имена — это основной интерфейс между программистом и читателем.

### Универсальные правила

| Сущность | Соглашение | Пример |
|----------|-----------|--------|
| Переменная | существительное, описательное | `user_invoice_count` |
| Булево | префикс is/has/can/should | `is_active`, `has_permission` |
| Функция | глагол + существительное | `calculate_tax()`, `fetch_user()` |
| Класс | PascalCase, существительное | `InvoiceRepository` |
| Константа | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Интерфейс | IEntity или EntityInterface | `IPaymentGateway` |
| Абстракция | префикс Abstract или суффикс -Base | `AbstractProcessor` |
| Перечисление | PascalCase, значения UPPER | `OrderStatus.PENDING` |

### Антипаттерны именования

```python
# ЗАПРЕЩЕНО — бессмысленные имена
def do_stuff(d, x, temp, data2):
    ...

# ЗАПРЕЩЕНО — вводящие в заблуждение имена
def get_user():
    user.delete()  # "get" подразумевает только чтение!

# ЗАПРЕЩЕНО — кодирование типа в имени (венгерская нотация)
strUserName = "Иван"  # тип — в аннотации, не в имени
intCount = 5

# ПРАВИЛЬНО
def deactivate_expired_subscriptions(cutoff_date: date) -> int:
    ...
```

### Единый язык (Ubiquitous Language)

Все имена в коде, базе данных, API и документации должны использовать **один и тот же предметный словарь**. Если бизнес говорит «Счёт-фактура», код пишет `Invoice` — не `Bill`, не `Receipt`, не `Document`.

Это напрямую связано с [Предметно-ориентированным проектированием](#23-предметно-ориентированное-проектирование-ddd).

---

## 3. Принципы SOLID

### [S] Принцип единственной ответственности

Класс должен иметь **одну и только одну причину для изменения**.

**ПЛОХО — UserService делает слишком много:**
```python
class UserService:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...    # Забота об email
    def generate_pdf_report(self, user): ...  # Забота об отчётах
    def log_user_activity(self, user): ...    # Забота о логировании
```

**ХОРОШО — каждый класс владеет одной зоной ответственности:**
```python
class UserService:
    def create_user(self, data: UserCreateDTO) -> User: ...

class UserNotificationService:
    def send_welcome_email(self, user: User) -> None: ...

class UserReportService:
    def generate_pdf_report(self, user: User) -> PDF: ...
```

---

### [O] Принцип открытости/закрытости

Программные сущности должны быть **открыты для расширения, закрыты для изменения**.
Новое поведение добавляется написанием *нового* кода, а не изменением *существующего*.

**ПЛОХО — каждый новый тип оплаты требует изменения ядра:**
```python
def process_payment(payment):
    if payment.type == "credit_card":
        charge_credit_card(payment)
    elif payment.type == "paypal":
        charge_paypal(payment)
    elif payment.type == "crypto":  # И снова правим!
        charge_crypto(payment)
```

**ХОРОШО — новые типы расширяются через новые классы:**
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, payment: Payment) -> PaymentResult: ...

class CreditCardProcessor(PaymentProcessor):
    def process(self, payment: Payment) -> PaymentResult: ...

class PayPalProcessor(PaymentProcessor):
    def process(self, payment: Payment) -> PaymentResult: ...

# Добавление крипто = новый класс, ноль изменений в существующем коде
class CryptoProcessor(PaymentProcessor):
    def process(self, payment: Payment) -> PaymentResult: ...
```

---

### [L] Принцип подстановки Лисков

Если `S` является подтипом `T`, то объекты типа `T` могут быть заменены объектами типа `S` **без нарушения корректности программы**.

**Тест:** можно ли использовать подкласс везде, где используется родительский класс, не ломая ничего?

**ПЛОХО:**
```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        self.height = w  # Нарушает LSP — неожиданный побочный эффект!
```

**ХОРОШО:** Используй общую абстракцию `Shape` вместо наследования:
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

### [I] Принцип разделения интерфейсов

**Ни один клиент не должен зависеть от методов, которые он не использует.**
Предпочитай много маленьких, специализированных интерфейсов одному большому универсальному.

**ПЛОХО — раздутый интерфейс:**
```python
class IWorker(ABC):
    @abstractmethod def work(self): ...
    @abstractmethod def eat(self): ...   # Роботы не едят!
    @abstractmethod def sleep(self): ...
```

**ХОРОШО — гранулярные интерфейсы:**
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

### [D] Принцип инверсии зависимостей

- Модули высокого уровня не должны зависеть от модулей низкого уровня. **Оба должны зависеть от абстракций.**
- Абстракции не должны зависеть от деталей. **Детали зависят от абстракций.**

**ПЛОХО:**
```python
class OrderService:
    def __init__(self):
        self.db = PostgreSQLDatabase()      # Жёсткая зависимость от конкретики
        self.mailer = SendGridMailer()      # Жёсткая зависимость от третьей стороны
```

**ХОРОШО:**
```python
class OrderService:
    def __init__(
        self,
        order_repo: IOrderRepository,       # Абстракция
        notification_service: INotifier,    # Абстракция
    ):
        self._repo = order_repo
        self._notifier = notification_service
```

> Это делает тестирование тривиальным — подставляй моки. Деплой становится гибким — замени PostgreSQL на MongoDB, написав новый адаптер.

---

## 4. Чистая архитектура и слоистая топология

Чистая архитектура (Роберт Мартин) организует код в концентрические слои. **Правило зависимостей: зависимости в исходном коде могут указывать только внутрь.**

```
┌─────────────────────────────────────────────────────────┐
│               ФРЕЙМВОРКИ И ДРАЙВЕРЫ                     │
│        (Web, БД, UI, Внешние API, CLI)                  │
│   ┌───────────────────────────────────────────────┐     │
│   │            ИНТЕРФЕЙСНЫЕ АДАПТЕРЫ              │     │
│   │  (Контроллеры, Презентеры, Шлюзы, DTO)       │     │
│   │   ┌─────────────────────────────────────┐     │     │
│   │   │           СЛОЙ ПРИЛОЖЕНИЯ            │     │     │
│   │   │  (Use Cases / Сервисы приложения)   │     │     │
│   │   │   ┌─────────────────────────┐        │     │     │
│   │   │   │    ДОМЕН / СУЩНОСТИ     │        │     │     │
│   │   │   │  (Бизнес-правила, Ядро) │        │     │     │
│   │   │   └─────────────────────────┘        │     │     │
│   │   └─────────────────────────────────────┘     │     │
│   └───────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
                    Зависимости →  ВНУТРЬ
```

### Ответственности слоёв

| Слой | Что здесь живёт | Чего НЕ должен знать |
|------|----------------|----------------------|
| **Домен/Сущности** | Бизнес-правила, доменные модели, объекты-значения, доменные события | Фреймворки, БД, HTTP, всё внешнее |
| **Приложение** | Use cases, сервисы приложения, обработчики команд/запросов | Фреймворки, драйверы БД, HTTP |
| **Интерфейсные адаптеры** | REST контроллеры, GraphQL резолверы, CLI, маперы DTO | Логика бизнес-правил |
| **Фреймворки и драйверы** | Настройка Django/FastAPI, конфигурация ORM, брокеры сообщений | Бизнес-правила |

### Правило на практике

```
domain/
│   entities/
│       order.py          ← Чистый Python, ноль импортов из внешних слоёв
│       user.py
│   value_objects/
│       money.py
│       email.py
│   repositories/         ← Интерфейсы (абстракции), не реализации
│       i_order_repo.py
│
application/
│   use_cases/
│       place_order.py    ← Оркестрирует домен, вызывает интерфейс репозитория
│       cancel_order.py
│   dtos/
│       order_dto.py
│
infrastructure/           ← Реализует интерфейсы домена
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

### Правило DTO (Data Transfer Object)

Межслойная коммуникация использует **только DTO** — простые структуры данных без поведения. Никогда не передавай доменные сущности через границы слоёв.

```python
# DTO — только данные, никакой логики
@dataclass(frozen=True)
class PlaceOrderDTO:
    user_id: UUID
    items: list[OrderItemDTO]
    shipping_address: AddressDTO

# Use Case принимает DTO, возвращает DTO
class PlaceOrderUseCase:
    def execute(self, dto: PlaceOrderDTO) -> OrderConfirmationDTO:
        order = Order.create(dto)            # Доменная логика
        self._repo.save(order)
        self._events.publish(OrderPlacedEvent(order.id))
        return OrderConfirmationDTO.from_order(order)
```

---

## 5. Гексагональная архитектура (Порты и Адаптеры)

Предложена Аластером Кокберном. Рассматривает приложение как **шестиугольник** с «портами» (интерфейсами) и «адаптерами» (реализациями).

```
               ┌──────────────┐
  HTTP API ───▶│   REST       │
               │  Адаптер     │
               └──────┬───────┘
                       │ (первичный/ведущий порт)
         ┌─────────────▼──────────────┐
         │                            │
REST ──▶ │      ЯДРО ПРИЛОЖЕНИЯ       │ ──▶ Адаптер БД ──▶ PostgreSQL
gRPC ──▶ │                            │ ──▶ Адаптер Email ──▶ SendGrid
CLI  ──▶ │  Бизнес-логика живёт здесь │ ──▶ Адаптер Очереди ──▶ RabbitMQ
         │                            │
         └────────────────────────────┘
                (вторичные/ведомые порты)
```

**Первичные порты** (ведущие): как внешние акторы вызывают приложение (HTTP, gRPC, CLI)
**Вторичные порты** (ведомые): как приложение вызывает внешние системы (БД, email, очереди)

**Преимущество:** ядро можно тестировать полностью изолированно от всей инфраструктуры.

```python
# ПОРТ (интерфейс, определённый в ядре)
class IPaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: Money, token: str) -> ChargeResult: ...

# АДАПТЕР (инфраструктура, реализует порт)
class StripePaymentAdapter(IPaymentGateway):
    def charge(self, amount: Money, token: str) -> ChargeResult:
        response = stripe.PaymentIntent.create(
            amount=amount.in_cents(),
            currency=amount.currency.lower(),
            payment_method=token,
        )
        return ChargeResult.from_stripe(response)

# ФЕЙКОВЫЙ АДАПТЕР для тестов
class FakePaymentAdapter(IPaymentGateway):
    def charge(self, amount: Money, token: str) -> ChargeResult:
        return ChargeResult(success=True, transaction_id="fake-txn-001")
```

---

## 6. Паттерны GoF — Порождающие

23 паттерна Банды Четырёх, организованных по категориям. Это проверенные решения повторяющихся задач.

### Фабричный метод (Factory Method)

Определяет интерфейс для создания объекта, но позволяет подклассам решать, какой класс инстанциировать.

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

# Регистрация
NotificationFactory.register("email", EmailNotification)
NotificationFactory.register("sms", SMSNotification)

# Использование — нулевая связность с конкретными классами
notifier = NotificationFactory.create("email")
notifier.send("Ваш заказ готов")
```

---

### Абстрактная фабрика (Abstract Factory)

Создаёт семейства связанных объектов без указания их конкретных классов.

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

### Строитель (Builder)

Конструирует сложные объекты пошагово.

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
        return self  # Текучий интерфейс

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

# Использование текучего строителя
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

### Одиночка (Singleton)

Гарантирует, что у класса есть только один экземпляр. **Используй редко** — часто признак глобального состояния.

```python
class ApplicationConfig:
    _instance: "ApplicationConfig | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "ApplicationConfig":
        if cls._instance is None:
            with cls._lock:  # Потокобезопасная двойная проверка
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._load()
        return cls._instance

    def _load(self) -> None:
        self._data = load_from_env()

    def get(self, key: str) -> str:
        return self._data[key]
```

> **Предупреждение:** Singleton часто является антипаттерном. Предпочитай инъекцию зависимостей с единственным экземпляром, управляемым DI-контейнером.

---

### Прототип (Prototype)

Клонирует объекты вместо создания с нуля.

```python
import copy

class DocumentTemplate:
    def __init__(self, title: str, sections: list[str]):
        self.title = title
        self.sections = sections
        self.metadata = {"created_at": datetime.now()}

    def clone(self) -> "DocumentTemplate":
        return copy.deepcopy(self)

# Базовый шаблон создаётся один раз
invoice_template = DocumentTemplate(
    title="Счёт-фактура",
    sections=["заголовок", "позиции", "итоги", "подвал"]
)

# Каждый счёт — клон, независимо изменяемый
new_invoice = invoice_template.clone()
new_invoice.title = f"Счёт-фактура #{next_id()}"
```

---

## 7. Паттерны GoF — Структурные

### Адаптер (Adapter)

Преобразует интерфейс класса в другой интерфейс, ожидаемый клиентами.

```python
# Целевой интерфейс, который ожидает наша система
class ITemperatureSensor(ABC):
    @abstractmethod
    def get_celsius(self) -> float: ...

# Устаревший сторонний датчик (возвращает Фаренгейт, другое имя метода)
class LegacyFahrenheitSensor:
    def read_temperature(self) -> float:
        return 98.6  # Фаренгейт

# Адаптер устраняет несовместимость
class FahrenheitSensorAdapter(ITemperatureSensor):
    def __init__(self, sensor: LegacyFahrenheitSensor):
        self._sensor = sensor

    def get_celsius(self) -> float:
        fahrenheit = self._sensor.read_temperature()
        return (fahrenheit - 32) * 5 / 9
```

---

### Декоратор (Decorator)

Динамически добавляет обязанности объекту.

```python
class IDataFetcher(ABC):
    @abstractmethod
    def fetch(self, url: str) -> str: ...

class HttpDataFetcher(IDataFetcher):
    def fetch(self, url: str) -> str:
        return requests.get(url).text

# Декоратор: добавляет кэширование, не трогая HttpDataFetcher
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

# Декоратор: добавляет логирование
class LoggingDecorator(IDataFetcher):
    def __init__(self, fetcher: IDataFetcher, logger: ILogger):
        self._fetcher = fetcher
        self._logger = logger

    def fetch(self, url: str) -> str:
        self._logger.info(f"Загружаем: {url}")
        result = self._fetcher.fetch(url)
        self._logger.info(f"Загружено {len(result)} байт")
        return result

# Стек декораторов — композиция вместо наследования
fetcher = LoggingDecorator(
    CachingDecorator(
        HttpDataFetcher(),
        RedisCache()
    ),
    StructuredLogger()
)
```

---

### Компоновщик (Composite)

Компонует объекты в древовидные структуры для представления иерархий часть-целое.

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

# Клиент работает с файлами и директориями одинаково
root = Directory("root")
root.add(File("readme.md", 1024))
docs = Directory("docs")
docs.add(File("guide.pdf", 2048000))
root.add(docs)

print(root.size())  # Работает рекурсивно по всему дереву
```

---

### Фасад (Facade)

Предоставляет упрощённый интерфейс к сложной подсистеме.

```python
# Сложная подсистема
class VideoEncoder: ...
class AudioEncoder: ...
class MetadataExtractor: ...
class ThumbnailGenerator: ...
class StorageUploader: ...

# Фасад — единый простой интерфейс
class VideoProcessingFacade:
    def __init__(self):
        self._video_encoder = VideoEncoder()
        self._audio_encoder = AudioEncoder()
        self._metadata = MetadataExtractor()
        self._thumbnails = ThumbnailGenerator()
        self._uploader = StorageUploader()

    def process_and_upload(self, video_path: str) -> str:
        """Один метод скрывает весь пайплайн обработки."""
        video = self._video_encoder.encode(video_path)
        audio = self._audio_encoder.extract_and_encode(video_path)
        meta = self._metadata.extract(video_path)
        thumb = self._thumbnails.generate(video_path)
        return self._uploader.upload(video, audio, meta, thumb)
```

---

### Заместитель (Proxy)

Предоставляет суррогат или замену для другого объекта, чтобы контролировать доступ к нему.

```python
class IExpensiveService(ABC):
    @abstractmethod
    def compute(self, data: str) -> str: ...

class ExpensiveService(IExpensiveService):
    def compute(self, data: str) -> str:
        time.sleep(5)  # Дорогая операция!
        return data.upper()

class LazyLoadingProxy(IExpensiveService):
    """Сервис создаётся только при первом обращении."""
    def __init__(self):
        self._service: ExpensiveService | None = None

    def compute(self, data: str) -> str:
        if self._service is None:
            self._service = ExpensiveService()
        return self._service.compute(data)
```

---

### Мост (Bridge)

Разделяет абстракцию и реализацию, чтобы они могли изменяться независимо.

```python
# Иерархия реализаций
class IRenderer(ABC):
    @abstractmethod
    def render_shape(self, shape_data: dict) -> None: ...

class OpenGLRenderer(IRenderer): ...
class VulkanRenderer(IRenderer): ...

# Иерархия абстракций — использует IRenderer, не зависит от конкретной реализации
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

### Приспособленец (Flyweight)

Использует разделение для эффективной поддержки большого количества мелких объектов.

```python
class CharacterStyle:
    """Разделяемый приспособленец — внутреннее состояние."""
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

# Документ с 1М символов разделяет лишь несколько объектов стиля
```

---

## 8. Паттерны GoF — Поведенческие

### Стратегия (Strategy)

Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.

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
        self._strategy = strategy  # Замена во время выполнения

    def process(self, data: list) -> list:
        return self._strategy.sort(data)
```

---

### Наблюдатель (Observer / Pub-Sub)

Определяет зависимость «один ко многим». При изменении состояния одного объекта все зависимые автоматически уведомляются.

```python
from typing import Callable

class EventBus:
    """Внутрипроцессная шина событий."""
    _subscribers: dict[str, list[Callable]] = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type: str, handler: Callable) -> None:
        cls._subscribers[event_type].append(handler)

    @classmethod
    def publish(cls, event_type: str, event: object) -> None:
        for handler in cls._subscribers.get(event_type, []):
            handler(event)

# Доменное событие
@dataclass
class OrderPlacedEvent:
    order_id: UUID
    user_id: UUID
    total: Money
    occurred_at: datetime = field(default_factory=datetime.now)

# Подписчики — полностью развязаны с созданием заказа
def send_confirmation_email(event: OrderPlacedEvent): ...
def update_inventory(event: OrderPlacedEvent): ...
def notify_warehouse(event: OrderPlacedEvent): ...

EventBus.subscribe("order.placed", send_confirmation_email)
EventBus.subscribe("order.placed", update_inventory)
EventBus.subscribe("order.placed", notify_warehouse)

# Издатель — ничего не знает о подписчиках
EventBus.publish("order.placed", OrderPlacedEvent(order_id=..., user_id=...))
```

---

### Команда (Command)

Инкапсулирует запрос как объект, позволяя параметризировать, ставить в очередь, логировать и отменять действия.

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

### Цепочка обязанностей (Chain of Responsibility)

Передаёт запрос по цепочке обработчиков. Каждый обработчик решает, обработать его или передать дальше.

```python
class RequestHandler(ABC):
    def __init__(self):
        self._next: RequestHandler | None = None

    def set_next(self, handler: "RequestHandler") -> "RequestHandler":
        self._next = handler
        return handler  # Текучее связывание

    def handle(self, request: Request) -> Response | None:
        if self._next:
            return self._next.handle(request)
        return None

class AuthenticationHandler(RequestHandler):
    def handle(self, request: Request) -> Response | None:
        if not request.has_valid_token():
            return Response(status=401, body="Не авторизован")
        return super().handle(request)

class RateLimitHandler(RequestHandler):
    def handle(self, request: Request) -> Response | None:
        if self._is_rate_limited(request.client_ip):
            return Response(status=429, body="Слишком много запросов")
        return super().handle(request)

class BusinessLogicHandler(RequestHandler):
    def handle(self, request: Request) -> Response | None:
        return process_business_logic(request)

# Построение цепочки
auth = AuthenticationHandler()
auth.set_next(RateLimitHandler()).set_next(BusinessLogicHandler())

response = auth.handle(incoming_request)
```

---

### Шаблонный метод (Template Method)

Определяет скелет алгоритма, оставляя некоторые шаги подклассам.

```python
class ReportGenerator(ABC):
    def generate(self) -> str:
        """Шаблонный метод — определяет скелет алгоритма."""
        data = self.fetch_data()
        processed = self.process_data(data)
        formatted = self.format_output(processed)
        return self.render(formatted)

    @abstractmethod
    def fetch_data(self) -> RawData: ...

    @abstractmethod
    def process_data(self, data: RawData) -> ProcessedData: ...

    def format_output(self, data: ProcessedData) -> FormattedData:
        """Реализация по умолчанию — можно переопределить."""
        return DefaultFormatter().format(data)

    @abstractmethod
    def render(self, data: FormattedData) -> str: ...

class PDFReportGenerator(ReportGenerator):
    def fetch_data(self): return self._db.query_sales()
    def process_data(self, data): return aggregate_by_month(data)
    def render(self, data): return PDFRenderer().render(data)
```

---

### Состояние (State)

Позволяет объекту менять своё поведение при изменении внутреннего состояния.

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
        raise InvalidTransitionError("Нельзя отправить неподтверждённый заказ")
    def cancel(self, order: "Order") -> None:
        order.set_state(CancelledState())

class ConfirmedState(IOrderState):
    def confirm(self, order: "Order") -> None:
        raise InvalidTransitionError("Заказ уже подтверждён")
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

### Итератор (Iterator)

Обеспечивает последовательный доступ к элементам коллекции без раскрытия её внутреннего устройства.

### Посредник (Mediator)

Определяет объект, инкапсулирующий взаимодействие множества объектов, снижая прямую связность.

### Хранитель (Memento)

Фиксирует и выносит за пределы объекта его внутреннее состояние, чтобы позже можно было восстановить объект — без нарушения инкапсуляции.

### Посетитель (Visitor)

Представляет операцию над элементами объектной структуры. Позволяет добавлять новые операции без изменения классов элементов.

### Интерпретатор (Interpreter)

Задаёт грамматику языка и предоставляет интерпретатор для работы с ней.

---

## 9. Корпоративные и архитектурные паттерны

### Паттерн «Репозиторий» (Repository)

Посредничает между доменом и слоем отображения данных. Предоставляет коллекционный интерфейс для доступа к доменным объектам.

```python
# Интерфейс в доменном слое
class IOrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    def find_by_user(self, user_id: UUID, status: OrderStatus | None = None) -> list[Order]: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def delete(self, order_id: UUID) -> None: ...

# Реализация в инфраструктурном слое
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

### Единица работы (Unit of Work)

Отслеживает объекты, затронутые бизнес-транзакцией, и координирует запись изменений.

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

# Использование — атомарная транзакция
def transfer_order(from_user_id: UUID, to_user_id: UUID, order_id: UUID):
    with UnitOfWork(get_session()) as uow:
        order = uow.orders.find_by_id(order_id)
        order.transfer_to(to_user_id)
        uow.orders.save(order)
        # Автокоммит при успехе, авторолбэк при исключении
```

---

### Паттерн «Спецификация» (Specification)

Инкапсулирует бизнес-правила в виде компонуемых, переиспользуемых спецификаций.

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

# Композиция
eligible_for_discount = ActiveUserSpec().and_(PremiumUserSpec())
users = [u for u in all_users if eligible_for_discount.is_satisfied_by(u)]
```

---

### Паттерн «Сага» (Saga)

Управляет распределёнными транзакциями через микросервисы с помощью последовательности локальных транзакций и компенсирующих действий.

**Хореографическая сага:**
```
OrderService ──публикует──▶ OrderCreated
                                   │
                       InventoryService ──▶ StockReserved
                                                   │
                                       PaymentService ──▶ PaymentProcessed
                                                                  │
                                              ShippingService ──▶ OrderShipped
```

**Оркестрационная сага:**
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
            logger.error(f"Сага провалилась для {order_id}: {e}")
            for compensation in reversed(compensations):
                await compensation  # Откат в обратном порядке
            raise SagaFailedError(order_id) from e
```

---

## 10. Паттерны распределённых систем

### Предохранитель (Circuit Breaker)

Предотвращает каскадные отказы, останавливая запросы к нестабильному сервису.

```
ЗАКРЫТ ──(порог отказов превышен)──▶ ОТКРЫТ
   ▲                                      │
   │                           (таймаут истёк)
   │                                      ▼
   └──(успех)──────────────── ПОЛУОТКРЫТ ──(отказ)──▶ ОТКРЫТ
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
                raise CircuitOpenError("Предохранитель разомкнут (OPEN)")

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
            logger.warning(f"Предохранитель ОТКРЫТ после {self._failures} отказов")
```

---

### Повтор с экспоненциальной задержкой (Retry with Exponential Backoff)

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
                delay *= (0.5 + random.random() * 0.5)  # Джиттер против «эффекта стада»

            logger.warning(f"Попытка {attempt + 1} провалилась: {e}. Повтор через {delay:.2f}с")
            time.sleep(delay)
```

---

### Переборка (Bulkhead)

Изолирует отказы в одной части системы, чтобы они не распространялись на другие.

```python
class BulkheadExecutor:
    """Пул потоков на сервис — исчерпание одного сервиса не влияет на другие."""
    def __init__(self, max_workers: int):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._semaphore = threading.Semaphore(max_workers)

    def submit(self, func: Callable, *args, timeout: float = 30.0) -> Future:
        if not self._semaphore.acquire(timeout=timeout):
            raise BulkheadFullError("Ёмкость переборки исчерпана")
        try:
            future = self._executor.submit(func, *args)
            future.add_done_callback(lambda _: self._semaphore.release())
            return future
        except Exception:
            self._semaphore.release()
            raise

# Каждая зависимость получает свой пул
payment_pool = BulkheadExecutor(max_workers=20)
inventory_pool = BulkheadExecutor(max_workers=10)
email_pool = BulkheadExecutor(max_workers=5)
```

---

### Паттерн «Исходящий ящик» (Outbox Pattern)

Гарантирует надёжную публикацию событий вместе с записью в базу данных.

```sql
-- Таблица транзакционного исходящего ящика
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

        # Записывается в ТОЙ ЖЕ транзакции, что и бизнес-данные
        db.insert_outbox(OutboxMessage(
            event_type="order.placed",
            payload=OrderPlacedEvent.from_order(order).to_dict()
        ))
        # Коммит атомарен — или оба успешны, или оба откатываются

# Отдельный релей-процесс опрашивает ящик и публикует в брокер
async def outbox_relay():
    while True:
        messages = db.fetch_pending_outbox(limit=100)
        for msg in messages:
            await message_broker.publish(msg.event_type, msg.payload)
            db.mark_outbox_processed(msg.id)
        await asyncio.sleep(1)
```

---

### Ключи идемпотентности (Idempotency Keys)

```python
class IdempotentCommandHandler:
    def __init__(self, handler: ICommandHandler, idempotency_store: IIdempotencyStore):
        self._handler = handler
        self._store = idempotency_store

    def handle(self, command: Command, idempotency_key: str) -> CommandResult:
        # Проверяем, не видели ли уже этот ключ
        if existing := self._store.get(idempotency_key):
            return existing  # Возвращаем кэшированный результат, не обрабатываем повторно

        result = self._handler.handle(command)
        self._store.set(idempotency_key, result, ttl=86400)  # Храним 24ч
        return result
```

---

## 11. CQRS и Event Sourcing

### CQRS — Разделение ответственности команд и запросов

Разделяет **модель чтения** от **модели записи**. Разные базы данных, оптимизированные под разные нагрузки.

```
                     ┌─────────────────┐
Сторона записи:      │   Шина команд   │
Команды ──────────▶  │                 │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐       ┌──────────────┐
                     │ Обработчик      │──────▶ │   БД записи  │
                     │ команд          │        │  (PostgreSQL)│
                     └────────┬────────┘       └──────┬───────┘
                              │                       │
                     Доменное событие опубликовано     │
                              │                       │
                     ┌────────▼────────┐    ┌─────────▼────────┐
                     │ Обработчик      │───▶ │   БД чтения      │
                     │ событий         │    │  (Elasticsearch) │
                     └─────────────────┘    └──────────────────┘
Сторона чтения:
Запросы ───────────────────────────────────▶ БД чтения (напрямую)
```

```python
# СТОРОНА КОМАНД
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

# СТОРОНА ЗАПРОСОВ (использует денормализованную модель чтения — намного быстрее)
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

### Event Sourcing — Источник событий

Сохраняет **последовательность событий**, приведших к текущему состоянию, а не само состояние.

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
        # Мутируем состояние на основе типа события
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
        account._events = []  # Очищаем — они уже сохранены
        return account
```

**Преимущества Event Sourcing:**
- Полный журнал аудита — каждое изменение состояния записано
- «Машина времени» — восстановление состояния на любой момент в истории
- Переигрывание событий — перестроение проекций с нуля
- Мощь отладки — видно точно, что произошло и когда

---

## 12. Архитектура микросервисов

### Принципы декомпозиции сервисов

- **По бизнес-возможностям**: каждый сервис владеет бизнес-доменом (OrderService, InventoryService, UserService)
- **По ограниченному контексту (DDD)**: каждый сервис соответствует ограниченному контексту
- **По владению командой**: Закон Конвея — структура системы отражает структуру коммуникации

### Коммуникация между сервисами

| Паттерн | Когда использовать | Технология |
|---------|--------------------|-----------|
| **Синхронный REST** | Запросы, необходим ответ | HTTP/HTTPS |
| **Синхронный gRPC** | Внутренние сервисы, критично к производительности | gRPC/protobuf |
| **Асинхронные события** | Изменения состояния, уведомления, развязанные потоки | Kafka, RabbitMQ |
| **Асинхронные команды** | Делегирование задач, «выстрелил и забыл» | SQS, Redis Queue |

### Сервисная сетка (Service Mesh)

Для крупных микросервисных деплойментов используй **service mesh** (Istio, Linkerd) для:
- mTLS между сервисами (сеть с нулевым доверием)
- Автоматической балансировки нагрузки
- Разрыва цепи на инфраструктурном уровне
- Инъекции распределённой трассировки

### API-шлюз (API Gateway)

```
Клиент
  │
  ▼
┌───────────────────────────────────┐
│            API Gateway            │
│  - Аутентификация                 │
│  - Ограничение частоты запросов   │
│  - Маршрутизация запросов         │
│  - Завершение SSL                 │
│  - Агрегация ответов              │
│  - Трансляция протоколов          │
└─┬──────────┬──────────┬───────────┘
  │          │          │
  ▼          ▼          ▼
Сервис    Сервис    Сервис
заказов  склада    пользователей
```

---

## 13. Событийно-ориентированная архитектура (EDA)

### Типы событий

| Тип | Описание | Пример |
|-----|----------|--------|
| **Доменное событие** | Что-то произошло в домене | `OrderPlaced`, `PaymentFailed` |
| **Интеграционное событие** | Межсервисное уведомление | `order-service.order.placed` |
| **Команда** | Инструкция что-то сделать | `ProcessPayment`, `SendEmail` |
| **Запрос** | Обращение только для чтения | `GetOrderById` |

### Проектирование схемы событий

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

**Правила эволюции схемы:**
1. Никогда не удаляй поля в минорной версии
2. Новые опциональные поля = повышение минорной версии
3. Ломающие изменения = новая версия типа события (`order.placed.v2`)
4. Поддерживай обратную совместимость не менее 2 мажорных версий

---

## 14. Стандарты проектирования API

### Стандарты REST API

**Проектирование URL:**
```
GET    /api/v1/orders              — Список заказов
POST   /api/v1/orders              — Создать заказ
GET    /api/v1/orders/{id}         — Получить заказ по ID
PUT    /api/v1/orders/{id}         — Полное обновление
PATCH  /api/v1/orders/{id}         — Частичное обновление
DELETE /api/v1/orders/{id}         — Удалить заказ
GET    /api/v1/orders/{id}/items   — Вложенный ресурс
POST   /api/v1/orders/{id}/cancel  — Действие (глагол здесь уместен)
```

**Стандарты HTTP-статусов:**

| Код | Когда использовать |
|-----|-------------------|
| 200 OK | Успешный GET, PUT, PATCH |
| 201 Created | Успешный POST |
| 204 No Content | Успешный DELETE |
| 400 Bad Request | Ошибка валидации |
| 401 Unauthorized | Отсутствует/невалидная аутентификация |
| 403 Forbidden | Аутентификация верна, нет разрешения |
| 404 Not Found | Ресурс не существует |
| 409 Conflict | Конфликт состояния (дубликат, рассогласование версий) |
| 422 Unprocessable Entity | Синтаксис верен, нарушены бизнес-правила |
| 429 Too Many Requests | Превышен лимит запросов |
| 500 Internal Server Error | Непредвиденная ошибка сервера |
| 503 Service Unavailable | Обслуживание, перегрузка |

**Стандартизованный ответ с ошибкой:**
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Валидация запроса не прошла",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Должен быть корректный email-адрес"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Возраст должен быть от 18 до 120"
      }
    ],
    "trace_id": "req-abc-123",
    "timestamp": "2026-03-11T10:00:00Z"
  }
}
```

### Стратегии версионирования API

| Стратегия | Плюсы | Минусы |
|-----------|-------|--------|
| URL-путь (`/v1/`) | Явно, кэшируемо | URL меняется |
| Заголовок (`Api-Version: 1`) | Чистые URL | Менее заметно |
| Параметр запроса (`?version=1`) | Легко тестировать | Захламляет URL |

**Рекомендация:** используй версионирование через URL-путь. Просто, явно, легко маршрутизировать.

### Стандарт пагинации

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

## 15. Моделирование данных и персистентность

### Объекты-значения vs Сущности vs Агрегаты

```python
# ОБЪЕКТ-ЗНАЧЕНИЕ — идентифицируется своим значением, неизменяем
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Деньги не могут быть отрицательными")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise CurrencyMismatchError()
        return Money(self.amount + other.amount, self.currency)

# СУЩНОСТЬ — идентифицируется по ID, изменяемое состояние
class Order:
    def __init__(self, order_id: UUID, user_id: UUID):
        self.id = order_id
        self.user_id = user_id
        self._items: list[OrderItem] = []
        self._status = OrderStatus.PENDING

# КОРЕНЬ АГРЕГАТА — кластер сущностей и объектов-значений
class Order:  # Корень агрегата Order
    def add_item(self, product_id: UUID, qty: int, price: Money) -> None:
        """Все мутации проходят через корень агрегата."""
        item = OrderItem(product_id=product_id, quantity=qty, unit_price=price)
        self._items.append(item)
        self._recalculate_total()

    def place(self) -> list[DomainEvent]:
        """Бизнес-логика применяется здесь, не в репозитории."""
        if not self._items:
            raise EmptyOrderError()
        self._status = OrderStatus.CONFIRMED
        return [OrderPlacedEvent(order_id=self.id, total=self.total)]
```

### Руководство по выбору базы данных

| База данных | Лучше всего для | Избегай когда |
|-------------|-----------------|---------------|
| **PostgreSQL** | Реляционные данные, ACID, сложные запросы | Огромные неструктурированные записи |
| **MongoDB** | Гибкая схема, иерархии документов | Сложные JOIN'ы, ACID-транзакции |
| **Redis** | Кэш, сессии, pub/sub, очереди | Большие данные, сложные запросы |
| **Elasticsearch** | Полнотекстовый поиск, агрегация логов | Основное хранилище данных |
| **Cassandra** | Огромная пропускная способность записи, временные ряды | Сложные запросы, ACID |
| **TimescaleDB** | Временные ряды, метрики | Нетемпоральные реляционные данные |
| **Neo4j** | Графовые связи, рекомендации | Нографовые данные |

### Стратегия миграций

```
migrations/
├── 001_create_users.sql
├── 002_create_orders.sql
├── 003_add_order_status_index.sql
└── 004_add_payment_method.sql
```

Правила:
- Миграции **только добавляются** — никогда не редактируй закоммиченную миграцию
- Каждая миграция **идемпотентна** (`CREATE TABLE IF NOT EXISTS`)
- Обратно совместимые миграции (паттерн «расширить/сократить»):
  1. **Расширить**: добавить новый столбец (nullable)
  2. **Перенести**: заполнить данные
  3. **Сократить**: удалить старый столбец (отдельный деплой)

---

## 16. Отказоустойчивость и надёжность

### Атомарный ввод-вывод (Запись во временный файл с подменой)

```python
def atomic_write(file_path: Path, data: bytes) -> None:
    """Атомарная запись через временный файл + переименование.
    Переименование атомарно в POSIX — никаких частичных записей.
    """
    tmp_path = file_path.with_suffix(".tmp")
    try:
        tmp_path.write_bytes(data)
        tmp_path.rename(file_path)  # Атомарно на той же файловой системе
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
```

### Паттерн «Контрольная точка и возобновление»

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

        # Проверка целостности
        if compute_checksum(items) != state.checksum:
            raise DataIntegrityError("Входные данные изменились с момента последней точки")

        # Продолжаем с того места, где остановились
        for i, item in enumerate(items[state.last_processed_offset:], start=state.last_processed_offset):
            self._process_item(item)

            # Сохраняем контрольную точку каждые N элементов
            if i % 100 == 0:
                state.last_processed_offset = i + 1
                self._save_checkpoint(state)

        state.status = "completed"
        self._save_checkpoint(state)
        return ProcessingResult(processed=len(items))
```

### Эндпоинт проверки состояния (Health Check)

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

# Проба живости — жив ли процесс?
GET /health/live    → 200 если процесс запущен

# Проба готовности — готов ли сервис принимать трафик?
GET /health/ready   → 200 только если все зависимости здоровы
```

### Иерархия таймаутов

Каждый внешний вызов ОБЯЗАН иметь таймаут. Каскадные таймауты для предотвращения голодания потоков:

```python
# Таймаут внешнего API-запроса
REQUEST_TIMEOUT = 30  # секунд

# Таймаут запроса к базе данных
DB_QUERY_TIMEOUT = 5  # секунд

# Таймаут кэша
CACHE_TIMEOUT = 1  # секунда

# Таймаут вызова внешнего API
EXTERNAL_API_TIMEOUT = 10  # секунд

# Таймаут публикации в брокер сообщений
MQ_PUBLISH_TIMEOUT = 3  # секунды
```

---

## 17. Стандарты безопасности

### Валидация входных данных (Никому не доверяй)

Всё внешнее входные данные ОБЯЗАНЫ валидироваться на границе системы. Внешнее = HTTP, сообщения из очереди, файлы, аргументы CLI, переменные окружения.

```python
class CreateUserRequest(BaseModel):
    """Модель Pydantic как граница валидации."""
    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")]
    age: Annotated[int, Field(ge=18, le=120)]
    role: Literal["admin", "user", "moderator"]

# В слое контроллера/адаптера:
def create_user(raw_data: dict) -> Response:
    try:
        dto = CreateUserRequest(**raw_data)  # Валидирует и бросает исключение при ошибке
    except ValidationError as e:
        raise BadRequestError(details=e.errors())
    return use_case.execute(dto)
```

### Аутентификация и авторизация

**Аутентификация (кто ты?):**
- Используй JWT с коротким сроком жизни (15 мин access-токен, 7 дней refresh-токен)
- Храни refresh-токены в httpOnly-куках
- Ротируй refresh-токены при использовании
- Инвалидируй все токены при смене пароля

**Авторизация (что ты можешь делать?):**
```python
# RBAC — управление доступом на основе ролей
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
                raise ForbiddenError(f"Требуется разрешение: {permission.value}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### Меры против OWASP Top 10

| Угроза | Мера защиты |
|--------|------------|
| **Внедрение (SQL, NoSQL)** | Параметризованные запросы ВСЕГДА. Никакой конкатенации SQL. |
| **Нарушенная аутентификация** | Ротация JWT, безопасные флаги кук, защита от перебора |
| **Утечка чувствительных данных** | Шифрование в покое (AES-256), в транзите (TLS 1.3), никогда не логировать PII |
| **XXE** | Отключить обработку внешних XML-сущностей |
| **IDOR** | Проверять владение объектом при КАЖДОМ запросе |
| **Неправильная конфигурация безопасности** | IaC, секреты в хранилище, отключить отладку в проде |
| **XSS** | Кодирование вывода, заголовки CSP, санитизация HTML-ввода |
| **Небезопасная десериализация** | Валидировать все десериализованные данные |
| **Уязвимые зависимости** | `dependabot`, `snyk`, регулярный `pip audit` / `npm audit` |
| **Недостаточное логирование** | Логировать все события аутентификации, отказы в доступе |

### Управление секретами

```python
# ЗАПРЕЩЕНО — жёстко закодированные секреты
DB_PASSWORD = "mysecretpassword123"
API_KEY = "sk-1234567890abcdef"

# ПРАВИЛЬНО — использовать менеджер секретов
from vault_client import VaultClient

class SecretsProvider:
    def __init__(self):
        self._vault = VaultClient(vault_addr=os.getenv("VAULT_ADDR"))

    def get_db_password(self) -> str:
        return self._vault.read("secret/database/password")
```

---

## 18. Наблюдаемость: Логи, Метрики, Трассировки

**Три столпа наблюдаемости**: Логи, Метрики, Распределённые трассировки.

### Структурированное логирование

```python
import structlog

logger = structlog.get_logger()

# НЕПРАВИЛЬНО — неструктурированное, непоисковое
print(f"Заказ {order_id} размещён пользователем {user_id}")

# ПРАВИЛЬНО — структурированный, запрашиваемый JSON
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

**Уровни логирования — когда что использовать:**

| Уровень | Применяется для |
|---------|----------------|
| `DEBUG` | Детальная диагностическая информация (только dev/staging) |
| `INFO` | Нормальные бизнес-операции (заказ размещён, пользователь вошёл) |
| `WARNING` | Неожиданное, но восстанавливаемое (попытка повтора, промах кэша) |
| `ERROR` | Операция провалилась, требует внимания |
| `CRITICAL` | Общесистемный сбой, немедленные действия |

**Никогда не логировать:**
- Пароли, токены, API-ключи
- Номера банковских карт (даже частичные)
- Персональные медицинские данные
- Любые поля, помеченные как PII

---

### Метрики (Методы RED и USE)

**Метод RED** (для сервисов):
- **R**ate — запросов в секунду
- **E**rrors — частота ошибок
- **D**uration — время ответа (p50, p95, p99)

**Метод USE** (для ресурсов):
- **U**tilization — % времени, когда ресурс занят
- **S**aturation — глубина очереди, время ожидания
- **E**rrors — события ошибок

```python
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Всего HTTP запросов",
    labelnames=["method", "path", "status_code"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Длительность HTTP запроса",
    labelnames=["method", "path"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
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

### Распределённая трассировка

Каждый запрос получает `trace_id`. Каждый вызов сервиса получает `span_id`. Передаются через заголовки.

```python
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace.get_tracer("order-service")

def place_order(command: PlaceOrderCommand, headers: dict) -> OrderResult:
    # Извлекаем контекст трассировки из входящего запроса
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

## 19. Стратегия тестирования

### Пирамида тестирования

```
            ▲
           /E\
          / 2E\        E2E-тесты (5%)
         /  E  \       — Полная система, браузерные тесты, API-интеграция
        /───────\
       /Интеграц.\    Интеграционные тесты (15%)
      /   тесты   \   — БД + сервисные тесты, брокер сообщений
     /─────────────\
    /  Юнит-тесты   \ Юнит-тесты (80%)
   /                 \ — Чистая логика, без I/O, быстро, много
  /───────────────────\
```

### Юнит-тесты

```python
class TestOrderPlacement:
    def test_order_placed_successfully(self):
        # ПОДГОТОВКА
        user_id = uuid4()
        items = [OrderItem(product_id=uuid4(), qty=2, price=Money("9.99", "USD"))]
        order = Order(user_id=user_id)

        # ДЕЙСТВИЕ
        events = order.place(items)

        # ПРОВЕРКА
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

### Интеграционные тесты

```python
@pytest.mark.integration
class TestOrderRepository:
    def test_save_and_retrieve_order(self, db_session):
        # ПОДГОТОВКА
        order = Order.create(user_id=uuid4(), items=[...])
        repo = PostgresOrderRepository(db_session)

        # ДЕЙСТВИЕ
        repo.save(order)
        retrieved = repo.find_by_id(order.id)

        # ПРОВЕРКА
        assert retrieved is not None
        assert retrieved.id == order.id
        assert retrieved.status == order.status
```

### Контрактные тесты (Pact)

Для микросервисов — проверяй соблюдение API-контракта между потребителем и поставщиком.

```python
# Потребитель определяет ожидаемый контракт
@pytest.fixture
def order_contract(pact):
    return (
        pact
        .given("Заказ #123 существует")
        .upon_receiving("запрос заказа #123")
        .with_request("GET", "/api/v1/orders/123")
        .will_respond_with(200, body={
            "id": "123",
            "status": "confirmed",
            "total": Like({"amount": "99.99", "currency": "USD"})
        })
    )
```

### Правила тестирования

- Тестируй поведение, а не реализацию (тестируй *что*, а не *как*)
- Одна проверка на логическую концепцию (не обязательно одна на функцию)
- Тесты должны быть **БЫСТРЫМИ** (юнит < 1 мс, интеграция < 1 с)
- Тесты должны быть **ИЗОЛИРОВАННЫМИ** (нет общего изменяемого состояния)
- Тесты должны быть **ДЕТЕРМИНИРОВАННЫМИ** (один результат при каждом запуске)
- Мокай только то, что тебе принадлежит (используй фейки для сторонних систем)
- Имена тестов: `test_{что}_{когда}_{ожидаемое}`

---

## 20. Инжиниринг производительности

### Стратегия кэширования

**Паттерны кэша:**

| Паттерн | Как работает | Лучше всего для |
|---------|-------------|-----------------|
| **Cache-Aside** | Приложение проверяет кэш, при промахе загружает из БД | Много чтений, вариативные данные |
| **Write-Through** | Запись в кэш И в БД одновременно | Важна согласованность |
| **Write-Behind** | Запись в кэш, асинхронная запись в БД | Много записей, допустима итоговая согласованность |
| **Read-Through** | Кэш сам загружает из БД при промахе | Прозрачное кэширование |

```python
class CachingOrderRepository(IOrderRepository):
    def __init__(self, repo: IOrderRepository, cache: ICache):
        self._repo = repo
        self._cache = cache

    def find_by_id(self, order_id: UUID) -> Order | None:
        cache_key = f"order:{order_id}"

        # Паттерн Cache-Aside
        if cached := self._cache.get(cache_key):
            return Order.deserialize(cached)

        order = self._repo.find_by_id(order_id)
        if order:
            self._cache.set(cache_key, order.serialize(), ttl=300)
        return order

    def save(self, order: Order) -> None:
        self._repo.save(order)
        self._cache.delete(f"order:{order.id}")  # Инвалидируем при записи
```

### Оптимизация запросов к БД

```sql
-- Анализируй свои запросы в продакшене
EXPLAIN ANALYZE
SELECT o.*, u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending'
  AND o.created_at > NOW() - INTERVAL '7 days'
ORDER BY o.created_at DESC
LIMIT 100;

-- Создавай целевые индексы
CREATE INDEX CONCURRENTLY idx_orders_status_created
    ON orders(status, created_at DESC)
    WHERE status = 'pending';  -- Частичный индекс = меньше, быстрее

-- Используй покрывающие индексы для тяжёлых запросов на чтение
CREATE INDEX idx_orders_user_covering
    ON orders(user_id) INCLUDE (id, status, total_amount, created_at);
```

### Асинхронный ввод-вывод

```python
async def fetch_order_data(order_id: UUID) -> OrderDetailDTO:
    """Загружаем связанные данные конкурентно, а не последовательно."""
    order, user, payment, shipment = await asyncio.gather(
        order_repo.find_by_id_async(order_id),
        user_repo.find_by_order_async(order_id),
        payment_repo.find_by_order_async(order_id),
        shipment_repo.find_by_order_async(order_id),
    )
    return OrderDetailDTO.assemble(order, user, payment, shipment)
```

---

## 21. CI/CD и DevOps пайплайн

### Стадии пайплайна

```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  # Стадия 1: Быстрая обратная связь (< 2 мин)
  lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .
      - run: mypy src/

  # Стадия 2: Юнит-тесты (< 5 мин)
  unit-tests:
    runs-on: ubuntu-latest
    needs: lint-and-type-check
    steps:
      - run: pytest tests/unit/ -x --tb=short

  # Стадия 3: Интеграционные тесты (< 15 мин)
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

  # Стадия 4: Сканирование безопасности
  security-scan:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - run: pip-audit
      - run: bandit -r src/
      - uses: snyk/actions/python@master

  # Стадия 5: Сборка и публикация Docker-образа
  build:
    needs: [integration-tests, security-scan]
    if: github.ref == 'refs/heads/main'
    steps:
      - run: docker build -t myapp:${{ github.sha }} .
      - run: docker push registry/myapp:${{ github.sha }}

  # Стадия 6: Деплой на staging, запуск E2E
  deploy-staging:
    needs: build
    steps:
      - run: kubectl set image deployment/myapp app=registry/myapp:${{ github.sha }} -n staging
      - run: pytest tests/e2e/ --base-url=https://staging.myapp.com

  # Стадия 7: Деплой на продакшен (ручное подтверждение)
  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://myapp.com
    steps:
      - run: kubectl set image deployment/myapp app=registry/myapp:${{ github.sha }} -n production
```

### Стратегии деплоя

| Стратегия | Описание | Скорость отката | Риск |
|-----------|----------|----------------|------|
| **Recreate** | Убить старое, запустить новое | Медленно | Высокий (простой) |
| **Rolling** | Постепенная замена экземпляров | Средне | Низкий |
| **Blue/Green** | Два идентичных окружения, переключение трафика | Мгновенно | Низкий (двойная стоимость) |
| **Canary** | Направить % трафика на новую версию | Мгновенно | Очень низкий |
| **Feature Flags** | Деплоим код, включаем в рантайме | Мгновенно | Минимальный |

---

## 22. Инфраструктура как код (IaC)

### Принципы

- Вся инфраструктура определяется в версионируемом коде (Terraform, Pulumi, CloudFormation)
- Окружения создаются/уничтожаются через код, а не ручными кликами
- Никаких ручных изменений продакшен-инфраструктуры
- Изменения инфраструктуры проходят тот же процесс PR/ревью, что и код приложения

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

### Лучшие практики Docker

```dockerfile
# Многостадийная сборка — минимальный продакшен-образ
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS production
# Безопасность: запускаем не от root
RUN useradd --create-home --no-log-init appuser
USER appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser src/ ./src/

# Проверка состояния встроена в образ
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health/live || exit 1

EXPOSE 8080
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 23. Предметно-ориентированное проектирование (DDD)

### Стратегический DDD

**Ограниченный контекст**: языковая граница, внутри которой конкретная доменная модель применяется и остаётся согласованной.

```
┌──────────────────────┐    ┌──────────────────────┐
│  КОНТЕКСТ ЗАКАЗОВ    │    │  КОНТЕКСТ СКЛАДА     │
│                      │    │                      │
│  Order               │    │  StockItem           │
│  LineItem            │    │  Warehouse           │
│  Customer (→ userId) │    │  Product (→ sku)     │
│                      │    │                      │
└──────────────────────┘    └──────────────────────┘
         │                             │
         │       Карта контекстов      │
         └─────────── ACL ─────────────┘
              (Антикоррупционный слой)
```

**Отношения в карте контекстов:**
- **Общее ядро**: два контекста делят часть модели
- **Клиент/Поставщик**: нижестоящая команда зависит от вышестоящей
- **Конформист**: нижестоящий принимает модель вышестоящего как есть
- **ACL (Антикоррупционный слой)**: нижестоящий транслирует из модели вышестоящего

### Тактические строительные блоки DDD

| Блок | Назначение |
|------|-----------|
| **Сущность (Entity)** | Имеет идентичность (ID), изменяемая |
| **Объект-значение (Value Object)** | Нет идентичности, определяется значением, неизменяем |
| **Агрегат (Aggregate)** | Кластер сущностей/ОЗ, граница согласованности |
| **Доменное событие (Domain Event)** | Что-то произошло, неизменяемый факт |
| **Репозиторий (Repository)** | Абстрагирует персистентность для агрегатов |
| **Доменный сервис (Domain Service)** | Бизнес-логика, не принадлежащая ни одной сущности |
| **Сервис приложения (Application Service)** | Оркестрирует use cases, без бизнес-логики |
| **Фабрика (Factory)** | Сложная конструкция агрегатов/сущностей |

### Доменные события на практике

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
        """Слой приложения собирает события после операций над агрегатом."""
        events = list(self._uncommitted_events)
        self._uncommitted_events.clear()
        return events

# Сервис приложения
def cancel_order(order_id: UUID, reason: str) -> None:
    with uow:
        order = uow.orders.find_by_id(order_id)
        order.cancel(reason)
        uow.orders.save(order)
        for event in order.pull_events():
            event_bus.publish(event)
```

---

## 24. Конкурентность и асинхронные паттерны

### Оптимистическая блокировка

```python
class Order:
    version: int = 0  # Инкрементируется при каждом сохранении

class PostgresOrderRepository:
    def save(self, order: Order) -> None:
        result = self._db.execute("""
            UPDATE orders
            SET status = %s, version = version + 1
            WHERE id = %s AND version = %s
        """, [order.status, order.id, order.version])

        if result.rowcount == 0:
            raise ConcurrentModificationError(
                f"Заказ {order.id} был изменён другим процессом"
            )
```

### Паттерн асинхронной очереди задач

```python
# Производитель
async def place_order(command: PlaceOrderCommand) -> UUID:
    order = Order.create(command)
    await order_repo.save(order)

    # Передаём тяжёлую работу в очередь, отвечаем немедленно
    await task_queue.enqueue(
        "send_order_confirmation",
        {"order_id": str(order.id), "user_email": command.user_email},
        priority="high"
    )
    return order.id

# Потребитель (отдельный процесс-воркер)
@task_queue.worker("send_order_confirmation")
async def handle_send_confirmation(payload: dict) -> None:
    order = await order_repo.find_by_id(UUID(payload["order_id"]))
    await email_service.send_confirmation(
        to=payload["user_email"],
        order=order
    )
```

### Чеклист потокобезопасности

- [ ] Общее изменяемое состояние защищено блокировками
- [ ] Соединения с БД не разделяются между потоками
- [ ] Синглтоны потокобезопасны (двойная проверка с блокировкой)
- [ ] Нет глобальных изменяемых переменных
- [ ] Асинхронный код не блокирует цикл событий (нет `time.sleep` в async)
- [ ] Пулы соединений sized appropriately под уровень конкурентности

---

## 25. Стандарты документации

### Документирование кода

```python
def calculate_compound_interest(
    principal: Money,
    annual_rate: Decimal,
    periods_per_year: int,
    years: int,
) -> Money:
    """
    Вычисляет сложные проценты по стандартной формуле.

    Формула: A = P(1 + r/n)^(nt)
    Где:
        A = итоговая сумма
        P = основной капитал
        r = годовая ставка (как десятичная дробь, например 0.05 = 5%)
        n = количество периодов начисления в год
        t = время в годах

    Args:
        principal:         Начальная сумма вложений
        annual_rate:       Годовая процентная ставка (0.05 = 5%)
        periods_per_year:  Количество периодов начисления в год
                           (1=ежегодно, 4=ежеквартально, 12=ежемесячно, 365=ежедневно)
        years:             Срок вложений в годах

    Returns:
        Итоговая сумма с учётом основного капитала и процентов

    Raises:
        NegativePrincipalError:  Если основной капитал отрицателен
        InvalidRateError:        Если annual_rate не в диапазоне [0, 1]
        InvalidPeriodsError:     Если periods_per_year < 1

    Пример:
        >>> calculate_compound_interest(
        ...     principal=Money("1000.00", "USD"),
        ...     annual_rate=Decimal("0.05"),
        ...     periods_per_year=12,
        ...     years=10
        ... )
        Money("1647.01", "USD")
    """
```

### Записи об архитектурных решениях (ADR)

Храни архитектурные решения в системе контроля версий. Шаблон:

```markdown
# ADR-042: Использовать Kafka для межсервисных событий

**Дата:** 2026-03-11
**Статус:** Принято
**Решающие:** @arch-team

## Контекст
Нам нужна надёжная асинхронная коммуникация между 12 микросервисами.
Текущий подход (прямой HTTP) создаёт тесную связность и теряет события при сбоях.

## Решение
Использовать Apache Kafka как центральную шину событий для всей межсервисной коммуникации.

## Последствия
**Положительные:**
- Развязанные сервисы — издателю не нужно, чтобы потребители были доступны
- Возможность переигрывания событий
- Горизонтальное масштабирование потребителей

**Отрицательные:**
- Операционная сложность управления кластером Kafka
- Итоговая согласованность (не мгновенная)
- Требует идемпотентности потребителей

## Рассмотренные альтернативы
- **RabbitMQ**: Проще в эксплуатации, но нет хранения логов/переигрывания
- **AWS SNS/SQS**: Управляемый сервис, но привязка к вендору, выше задержки
- **Прямой HTTP**: Ноль инфраструктуры, но тесная связность, нет гарантий доставки
```

---

## 26. Командный процесс и культура кода

### Git-рабочий процесс

**Именование веток:**
```
feature/TICKET-123-add-payment-method
bugfix/TICKET-456-fix-order-total-calculation
hotfix/TICKET-789-critical-payment-failure
chore/TICKET-012-upgrade-dependencies
```

**Сообщения коммитов (Conventional Commits):**
```
feat(orders): add bulk order cancellation
fix(payments): prevent double charge on retry
docs(api): update order endpoint examples
refactor(auth): extract token validation logic
test(inventory): add concurrent reservation tests
chore(deps): upgrade django from 4.2 to 5.0
perf(queries): add covering index for order listing
```

### Стандарты ревью кода

**Что проверяет ревьюер:**
- [ ] Делает ли код то, что написано в тикете?
- [ ] Достаточно ли тестов?
- [ ] Обработаны ли граничные случаи?
- [ ] Корректна ли обработка ошибок?
- [ ] Есть ли проблемы безопасности?
- [ ] Читается ли код без дополнительных объяснений?
- [ ] Есть ли нарушения SOLID?
- [ ] Нет ли излишней сложности?
- [ ] Осмысленны ли логи и не утекает ли PII?

**Этикет ревью:**
- Придирки помечать `[nit]` — автор может игнорировать
- Блокирующие комментарии требуют объяснения
- Аппрув с запросом изменений, когда замечания незначительны
- Никогда не апрувить не читая

### Определение «Готово» (Definition of Done)

Фича готова, когда:
- [ ] Код написан и прошёл ревью
- [ ] Юнит-тесты проходят (покрытие ≥ 80% нового кода)
- [ ] Интеграционные тесты проходят
- [ ] Документация обновлена (API docs, ADR при архитектурном изменении)
- [ ] Фича-флаги настроены при необходимости
- [ ] Мониторинг/алерты настроены
- [ ] Задеплоено на staging и проверено
- [ ] Принято Product Owner'ом

---

## 27. Антипаттерны — чего избегать

| Антипаттерн | Описание | Решение |
|------------|---------|---------|
| **Объект Бог (God Object)** | Один класс, который всё знает и делает | Разбить по SRP |
| **Магические числа** | `if status == 3` | Именованные константы/перечисления |
| **Дробовик (Shotgun Surgery)** | Одно изменение требует правок во многих местах | Инкапсулировать связанную логику |
| **Одержимость примитивами** | Использование `str` для email, `int` для денег | Объекты-значения |
| **Зависть к данным (Feature Envy)** | Метод больше использует данные чужого класса | Переместить в нужный класс |
| **Кучки данных (Data Clumps)** | Одни и те же 3 параметра всегда вместе | Создать объект данных |
| **Расходящиеся изменения** | Класс меняется по разным несвязанным причинам | Разбить класс |
| **Ленивый класс** | Класс почти ничего не делает | Объединить или удалить |
| **Призрачная обобщённость** | Абстракции без текущей конкретной нужды | YAGNI |
| **Временная связность (Temporal Coupling)** | `A.init()` нужно вызвать до `A.process()` | Инъекция через конструктор |
| **Локатор сервисов (Service Locator)** | Глобальный реестр зависимостей | Правильный DI-контейнер |
| **Анемичная доменная модель** | Доменные объекты — только контейнеры данных | Перенести логику в сущности |
| **Распределённый монолит** | Микросервисы, которые деплоятся вместе | Исправить границы сервисов |
| **N+1 запросов** | Цикл делает запрос к БД на каждой итерации | JOIN или жадная загрузка |
| **Спагетти-код** | Нет структуры, всё вызывает всё | Применить чистую архитектуру |

---

## 28. Чеклисты — перед деплоем и ревью архитектуры

### Чеклист перед деплоем

```
БЕЗОПАСНОСТЬ
─────────────────────────────────────────────────────────
[ ] Никаких секретов в репозитории
[ ] Все внешние входные данные валидируются
[ ] Аутентификация и авторизация проверены
[ ] Зависимости просканированы на уязвимости (pip-audit / npm audit)
[ ] SQL-инъекции невозможны (параметризованные запросы везде)

НАДЁЖНОСТЬ
─────────────────────────────────────────────────────────
[ ] Для всех внешних вызовов настроены таймауты
[ ] Логика повтора реализована для транзиентных ошибок
[ ] Предохранители установлены для критических зависимостей
[ ] Реализовано graceful shutdown (обработчик SIGTERM)
[ ] Миграции БД обратно совместимы

НАБЛЮДАЕМОСТЬ
─────────────────────────────────────────────────────────
[ ] Структурированное логирование настроено
[ ] Ключевые бизнес-события логируются
[ ] Метрики выгружаются на эндпоинт /metrics
[ ] Заголовки распределённой трассировки передаются
[ ] Эндпоинты проверки состояния отвечают корректно
[ ] Алерты настроены по частоте ошибок и задержкам

ПРОИЗВОДИТЕЛЬНОСТЬ
─────────────────────────────────────────────────────────
[ ] Запросы к БД проиндексированы (проверен EXPLAIN ANALYZE)
[ ] Нет N+1-запросов
[ ] Настроено подходящее кэширование
[ ] Нагрузочное тестирование проведено при ожидаемом пиковом трафике

ДАННЫЕ
─────────────────────────────────────────────────────────
[ ] Миграции протестированы на staging с реальным объёмом данных
[ ] Есть план отката для миграций данных
[ ] PII идентифицированы и обрабатываются согласно политике
[ ] Резервные копии протестированы, время восстановления измерено
```

### Чеклист ревью архитектуры

```
ДИЗАЙН
─────────────────────────────────────────────────────────
[ ] Ограниченные контексты чётко определены
[ ] Зависимости направлены внутрь (Чистая архитектура)
[ ] Агрегаты обеспечивают инварианты
[ ] Доменная модель свободна от зависимостей от фреймворков
[ ] API соответствует стандарту версионирования

МАСШТАБИРУЕМОСТЬ
─────────────────────────────────────────────────────────
[ ] Stateless-дизайн сервисов (состояние вынесено наружу)
[ ] Горизонтальное масштабирование возможно без переработки
[ ] БД не является узким местом (реплики чтения, план шардинга)
[ ] Стратегия кэширования задокументирована

ЭКСПЛУАТАЦИЯ
─────────────────────────────────────────────────────────
[ ] Стратегия деплоя определена (rolling/canary/blue-green)
[ ] Фича-флаги установлены для рискованных изменений
[ ] Runbook написан для типичных сценариев сбоя
[ ] Путь эскалации дежурного задокументирован
[ ] План аварийного восстановления протестирован
```

---

## ПРИЛОЖЕНИЕ: Краткий справочник

### Компромисс между сложностью и пользой

```
Применяй Чистую архитектуру, когда:     Пропускай, когда:
─ Команда > 3 разработчиков              ─ Проект на выходных
─ Много интеграционных точек             ─ Утилита/CLI-скрипт
─ Долгосрочная кодовая база              ─ Чистый пайплайн данных
─ Несколько команд работают над ней      ─ Прототип (пока не станет чем-то большим)

Применяй микросервисы, когда:           Пропускай, когда:
─ Командам нужны независимые деплои     ─ Команда < 10 человек
─ Сервисы масштабируются по-разному     ─ Бизнес-домен ещё не устоялся
─ Нужны разные технологические стеки    ─ Запускаешь новый продукт

Применяй Event Sourcing, когда:         Пропускай, когда:
─ Журнал аудита — ключевое требование   ─ Нет требований к аудиту
─ Нужна отладка с машиной времени       ─ Простое CRUD-приложение
─ Требуются сложные проекции            ─ Команда не знакома с паттерном
```

### Сводка золотых правил

```
┌─────────────────────────────────────────────────────────────────┐
│                  10 ЗАПОВЕДЕЙ АРХИТЕКТОРА                       │
├─────────────────────────────────────────────────────────────────┤
│  I.   Не дублируй логику                                        │
│  II.  Пиши только то, что нужно, и не больше                    │
│  III. Называй вещи так, словно от этого зависит твоя жизнь      │
│  IV.  Инвертируй свои зависимости                               │
│  V.   Валидируй все внешние входные данные                      │
│  VI.  Делай весь ввод-вывод атомарным                           │
│  VII. Логируй структурированно и осмысленно                     │
│  VIII.Тестируй поведение, а не реализацию                       │
│  IX.  Никогда не храни секреты в коде                           │
│  X.   У тебя всегда должен быть план отката                     │
└─────────────────────────────────────────────────────────────────┘
```

---

*СТАНДАРТЫ СИСТЕМЫ ASGUARD01 — Полное руководство архитектора*
*Версия 3.0 · Последнее обновление: 2026 · Гриф: Внутренний справочник*

> *«Сначала сделай, чтобы работало. Потом сделай правильно. Потом сделай быстро.»*
> — Кент Бек
