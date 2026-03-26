# PHP Naming Conventions — The Complete Guide

> Covers PSR-1, PSR-2, PSR-12, Symfony, Laravel, and modern PHP 8.x community standards.

---

## Table of Contents

1. [General Principles](#1-general-principles)
2. [Variables](#2-variables)
3. [Constants](#3-constants)
4. [Functions](#4-functions)
5. [Classes](#5-classes)
6. [Abstract Classes & Interfaces](#6-abstract-classes--interfaces)
7. [Traits](#7-traits)
8. [Enums (PHP 8.1+)](#8-enums-php-81)
9. [Methods](#9-methods)
10. [Properties & Fields](#10-properties--fields)
11. [Private / Protected Members](#11-private--protected-members)
12. [Parameters](#12-parameters)
13. [Namespaces](#13-namespaces)
14. [Files & Directories](#14-files--directories)
15. [Type Declarations & Generics (Psalm/PHPStan)](#15-type-declarations--generics-psalmphpstan)
16. [Boolean Variables](#16-boolean-variables)
17. [Magic Methods](#17-magic-methods)
18. [Exceptions](#18-exceptions)
19. [Event Handlers & Listeners](#19-event-handlers--listeners)
20. [Laravel Conventions](#20-laravel-conventions)
21. [Symfony Conventions](#21-symfony-conventions)
22. [Test Files & Test Identifiers](#22-test-files--test-identifiers)
23. [Abbreviations & Acronyms](#23-abbreviations--acronyms)
24. [Naming Anti-patterns](#24-naming-anti-patterns)
25. [Quick Reference Cheatsheet](#25-quick-reference-cheatsheet)
26. [References & Further Reading](#26-references--further-reading)

---

## 1. General Principles

- **Follow PSR standards** — PSR-1 and PSR-12 are the baseline for all modern PHP projects.
- **Be descriptive, not terse.** `$userAccountList` beats `$ul` or `$data`.
- **Be consistent.** Pick one convention per construct and never mix.
- **Avoid abbreviations** unless they are universally known (`url`, `id`, `http`, `api`, `sql`).
- **Pronounceable names.** If you can't say it aloud, reconsider.
- **Don't encode the type in the name** (Hungarian notation is dead): `$strName` → `$name`, `$arrItems` → `$items`.
- **Avoid noise words**: `data`, `info`, `object`, `manager` add no meaning unless necessary.
- **Use positive naming for booleans**: `$isLoading`, not `$isNotLoading`.
- **Avoid single-letter names** except for well-understood loop counters (`$i`, `$j`, `$k`) or math variables (`$x`, `$y`).

---

## 2. Variables

Use **camelCase** (PSR-1 recommendation).

```php
// ✅ Good
$userName = 'Alice';
$itemCount = 42;
$fetchedUsers = [];
$orderTotal = 99.95;

// ❌ Bad
$UserName = 'Alice';     // PascalCase is for classes
$user_name = 'Alice';    // snake_case (used in some legacy codebases, avoid in new code)
$usrnm = 'Alice';        // cryptic abbreviation
$strUserName = 'Alice';  // Hungarian notation
```

### Naming patterns by data type

| Data | Example |
|------|---------|
| String | `$firstName`, `$pageTitle` |
| Integer | `$itemCount`, `$maxRetries`, `$pageIndex` |
| Float | `$totalPrice`, `$taxRate` |
| Array | `$users`, `$orderItems`, `$selectedIds` (use **plural nouns**) |
| Object | `$userProfile`, `$requestConfig` |
| Null | same name as its non-null counterpart |
| Closure/Callable | `$callback`, `$formatter`, `$comparator` |

---

## 3. Constants

### Class constants — SCREAMING_SNAKE_CASE

```php
class HttpStatus
{
    public const OK = 200;
    public const NOT_FOUND = 404;
    public const INTERNAL_SERVER_ERROR = 500;
}

class Order
{
    public const MAX_ITEMS = 50;
    protected const DEFAULT_CURRENCY = 'USD';
    private const TAX_RATE = 0.2;
}
```

### Global constants — SCREAMING_SNAKE_CASE

```php
// ✅ Good
define('APP_ENV', 'production');
define('MAX_UPLOAD_SIZE', 10 * 1024 * 1024);

const DB_HOST = 'localhost';
const API_BASE_URL = 'https://api.example.com';

// ❌ Bad
define('appEnv', 'production');   // camelCase
define('App_Env', 'production');  // mixed case
```

### Interface constants

```php
interface Colorable
{
    public const COLOR_RED = 'red';
    public const COLOR_GREEN = 'green';
    public const COLOR_BLUE = 'blue';
}
```

---

## 4. Functions

Use **snake_case** for standalone (non-method) functions (PSR-1). Name functions with a **verb** or **verb phrase**.

```php
// ✅ Good — standalone functions
function get_user_by_id(string $id): User { ... }
function calculate_total_price(array $items): float { ... }
function format_date(\DateTimeInterface $date): string { ... }
function is_email_valid(string $email): bool { ... }

// ❌ Bad
function User(string $id): User { ... }      // noun only, uppercase
function GetUser(string $id): User { ... }   // PascalCase (class-style)
function g(string $id): User { ... }         // meaningless
```

> **Note:** In practice, most modern PHP code lives inside classes/namespaces. Standalone functions in namespaces use `snake_case` (PSR-1). Some teams (especially Laravel helpers) use `snake_case`. Class methods use `camelCase` — see Section 9.

### Common verb prefixes

| Prefix | Use case | Example |
|--------|----------|---------|
| `get` | Returns a value | `getUserById()`, `getTotal()` |
| `find` | Search, may return null | `findByEmail()`, `findOrFail()` |
| `fetch` | External data retrieval | `fetchFromApi()` |
| `set` | Sets / updates a value | `setUserName()` |
| `update` | Partial update | `updateProfile()` |
| `create` | Factory / instantiation | `createOrder()` |
| `make` | Same as create | `makeRequest()` |
| `build` | Builder pattern | `buildQuery()` |
| `handle` | Action/event handler | `handleSubmit()` |
| `process` | Multi-step action | `processPayment()` |
| `is` / `has` / `can` / `should` | Boolean predicate | `isAdmin()`, `hasPermission()` |
| `check` | Validation that may throw | `checkAuth()` |
| `validate` | Returns bool or throws | `validateEmail()` |
| `parse` | Transforms raw data | `parseResponse()` |
| `format` | Transforms for display | `formatCurrency()` |
| `calculate` / `compute` | Math / derived values | `calculateDiscount()` |
| `render` | Returns output | `renderView()` |
| `init` / `initialize` | Setup | `initDatabase()` |
| `reset` | Restore to defaults | `resetForm()` |
| `load` | Load data | `loadConfig()` |
| `save` / `store` | Persist data | `saveSettings()` |
| `delete` / `remove` | Deletion | `deleteUser()`, `removeItem()` |
| `clear` | Empty a collection | `clearCache()` |
| `send` | Communication | `sendEmail()` |
| `dispatch` | Events / jobs | `dispatchEvent()` |
| `subscribe` | Pub/sub | `subscribeToChannel()` |
| `resolve` | DI / promise resolution | `resolveService()` |
| `map` / `transform` | Shape transformation | `mapToDto()` |
| `convert` | Type conversion | `convertToCsv()` |

---

## 5. Classes

Use **PascalCase** (PSR-1 requirement). Name with a **noun** or **noun phrase**.

```php
// ✅ Good
class UserRepository { ... }
class ShoppingCart { ... }
class AuthenticationService { ... }
class HttpClient { ... }
class EventDispatcher { ... }
class PasswordHasher { ... }

// ❌ Bad
class userRepository { ... }   // camelCase
class manage_users { ... }     // snake_case
class DoUserStuff { ... }      // verb phrase
class USERREPOSITORY { ... }   // all caps
```

### Naming suffixes by responsibility

| Suffix | Purpose | Example |
|--------|---------|---------|
| `Service` | Business logic | `UserService`, `PaymentService` |
| `Repository` | Data access layer | `UserRepository`, `OrderRepository` |
| `Controller` | HTTP request handling | `UserController`, `AuthController` |
| `Middleware` | HTTP pipeline | `AuthMiddleware`, `CorsMiddleware` |
| `Factory` | Object creation | `UserFactory`, `OrderFactory` |
| `Builder` | Fluent construction | `QueryBuilder`, `MailBuilder` |
| `Handler` | Handles a request/command | `CreateOrderHandler` |
| `Command` | Command object (CQRS) | `CreateOrderCommand` |
| `Query` | Query object (CQRS) | `GetUserQuery` |
| `Event` | Domain event | `UserCreatedEvent`, `OrderPaidEvent` |
| `Listener` | Handles an event | `SendWelcomeEmailListener` |
| `Observer` | Observes model events | `UserObserver` |
| `Job` | Queued job | `SendEmailJob`, `ProcessPaymentJob` |
| `Policy` | Authorization rules | `UserPolicy`, `PostPolicy` |
| `Request` | Form request validation | `CreateUserRequest` |
| `Resource` | API response transformation | `UserResource`, `OrderResource` |
| `Collection` | Resource collection | `UserCollection` |
| `Provider` | Service registration | `AppServiceProvider` |
| `Seeder` | Database seeding | `UserSeeder`, `DatabaseSeeder` |
| `Migration` | DB migration class | auto-generated by framework |
| `Dto` / `DTO` | Data Transfer Object | `CreateUserDto`, `UserDto` |
| `VO` / `ValueObject` | Value object | `Money`, `Email`, `Address` |
| `Presenter` | View presenter | `UserPresenter` |
| `Transformer` | Data transformation | `UserTransformer` |
| `Resolver` | GraphQL / DI resolver | `UserResolver` |
| `Validator` | Custom validator | `UniqueEmailValidator` |
| `Exception` | Custom exception | `UserNotFoundException` |
| `Interface` | (avoid — use plain name) | `UserRepositoryInterface` or just `UserRepository` as interface |
| `Trait` | Reusable behavior | `HasTimestamps`, `SoftDeletes` |

---

## 6. Abstract Classes & Interfaces

### Abstract Classes

Prefix with `Abstract` or use `Base`:

```php
// ✅ Good
abstract class AbstractRepository
{
    abstract public function findById(int $id): ?object;
}

abstract class BaseController
{
    protected function jsonResponse(array $data): JsonResponse { ... }
}

// ❌ Bad
abstract class repositoryAbstract { ... }  // wrong order + case
```

### Interfaces

Use **PascalCase**. Two common conventions exist — choose one and stick to it:

**Option 1 — Descriptive name (preferred by PSR, Symfony):**

```php
// ✅ PSR / Symfony style
interface UserRepository
{
    public function findById(int $id): ?User;
    public function save(User $user): void;
}

interface Serializable
{
    public function serialize(): string;
}

interface LoggerInterface  // PSR-3 uses Interface suffix — acceptable
{
    public function log(string $level, string $message): void;
}
```

**Option 2 — `Interface` suffix (Laravel style, some teams):**

```php
// ✅ Also acceptable
interface UserRepositoryInterface { ... }
interface CacheInterface { ... }
```

**Option 3 — `I` prefix (avoid in modern PHP):**

```php
// ❌ Outdated — Microsoft/COM style, not idiomatic PHP
interface IUserRepository { ... }
```

---

## 7. Traits

Use **PascalCase**. Name traits as **adjectives** or **capability descriptions**. Popular convention: prefix with `Has` or `Can`, or use adjective forms:

```php
// ✅ Good
trait HasTimestamps
{
    public function getCreatedAt(): \DateTimeInterface { ... }
    public function getUpdatedAt(): \DateTimeInterface { ... }
}

trait SoftDeletes
{
    public function delete(): void { ... }
    public function restore(): void { ... }
}

trait HasUuid
{
    public function getUuid(): string { ... }
}

trait Cacheable
{
    public function getCacheKey(): string { ... }
}

trait Sluggable
{
    public function generateSlug(string $title): string { ... }
}

// ❌ Bad
trait userTimestamps { ... }   // camelCase
trait timestamps_trait { ... } // snake_case
trait TimestampsTrait { ... }  // redundant "Trait" suffix
```

---

## 8. Enums (PHP 8.1+)

### Enum name — PascalCase

```php
// ✅ Good — Pure enum
enum Direction
{
    case Up;
    case Down;
    case Left;
    case Right;
}

// ✅ Good — Backed enum (string)
enum UserRole: string
{
    case Admin = 'admin';
    case Editor = 'editor';
    case Viewer = 'viewer';
}

// ✅ Good — Backed enum (int)
enum HttpStatus: int
{
    case Ok = 200;
    case NotFound = 404;
    case InternalServerError = 500;
}

// ❌ Bad
enum userRole: string { ... }   // camelCase
enum USER_ROLE: string { ... }  // SCREAMING_SNAKE_CASE
```

### Enum cases — PascalCase

```php
// ✅ Good
enum Suit: string
{
    case Hearts = 'H';
    case Diamonds = 'D';
    case Clubs = 'C';
    case Spades = 'S';
}

// ❌ Bad — SCREAMING
enum Suit: string
{
    case HEARTS = 'H';
    case DIAMONDS = 'D';
}
```

### Using enums

```php
$role = UserRole::Admin;
$role->value;           // 'admin'
UserRole::from('admin'); // UserRole::Admin
```

---

## 9. Methods

Use **camelCase** (PSR-1). Name with a **verb** or **verb phrase**.

```php
class UserService
{
    // ✅ Good
    public function getUserById(int $id): ?User { ... }
    public function createUser(CreateUserDto $dto): User { ... }
    public function updateUserEmail(int $id, string $email): void { ... }
    public function deleteUser(int $id): void { ... }
    public function isAdmin(User $user): bool { ... }
    public function hasPermission(User $user, string $action): bool { ... }

    // ❌ Bad
    public function User(int $id): ?User { ... }        // noun only
    public function GET_USER(int $id): ?User { ... }    // screaming
    public function u(int $id): ?User { ... }           // meaningless
    public function get_user_by_id(int $id): ?User { } // snake_case (for standalone fn only)
}
```

### Fluent / Builder methods — return `$this`

```php
class QueryBuilder
{
    public function select(string ...$columns): static
    {
        $this->columns = $columns;
        return $this;
    }

    public function where(string $column, mixed $value): static
    {
        $this->conditions[] = [$column, $value];
        return $this;
    }

    public function orderBy(string $column, string $direction = 'ASC'): static
    {
        $this->orderBy = "$column $direction";
        return $this;
    }

    public function get(): array { ... }
}

// Usage
$users = $query->select('id', 'name')->where('active', true)->orderBy('name')->get();
```

### Accessor / Mutator (Laravel Eloquent)

```php
// Laravel 9+ (attribute casting style)
class User extends Model
{
    // Accessor
    protected function fullName(): Attribute
    {
        return Attribute::make(
            get: fn () => "{$this->first_name} {$this->last_name}",
        );
    }

    // Mutator
    protected function password(): Attribute
    {
        return Attribute::make(
            set: fn (string $value) => bcrypt($value),
        );
    }
}

// Legacy Laravel (still widely used)
public function getFullNameAttribute(): string
{
    return "{$this->first_name} {$this->last_name}";
}

public function setPasswordAttribute(string $value): void
{
    $this->attributes['password'] = bcrypt($value);
}
```

---

## 10. Properties & Fields

Use **camelCase** for instance properties:

```php
class Order
{
    // ✅ Good
    public string $orderId;
    public \DateTimeImmutable $createdAt;
    public float $totalAmount;
    public array $lineItems = [];

    // ❌ Bad
    public string $OrderId;      // PascalCase
    public \DateTimeImmutable $created_at;  // snake_case
    public float $total;         // too vague
}
```

### Static properties

```php
class HttpClient
{
    public static int $instanceCount = 0;           // camelCase
    private static ?self $instance = null;          // singleton pattern
    protected static string $defaultDriver = 'curl'; // camelCase
}
```

### Promoted constructor properties (PHP 8.0+)

```php
class User
{
    public function __construct(
        public readonly int $id,
        public string $name,
        public string $email,
        private string $passwordHash,
        protected \DateTimeImmutable $createdAt = new \DateTimeImmutable(),
    ) {}
}
```

---

## 11. Private / Protected Members

Use **camelCase** — no prefix needed. The visibility keyword already signals access level:

```php
class UserService
{
    // ✅ Good
    private UserRepository $repository;
    private LoggerInterface $logger;
    protected EventDispatcher $dispatcher;

    // ❌ Bad — underscore prefix is legacy, avoid in modern PHP
    private $_repository;
    private $m_logger;         // m_ prefix is from C++
    private $strUserName;      // Hungarian notation
}
```

> **Legacy pattern:** Some older codebases use `$_propertyName` for private/protected. Avoid in new code — the visibility modifier is sufficient.

---

## 12. Parameters

Use **camelCase**. Be descriptive:

```php
// ✅ Good
function createUser(string $firstName, string $lastName, UserRole $role): User { ... }
function fetchOrdersByDateRange(\DateTimeInterface $startDate, \DateTimeInterface $endDate): array { ... }

// ❌ Bad
function createUser(string $fn, string $ln, UserRole $r): User { ... }  // cryptic
function fetch(\DateTimeInterface $s, \DateTimeInterface $e): array { ... } // meaningless
```

### Variadic parameters

Use a clear **plural noun**:

```php
// ✅ Good
function logMessages(string ...$messages): void { ... }
function mergeArrays(array ...$arrays): array { ... }

// ❌ Bad
function log(string ...$args): void { ... }   // vague
function merge(array ...$a): array { ... }    // single letter
```

### Named arguments (PHP 8.0+)

Parameter names become part of the API when using named arguments — name them clearly:

```php
function createUser(
    string $firstName,
    string $lastName,
    string $email,
    UserRole $role = UserRole::Viewer,
    bool $isVerified = false,
): User { ... }

// Named argument call — parameter names are now public API
$user = createUser(
    firstName: 'Alice',
    lastName: 'Smith',
    email: 'alice@example.com',
    role: UserRole::Admin,
);
```

---

## 13. Namespaces

Use **PascalCase** for each segment (PSR-4 requirement). Structure mirrors the directory tree:

```php
// PSR-4: namespace maps to directory path
// App\Services\UserService → src/Services/UserService.php

namespace App\Services;
namespace App\Http\Controllers;
namespace App\Domain\User\ValueObjects;
namespace App\Infrastructure\Persistence\Doctrine;
namespace Vendor\Package\SubPackage;

// ✅ Good
namespace App\Models;
namespace App\Http\Middleware;
namespace App\Events;
namespace App\Exceptions;

// ❌ Bad
namespace App\services;         // lowercase
namespace app\Http\Controllers; // lowercase 'app'
namespace App\http_middleware;  // snake_case
```

### PSR-4 Autoloading Structure

```
src/
  Domain/
    User/
      User.php                      → App\Domain\User\User
      UserRepository.php            → App\Domain\User\UserRepository (interface)
      ValueObjects/
        Email.php                   → App\Domain\User\ValueObjects\Email
        UserId.php                  → App\Domain\User\ValueObjects\UserId
  Application/
    User/
      CreateUser/
        CreateUserCommand.php       → App\Application\User\CreateUser\CreateUserCommand
        CreateUserHandler.php       → App\Application\User\CreateUser\CreateUserHandler
  Infrastructure/
    Persistence/
      Doctrine/
        DoctrineUserRepository.php  → App\Infrastructure\Persistence\Doctrine\DoctrineUserRepository
```

---

## 14. Files & Directories

### Class files — PascalCase (required by PSR-4)

One class per file. The filename **must** match the class name exactly:

```
// ✅ Good
UserService.php
ShoppingCart.php
AuthMiddleware.php
CreateUserRequest.php
UserCreatedEvent.php

// ❌ Bad — won't autoload correctly
userService.php
user-service.php
user_service.php
```

### Non-class files — snake_case or kebab-case

```
helpers.php
bootstrap.php
config/database.php
config/mail.php
routes/web.php
routes/api.php
```

### Directory naming — PascalCase or snake_case depending on context

```
// ✅ PSR-4 source directories — PascalCase (maps to namespace)
src/
  Services/
  Repositories/
  Http/
    Controllers/
    Middleware/
  Domain/
  Infrastructure/

// ✅ Config, routes, resources — lowercase/kebab
config/
resources/
  views/
  lang/
database/
  migrations/
  seeders/
```

### Migration files (Laravel)

Auto-generated, use `snake_case` with timestamp:

```
2024_01_15_120000_create_users_table.php
2024_01_16_090000_add_email_verified_at_to_users_table.php
2024_02_01_000000_create_orders_table.php
```

---

## 15. Type Declarations & Generics (Psalm/PHPStan)

PHP lacks native generics, but Psalm and PHPStan support them via PHPDoc annotations.

### Type hints — always use them (PHP 7.4+/8.x)

```php
// ✅ PHP 8.x with full type declarations
class UserRepository
{
    public function findById(int $id): ?User { ... }
    public function findAll(): array { ... }  // weak — use @return User[]
    public function save(User $user): void { ... }
    public function delete(int $id): bool { ... }
}
```

### PHPDoc generics (Psalm / PHPStan)

Use **T** for primary type, **TKey/TValue** for collections:

```php
/**
 * @template T
 */
class Collection
{
    /** @var T[] */
    private array $items = [];

    /**
     * @param T $item
     */
    public function add(mixed $item): void
    {
        $this->items[] = $item;
    }

    /**
     * @return T[]
     */
    public function all(): array
    {
        return $this->items;
    }
}

/**
 * @template TKey of array-key
 * @template TValue
 * @param array<TKey, TValue> $array
 * @param callable(TValue): bool $predicate
 * @return array<TKey, TValue>
 */
function array_filter_values(array $array, callable $predicate): array
{
    return array_filter($array, $predicate);
}
```

### Common PHPDoc type patterns

```php
/** @var User[] */
private array $users;

/** @var array<string, mixed> */
private array $config;

/** @var array<int, User> */
private array $userMap;

/** @var non-empty-list<string> */
private array $roles;

/** @var callable(User): bool */
private $predicate;

/** @var \Closure(string, int): void */
private \Closure $callback;
```

---

## 16. Boolean Variables

Use **`is`, `has`, `can`, `should`, `was`, `did`** prefixes:

```php
// ✅ Good
$isLoading = false;
$isAuthenticated = false;
$isActive = true;
$hasErrors = false;
$hasPermission = true;
$canEdit = false;
$canDelete = false;
$shouldRefetch = true;
$wasModified = false;
$didSubmit = false;

// In classes / DTOs
class User
{
    public bool $isActive;
    public bool $isVerified;
    public bool $hasSubscription;
}

// ❌ Bad
$loading = false;           // ambiguous
$authenticated = false;     // adjective without prefix
$errors = false;            // sounds like array of errors
$editPermission = false;    // noun phrase
```

---

## 17. Magic Methods

PHP magic methods are always **lowercase with double underscores** (language requirement):

```php
class User
{
    // Lifecycle
    public function __construct(...) { }
    public function __destruct() { }

    // Property access
    public function __get(string $name): mixed { }
    public function __set(string $name, mixed $value): void { }
    public function __isset(string $name): bool { }
    public function __unset(string $name): void { }

    // Serialization
    public function __sleep(): array { }
    public function __wakeup(): void { }
    public function __serialize(): array { }
    public function __unserialize(array $data): void { }

    // String / invokable
    public function __toString(): string { }
    public function __invoke(mixed ...$args): mixed { }

    // Cloning
    public function __clone(): void { }

    // Static calls
    public static function __callStatic(string $name, array $args): mixed { }
    public function __call(string $name, array $args): mixed { }

    // Debugging
    public function __debugInfo(): array { }
}
```

---

## 18. Exceptions

Use **PascalCase** with `Exception` suffix. Name the exception after what went wrong:

```php
// ✅ Good
class UserNotFoundException extends \RuntimeException { }
class InvalidEmailException extends \InvalidArgumentException { }
class PaymentFailedException extends \RuntimeException { }
class AuthorizationException extends \RuntimeException { }
class DuplicateEmailException extends \DomainException { }
class InsufficientFundsException extends \DomainException { }
class ApiConnectionException extends \RuntimeException { }

// ❌ Bad
class UserException { }         // too vague
class Exception2 { }            // meaningless
class BadUserException { }      // "bad" adds no info
class UserNotFoundError { }     // should end in Exception in PHP
```

### Exception hierarchy

```php
// Domain exceptions
class DomainException extends \DomainException { }
class UserNotFoundException extends DomainException { }
class OrderNotFoundException extends DomainException { }

// Infrastructure exceptions
class DatabaseException extends \RuntimeException { }
class ConnectionTimeoutException extends DatabaseException { }

// Application exceptions
class ValidationException extends \InvalidArgumentException
{
    /** @param array<string, string[]> $errors */
    public function __construct(
        private readonly array $errors,
        string $message = 'Validation failed.',
    ) {
        parent::__construct($message);
    }

    /** @return array<string, string[]> */
    public function getErrors(): array
    {
        return $this->errors;
    }
}
```

---

## 19. Event Handlers & Listeners

### Events — PascalCase + `Event` suffix (or past tense noun)

```php
// ✅ Both styles are acceptable

// Option 1 — Event suffix (explicit)
class UserCreatedEvent { }
class OrderPaidEvent { }
class PasswordResetRequestedEvent { }

// Option 2 — Past tense without suffix (DDD style)
class UserRegistered { }
class OrderPlaced { }
class PasswordChanged { }
```

### Listeners — PascalCase + `Listener` suffix

```php
// ✅ Good
class SendWelcomeEmailListener
{
    public function handle(UserCreatedEvent $event): void { ... }
}

class NotifyAdminOnOrderListener
{
    public function handle(OrderPaidEvent $event): void { ... }
}
```

### Observers — PascalCase + `Observer` suffix

```php
class UserObserver
{
    public function created(User $user): void { ... }
    public function updated(User $user): void { ... }
    public function deleted(User $user): void { ... }
    public function restored(User $user): void { ... }
    public function forceDeleted(User $user): void { ... }
}
```

### Subscribers

```php
// Symfony EventSubscriber
class UserEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            UserCreatedEvent::class => 'onUserCreated',
            UserDeletedEvent::class => ['onUserDeleted', 10], // priority
        ];
    }

    public function onUserCreated(UserCreatedEvent $event): void { ... }
    public function onUserDeleted(UserDeletedEvent $event): void { ... }
}
```

---

## 20. Laravel Conventions

Laravel has its own opinionated naming on top of PSR standards:

### Models — singular PascalCase

```php
// ✅ Good
class User extends Model { }
class Order extends Model { }
class BlogPost extends Model { }

// ❌ Bad
class Users extends Model { }      // plural
class blog_post extends Model { }  // snake_case
```

### Eloquent relationships

```php
class User extends Model
{
    // hasMany — plural
    public function orders(): HasMany
    {
        return $this->hasMany(Order::class);
    }

    // belongsTo — singular
    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    // belongsToMany — plural
    public function permissions(): BelongsToMany
    {
        return $this->belongsToMany(Permission::class);
    }

    // hasOne — singular
    public function profile(): HasOne
    {
        return $this->hasOne(UserProfile::class);
    }
}
```

### Controllers — singular PascalCase + `Controller`

```php
// ✅ Good
class UserController extends Controller { }
class OrderController extends Controller { }
class AuthController extends Controller { }

// Resource controller actions (follow exactly)
class PostController extends Controller
{
    public function index(): View { }       // list all
    public function create(): View { }      // show create form
    public function store(Request $r): RedirectResponse { }  // save new
    public function show(Post $post): View { } // show one
    public function edit(Post $post): View { } // show edit form
    public function update(Request $r, Post $post): RedirectResponse { } // save edit
    public function destroy(Post $post): RedirectResponse { } // delete
}
```

### Routes

```php
// ✅ Route names — snake_case or dot notation
Route::get('/users', [UserController::class, 'index'])->name('users.index');
Route::get('/users/{user}', [UserController::class, 'show'])->name('users.show');
Route::post('/users', [UserController::class, 'store'])->name('users.store');

// ✅ Route parameters — camelCase (matches model binding)
Route::get('/users/{userId}/orders', [OrderController::class, 'index']);
Route::get('/blog/{blogPost}', [BlogPostController::class, 'show']); // model binding
```

### Blade templates — kebab-case

```
resources/views/
  users/
    index.blade.php
    show.blade.php
    create.blade.php
    edit.blade.php
  components/
    user-card.blade.php
    nav-bar.blade.php
    alert-message.blade.php
  layouts/
    app.blade.php
    guest.blade.php
```

### Database — snake_case

```php
// Table names — plural snake_case
'users', 'orders', 'blog_posts', 'user_roles'

// Column names — snake_case
'first_name', 'last_name', 'email_verified_at', 'created_at', 'updated_at'

// Foreign keys — singular_snake + _id
'user_id', 'order_id', 'blog_post_id'

// Pivot tables — alphabetical singular_snake
'role_user', 'permission_role', 'post_tag'
```

### Config keys — snake_case

```php
// config/app.php
return [
    'name' => 'My App',
    'timezone' => 'UTC',
    'locale' => 'en',
    'debug_mode' => false,
];

config('app.debug_mode');
```

---

## 21. Symfony Conventions

### Service classes — PascalCase + descriptive suffix

```php
// ✅ Good
class UserManager { }               // manages lifecycle
class UserProvider { }              // provides users (security)
class PasswordEncoder { }           // encodes passwords
class TokenGenerator { }            // generates tokens
class FormFactory { }               // creates forms
class EventSubscriber { }
```

### Service IDs (DI container) — FQCN or snake_case

```yaml
# services.yaml
services:
    App\Service\UserService: ~           # FQCN (preferred in Symfony 4+)
    app.service.user_service:            # legacy snake_case alias
        class: App\Service\UserService
```

### Twig templates — snake_case

```
templates/
  user/
    index.html.twig
    show.html.twig
    _form.html.twig          ← partial, prefixed with _
  layout/
    base.html.twig
    _navbar.html.twig
```

### Form types — PascalCase + `Type` suffix

```php
class UserType extends AbstractType { }
class CreateOrderType extends AbstractType { }
class LoginFormType extends AbstractType { }
```

### Voters — PascalCase + `Voter` suffix

```php
class UserVoter extends Voter { }
class PostVoter extends Voter { }
```

---

## 22. Test Files & Test Identifiers

### Test file naming

```
Tests/
  Unit/
    UserServiceTest.php         ← unit test
    UserRepositoryTest.php
  Integration/
    UserControllerTest.php      ← integration test
  Feature/
    CreateUserTest.php          ← feature test
  E2E/
    UserRegistrationTest.php    ← end-to-end
```

### Test class — PascalCase + `Test` suffix

```php
class UserServiceTest extends TestCase { }
class UserControllerTest extends TestCase { }
class CreateOrderHandlerTest extends TestCase { }
```

### Test methods — camelCase, descriptive

```php
class UserServiceTest extends TestCase
{
    // ✅ PHPUnit style — camelCase with test prefix
    public function testGetUserByIdReturnsUserWhenFound(): void { ... }
    public function testGetUserByIdThrowsExceptionWhenNotFound(): void { ... }
    public function testCreateUserReturnsNewUserWithCorrectData(): void { ... }

    // ✅ PHPUnit with @test annotation — plain English (preferred by many)
    /** @test */
    public function it_returns_the_user_when_found(): void { ... }

    /** @test */
    public function it_throws_user_not_found_exception_when_id_is_invalid(): void { ... }

    // ✅ PHPUnit #[Test] attribute (PHP 8.x / PHPUnit 10+)
    #[\PHPUnit\Framework\Attributes\Test]
    public function it_creates_a_user_with_hashed_password(): void { ... }
}
```

### Data providers

```php
/** @return array<string, array{string, bool}> */
public static function provideEmailValidationCases(): array
{
    return [
        'valid email'          => ['user@example.com', true],
        'missing @ symbol'     => ['userexample.com', false],
        'empty string'         => ['', false],
        'international domain' => ['user@münchen.de', true],
    ];
}

#[\PHPUnit\Framework\Attributes\DataProvider('provideEmailValidationCases')]
public function testEmailValidation(string $email, bool $expected): void
{
    $this->assertSame($expected, $this->validator->isValid($email));
}
```

### Test variables

```php
// ✅ Use 'mock', 'stub', 'spy', 'fake', 'dummy' prefixes (xUnit patterns)
$mockUserRepository = $this->createMock(UserRepository::class);
$stubMailer = $this->createStub(Mailer::class);

// ✅ Use 'expected' / 'actual' for assertions
$expectedUser = new User(id: 1, name: 'Alice');
$actualUser = $this->service->getUserById(1);
$this->assertEquals($expectedUser, $actualUser);

// ✅ Use 'sut' (System Under Test) for the class being tested
$sut = new UserService($mockUserRepository, $stubMailer);
```

---

## 23. Abbreviations & Acronyms

### Well-known abbreviations — camelCase treatment

```php
// ✅ Good
$apiUrl = 'https://api.example.com';
$htmlContent = '<p>Hello</p>';
$userId = 123;
$httpClient = new HttpClient();
$xmlParser = new XmlParser();

// ❌ Bad
$APIUrl = '...';       // inconsistent
$HTMLContent = '...';  // inconsistent
$userID = 123;         // ambiguous — looks like constant
```

### Acronyms in PascalCase — capitalize only the first letter

```php
// ✅ Good
class HttpClient { }       // not HTTPClient
class XmlParser { }        // not XMLParser
class JsonSerializer { }   // not JSONSerializer
class HtmlSanitizer { }    // not HTMLSanitizer
class SqlBuilder { }       // not SQLBuilder
class ApiGateway { }       // not APIGateway

// Exception: 2-letter acronyms are usually all caps
class DbConnection { }     // or DBConnection (both acceptable)
$id = 1;                   // not $ID

// PSR-3 named its interface LoggerInterface using full caps for common word
// This is an exception, not the rule
```

---

## 24. Naming Anti-patterns

### ❌ Generic / meaningless names

```php
// Bad
$data = $this->userRepository->findAll();
$result = $this->orderService->process($order);
$temp = $this->calculator->calculate();
$obj = new UserService();
$info = $this->getUserInfo($id);

// Good
$users = $this->userRepository->findAll();
$processedOrder = $this->orderService->process($order);
$orderTotal = $this->calculator->calculateOrderTotal();
$userService = new UserService();
$userProfile = $this->getUserProfile($id);
```

### ❌ Misleading names

```php
// Implies array but holds count
$users = 42;                    // should be $userCount

// Implies boolean but returns object
$isUser = $this->getUser($id);  // should be $user

// Name lies about return type
public function getUsers(): User { ... }   // returns one, name says many
public function findUser(): array { ... }  // returns array, name says one
```

### ❌ Unnecessary context repetition

```php
// In class UserService — "user" is redundant in method names
class UserService
{
    public function getUserById(): User { ... }      // ❌ "user" obvious from class
    public function getById(): User { ... }          // ✅ better

    public function createUserAccount(): User { ... } // ❌
    public function createAccount(): User { ... }     // ✅
}

// In a user array/object — "user" is redundant
$user = [
    'userName' => 'Alice',   // ❌
    'name' => 'Alice',        // ✅
    'userEmail' => 'a@x.com', // ❌
    'email' => 'a@x.com',     // ✅
];
```

### ❌ Numeric suffixes

```php
// Bad — what's the difference?
$user1 = $this->getUser($id1);
$user2 = $this->getUser($id2);

// Good — be specific
$currentUser = $this->getUser($currentUserId);
$targetUser = $this->getUser($targetUserId);
```

### ❌ Negated booleans

```php
// Bad — double negatives are confusing
$isNotActive = !$user->isActive();
if (!$isNotActive) { ... }   // confusing!

// Good
$isActive = $user->isActive();
if ($isActive) { ... }
```

### ❌ Manager / Helper / Util classes

These names are code smells — they become dumping grounds:

```php
// ❌ Bad — vague class names
class UserManager { }     // manages what exactly?
class StringHelper { }    // helps with what?
class Utils { }           // does what?
class Helpers { }         // vague

// ✅ Good — specific responsibility
class UserPasswordHasher { }     // specific what it does
class SlugGenerator { }          // specific
class DateRangeFormatter { }     // specific
class EmailNormalizer { }        // specific
```

---

## 25. Quick Reference Cheatsheet

| Construct | Convention | Example |
|-----------|-----------|---------|
| Variable | camelCase | `$userCount`, `$isLoading` |
| Global constant | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_URL` |
| Class constant | SCREAMING_SNAKE_CASE | `self::MAX_ITEMS`, `HttpStatus::NOT_FOUND` |
| Standalone function | snake_case | `get_user_by_id()`, `format_date()` |
| Class | PascalCase + noun | `UserService`, `ShoppingCart` |
| Abstract class | `Abstract` / `Base` + PascalCase | `AbstractRepository`, `BaseController` |
| Interface | PascalCase (no `I`) | `UserRepository`, `Serializable` |
| Trait | PascalCase + adjective | `HasTimestamps`, `SoftDeletes` |
| Enum | PascalCase | `UserRole`, `HttpStatus` |
| Enum case | PascalCase | `UserRole::Admin`, `Direction::Up` |
| Method | camelCase + verb | `getUserById()`, `isAdmin()` |
| Property | camelCase | `$firstName`, `$createdAt` |
| Static property | camelCase | `$instanceCount` |
| Parameter | camelCase | `$userId`, `$startDate` |
| Variadic parameter | camelCase plural | `...$messages`, `...$items` |
| Namespace segment | PascalCase | `App\Services`, `App\Http\Controllers` |
| File (class) | PascalCase.php | `UserService.php`, `UserController.php` |
| File (non-class) | snake_case.php | `helpers.php`, `bootstrap.php` |
| Directory (source) | PascalCase | `Services/`, `Http/Controllers/` |
| Directory (other) | lowercase/kebab | `config/`, `resources/views/` |
| Boolean variable | `is/has/can/should` + adj | `$isActive`, `$hasErrors`, `$canEdit` |
| Exception | PascalCase + `Exception` | `UserNotFoundException` |
| Event | PascalCase + `Event` / past tense | `UserCreatedEvent`, `UserRegistered` |
| Listener | PascalCase + `Listener` | `SendWelcomeEmailListener` |
| Observer | PascalCase + `Observer` | `UserObserver` |
| Decorator (class) | PascalCase + class name | `CachingUserRepository` |
| Magic method | `__` + lowercase | `__construct()`, `__toString()` |
| Test class | PascalCase + `Test` | `UserServiceTest` |
| Test method | camelCase or `it_snake_case` | `testGetUser()` / `it_finds_user()` |
| Mock/stub/spy | prefix + name | `$mockRepo`, `$stubMailer` |
| Laravel Model | singular PascalCase | `User`, `BlogPost` |
| Laravel Controller | singular + `Controller` | `UserController` |
| Laravel Form Request | PascalCase + `Request` | `CreateUserRequest` |
| Laravel Resource | PascalCase + `Resource` | `UserResource` |
| Laravel Job | PascalCase + `Job` | `SendEmailJob` |
| Laravel Policy | PascalCase + `Policy` | `UserPolicy` |
| Laravel Event | PascalCase + `Event` | `UserCreated` |
| DB table | plural snake_case | `users`, `blog_posts` |
| DB column | snake_case | `first_name`, `created_at` |
| DB foreign key | singular_snake + `_id` | `user_id`, `order_id` |
| Blade template | snake_case.blade.php | `user-card.blade.php` |

---

## 26. References & Further Reading

| Resource | URL |
|----------|-----|
| **PSR-1: Basic Coding Standard** | https://www.php-fig.org/psr/psr-1/ |
| **PSR-12: Extended Coding Style** | https://www.php-fig.org/psr/psr-12/ |
| **PSR-4: Autoloading Standard** | https://www.php-fig.org/psr/psr-4/ |
| **PHP-FIG Standards** | https://www.php-fig.org/psr/ |
| **PHP The Right Way** | https://phptherightway.com |
| **Laravel Naming Conventions** | https://laravel.com/docs |
| **Symfony Coding Standards** | https://symfony.com/doc/current/contributing/code/standards.html |
| **PHPStan** | https://phpstan.org |
| **Psalm** | https://psalm.dev |
| **PHP CS Fixer** | https://github.com/PHP-CS-Fixer/PHP-CS-Fixer |
| **PHP_CodeSniffer** | https://github.com/squizlabs/PHP_CodeSniffer |
| **PHPUnit** | https://phpunit.de |
| **Clean Code PHP** | https://github.com/piotrplenik/clean-code-php |

### Recommended PHP CS Fixer / PHPCS config

```php
// .php-cs-fixer.php
$finder = PhpCsFixer\Finder::create()->in(__DIR__ . '/src');

return (new PhpCsFixer\Config())
    ->setRules([
        '@PSR12' => true,
        '@PHP81Migration' => true,
        'array_syntax' => ['syntax' => 'short'],
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
        'not_operator_with_successor_space' => true,
        'trailing_comma_in_multiline' => true,
    ])
    ->setFinder($finder);
```

### PHPStan level config

```neon
# phpstan.neon
parameters:
    level: 9               # max strictness
    paths:
        - src
        - tests
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
```

---

*Last updated: 2026 — Based on PHP 8.3, PSR-12, Laravel 11, Symfony 7*
