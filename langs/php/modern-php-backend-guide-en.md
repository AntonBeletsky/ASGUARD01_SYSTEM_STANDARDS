# THE COMPLETE MODERN PHP BACKEND REFERENCE
## Canonical AI Guide · PHP 8.1 – 8.4 · Clean Code · Production-Ready

> **Edition:** 2025 | **Coverage:** PHP 8.1, 8.2, 8.3, 8.4 | **Paradigm:** Clean Code · SOLID · DDD · PSR
>
> This document is a **self-sufficient, authoritative reference** for writing clean, secure, and
> maintainable PHP backend code without frameworks. Every section contains canonical patterns,
> anti-patterns with explanations, and production-grade code. Treat every rule here as an
> absolute standard unless a specific context demands deviation — and that deviation must be
> explicitly justified in code comments.

---

## TABLE OF CONTENTS

1.  [Philosophy of Modern PHP](#1-philosophy-of-modern-php)
2.  [Environment & Toolchain](#2-environment--toolchain)
3.  [Strict Typing — The Non-Negotiable Foundation](#3-strict-typing--the-non-negotiable-foundation)
4.  [Naming Conventions & Code Structure](#4-naming-conventions--code-structure)
5.  [OOP: Classes, Interfaces, Traits, Enums](#5-oop-classes-interfaces-traits-enums)
6.  [SOLID Principles — Deep Dive](#6-solid-principles--deep-dive)
7.  [Design Patterns](#7-design-patterns)
8.  [Domain-Driven Design (DDD) in PHP](#8-domain-driven-design-ddd-in-php)
9.  [Error Handling & Exceptions](#9-error-handling--exceptions)
10. [Database Layer (PDO)](#10-database-layer-pdo)
11. [Security — Comprehensive Guide](#11-security--comprehensive-guide)
12. [HTTP: Requests & Responses](#12-http-requests--responses)
13. [Routing](#13-routing)
14. [Middleware Pipeline](#14-middleware-pipeline)
15. [Dependency Injection & Service Container](#15-dependency-injection--service-container)
16. [Configuration & Environment](#16-configuration--environment)
17. [Filesystem Operations](#17-filesystem-operations)
18. [Caching Strategies](#18-caching-strategies)
19. [Logging](#19-logging)
20. [Input Validation](#20-input-validation)
21. [REST API Design & Implementation](#21-rest-api-design--implementation)
22. [Authentication & Authorization](#22-authentication--authorization)
23. [Sessions](#23-sessions)
24. [Email](#24-email)
25. [Queues & Background Jobs](#25-queues--background-jobs)
26. [Testing — Unit, Integration, API](#26-testing--unit-integration-api)
27. [Composer & Package Management](#27-composer--package-management)
28. [PSR Standards — Full Reference](#28-psr-standards--full-reference)
29. [Performance Optimization](#29-performance-optimization)
30. [CLI Applications](#30-cli-applications)
31. [Project Structure](#31-project-structure)
32. [Deployment & Infrastructure](#32-deployment--infrastructure)
33. [Modern PHP 8.x Features — Complete Reference](#33-modern-php-8x-features--complete-reference)
34. [Advanced Patterns: CQRS, Event Sourcing, Hexagonal Architecture](#34-advanced-patterns-cqrs-event-sourcing-hexagonal-architecture)
35. [API Documentation (OpenAPI)](#35-api-documentation-openapi)
36. [Internationalization & Localization](#36-internationalization--localization)
37. [Quality Gates & Checklists](#37-quality-gates--checklists)
38. [Glossary](#38-glossary)

---

## 1. PHILOSOPHY OF MODERN PHP

### 1.1 Core Tenets

Modern PHP is a **statically-analysable, strictly-typed, enterprise-grade language**. The era of
PHP as a "templating glue" is over. Today PHP runs at scale at Slack, Wikipedia, Etsy, and
countless financial systems. The language has a rich type system, native fibers, JIT compilation,
and a mature PSR ecosystem.

**The modern PHP developer's creed:**

| Principle | Meaning |
|---|---|
| **Explicit over implicit** | Types everywhere; no silent coercions; no magic |
| **Fail fast** | Errors surface immediately and loudly; no silent failures |
| **Immutability by default** | Data does not mutate unless an explicit mutation is the intent |
| **Single responsibility** | One class = one reason to change; one method = one action |
| **Constructor injection** | No global state; no service locators inside business logic |
| **Program to interfaces** | Depend on abstractions, not concrete implementations |
| **Tests as executable specification** | Every behaviour has a test; tests document intent |

### 1.2 The Absolute Prohibitions

These patterns are **banned** in all modern PHP code, with no exceptions:

```php
<?php
// ❌ BANNED — global variables
global $db;
$GLOBALS['config'] = [];

// ❌ BANNED — mixing HTML and PHP logic
echo "<div>" . $user->name . "</div>";

// ❌ BANNED — functions / methods without type declarations
function getUser($id) { ... }
function process($data): mixed { ... }  // mixed is a last resort, not a default

// ❌ BANNED — error suppression operator
$result = @file_get_contents($url);

// ❌ BANNED — die() / exit() inside business logic
if (!$user) { die('User not found'); }

// ❌ BANNED — accessing superglobals inside domain / service classes
$name = $_GET['name'];
$body = $_POST;

// ❌ BANNED — string interpolation in SQL
$sql = "SELECT * FROM users WHERE id = {$_GET['id']}";

// ❌ BANNED — weak password hashing
$hash = md5($password);
$hash = sha1($password);
$hash = crypt($password);

// ❌ BANNED — catch-all with empty bodies
try {
    riskyOperation();
} catch (\Exception $e) {
    // swallowing exceptions silently
}

// ❌ BANNED — var_dump / print_r in production code
var_dump($user);
print_r($data);

// ❌ BANNED — static methods for everything (static cling)
class UserService {
    public static function create(array $data): User { ... }
    public static function find(int $id): ?User { ... }
}

// ❌ BANNED — new inside business logic (violates DIP)
class OrderService {
    public function place(array $data): Order {
        $repo = new MysqlOrderRepository(); // hard dependency!
        $mailer = new SmtpMailer();         // untestable!
    }
}
```

---

## 2. ENVIRONMENT & TOOLCHAIN

### 2.1 Required Stack

```
PHP        >= 8.3 (8.4 recommended for property hooks + array_find)
Composer   >= 2.7
PHPStan    >= 1.12  at level max  (or Psalm at level 1)
PHP-CS-Fixer >= 3.50
PHPUnit    >= 11.0
```

### 2.2 php.ini — Production Settings

```ini
;; === Core ===
expose_php               = Off
display_errors           = Off
display_startup_errors   = Off
log_errors               = On
error_log                = /var/log/php/error.log
error_reporting          = E_ALL
zend.exception_ignore_args = On      ; don't leak args in stack traces (PHP 8.0+)

;; === Security ===
allow_url_fopen          = Off
allow_url_include        = Off
disable_functions        = exec,passthru,shell_exec,system,proc_open,popen,\
                           curl_multi_exec,parse_ini_file,show_source

;; === OPcache (mandatory on production) ===
opcache.enable                 = 1
opcache.enable_cli             = 0
opcache.memory_consumption     = 256
opcache.interned_strings_buffer= 16
opcache.max_accelerated_files  = 20000
opcache.validate_timestamps    = 0   ; NEVER revalidate on production
opcache.revalidate_freq        = 0
opcache.save_comments          = 1   ; needed for annotations / docblocks
opcache.jit                    = 1255
opcache.jit_buffer_size        = 128M

;; === Session ===
session.use_strict_mode   = 1
session.cookie_httponly   = 1
session.cookie_secure     = 1
session.cookie_samesite   = Strict
session.gc_maxlifetime    = 1440
session.sid_length        = 48
session.sid_bits_per_character = 6

;; === Upload ===
file_uploads              = On
upload_max_filesize       = 20M
post_max_size             = 25M
max_execution_time        = 30
max_input_time            = 30
memory_limit              = 256M
```

### 2.3 phpstan.neon — Maximum Strictness

```neon
includes:
    - vendor/phpstan/phpstan-strict-rules/rules.neon

parameters:
    level: max
    paths:
        - src
        - tests
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
    checkMissingCallableSignature: true
    reportUnmatchedIgnoredErrors: true
    treatPhpDocTypesAsCertain: false
    strictRules:
        allRules: true
    ignoreErrors:
        # Only add here with a comment explaining WHY
```

### 2.4 php-cs-fixer — .php-cs-fixer.dist.php

```php
<?php

$finder = PhpCsFixer\Finder::create()
    ->in(__DIR__ . '/src')
    ->in(__DIR__ . '/tests')
    ->name('*.php');

return (new PhpCsFixer\Config())
    ->setRules([
        '@PER-CS2.0'                         => true,
        '@PHP83Migration'                    => true,
        'declare_strict_types'               => true,
        'strict_param'                       => true,
        'array_syntax'                       => ['syntax' => 'short'],
        'ordered_imports'                    => ['sort_algorithm' => 'alpha'],
        'no_unused_imports'                  => true,
        'single_quote'                       => true,
        'trailing_comma_in_multiline'        => true,
        'phpdoc_align'                       => true,
        'phpdoc_order'                       => true,
        'return_type_declaration'            => ['space_before' => 'none'],
    ])
    ->setFinder($finder)
    ->setRiskyAllowed(true);
```

### 2.5 composer.json — Canonical Template

```json
{
    "name": "vendor/project",
    "description": "Modern PHP Application",
    "type": "project",
    "license": "proprietary",
    "require": {
        "php":          ">=8.3",
        "ext-pdo":      "*",
        "ext-json":     "*",
        "ext-mbstring": "*",
        "ext-openssl":  "*",
        "ext-redis":    "*",
        "ext-intl":     "*"
    },
    "require-dev": {
        "phpunit/phpunit":                   "^11.0",
        "phpstan/phpstan":                   "^1.12",
        "phpstan/phpstan-strict-rules":      "^1.6",
        "friendsofphp/php-cs-fixer":         "^3.50",
        "fakerphp/faker":                    "^1.23",
        "phpunit/php-code-coverage":         "^11.0"
    },
    "autoload": {
        "psr-4": { "App\\": "src/" }
    },
    "autoload-dev": {
        "psr-4": { "Tests\\": "tests/" }
    },
    "scripts": {
        "test":       "phpunit --colors=always",
        "test:cover": "phpunit --coverage-html=.coverage",
        "analyze":    "phpstan analyse --memory-limit=512M",
        "cs:fix":     "php-cs-fixer fix",
        "cs:check":   "php-cs-fixer fix --dry-run --diff",
        "check":      ["@cs:check", "@analyze", "@test"]
    },
    "config": {
        "sort-packages":       true,
        "optimize-autoloader": true,
        "preferred-install":   "dist",
        "allow-plugins": {
            "phpstan/extension-installer": true
        }
    }
}
```

---

## 3. STRICT TYPING — THE NON-NEGOTIABLE FOUNDATION

### 3.1 The declare Directive — Always, No Exceptions

**Every single PHP file begins with this exact header. Without exception. No file is exempt.**

```php
<?php

declare(strict_types=1);

namespace App\Domain\User;
```

What `strict_types=1` enforces:
- Scalar parameters accept **only the exact declared type** — `"5"` passed to `int` throws `TypeError`
- Return types are strictly enforced
- Silent coercion (`true` → `1`, `"3.14"` → `3`) is eliminated entirely
- Type errors are `TypeError` exceptions, not silent wrong behaviour

### 3.2 The Complete PHP 8.x Type System

```php
<?php

declare(strict_types=1);

// ── Scalar types ─────────────────────────────────────────────────────────────
function add(int $a, int $b): int            { return $a + $b; }
function ratio(float $n, float $d): float    { return $n / $d; }
function upper(string $s): string            { return strtoupper($s); }
function toggle(bool $flag): bool            { return !$flag; }

// ── Nullable ──────────────────────────────────────────────────────────────────
function findUser(int $id): ?User { /* returns User or null */ }

// ── void — the function returns no value ─────────────────────────────────────
function logMessage(string $message): void { /* no return statement */ }

// ── never — the function NEVER returns (throws or exits) ─────────────────────
function throwNotFound(string $resource): never
{
    throw new NotFoundException($resource);
}

// ── Union types (PHP 8.0+) ────────────────────────────────────────────────────
function parseId(int|string $id): int
{
    return is_string($id) ? (int) $id : $id;
}

// ── Intersection types (PHP 8.1+) ─────────────────────────────────────────────
function processSizedIterable(Countable&Iterator $col): void { }

// ── DNF types — Disjunctive Normal Form (PHP 8.2+) ───────────────────────────
function accept((Countable&Stringable)|null $value): void { }

// ── mixed — use ONLY when the type is genuinely unknowable ───────────────────
function jsonDecode(string $json): mixed
{
    return json_decode($json, true, 512, JSON_THROW_ON_ERROR);
}

// ── Generics via PHPDoc (for static analysis) ────────────────────────────────
/**
 * @template T of object
 * @param array<T>    $items
 * @param callable(T): bool $predicate
 * @return array<T>
 */
function filter(array $items, callable $predicate): array
{
    return array_values(array_filter($items, $predicate));
}

/**
 * @param array<string, int> $scores
 * @return array<string, int>
 */
function topScores(array $scores, int $n): array
{
    arsort($scores);
    return array_slice($scores, 0, $n, preserve_keys: true);
}
```

### 3.3 Value Objects — Type-Safe Wrappers

Value Objects are one of the most powerful tools in PHP. They replace primitive obsession with
semantically meaningful, self-validating types.

```php
<?php

declare(strict_types=1);

namespace App\Domain\ValueObject;

// ── Email ─────────────────────────────────────────────────────────────────────
final class Email implements \Stringable
{
    private readonly string $value;

    public function __construct(string $raw)
    {
        $normalized = mb_strtolower(trim($raw));

        if (!filter_var($normalized, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException(
                "'{$raw}' is not a valid email address."
            );
        }

        $this->value = $normalized;
    }

    public function toString(): string  { return $this->value; }
    public function domain(): string    { return substr($this->value, strpos($this->value, '@') + 1); }
    public function localPart(): string { return strstr($this->value, '@', before_needle: true); }

    public function equals(self $other): bool { return $this->value === $other->value; }

    public function __toString(): string { return $this->value; }
}

// ── Money ─────────────────────────────────────────────────────────────────────
final class Money
{
    public function __construct(
        private readonly int    $amount,   // in smallest currency unit (cents, pence, kopecks)
        private readonly string $currency, // ISO 4217: USD, EUR, GBP
    ) {
        if ($this->amount < 0) {
            throw new \InvalidArgumentException('Money amount cannot be negative.');
        }
        if (!preg_match('/^[A-Z]{3}$/', $this->currency)) {
            throw new \InvalidArgumentException("Invalid currency code: '{$this->currency}'.");
        }
    }

    public static function zero(string $currency): self { return new self(0, $currency); }

    public function add(self $other): self
    {
        $this->guardSameCurrency($other);
        return new self($this->amount + $other->amount, $this->currency);
    }

    public function subtract(self $other): self
    {
        $this->guardSameCurrency($other);
        if ($other->amount > $this->amount) {
            throw new \DomainException('Subtraction would result in negative money.');
        }
        return new self($this->amount - $other->amount, $this->currency);
    }

    public function multiply(float $factor): self
    {
        if ($factor < 0) {
            throw new \InvalidArgumentException('Factor cannot be negative.');
        }
        return new self((int) round($this->amount * $factor), $this->currency);
    }

    public function percentage(int $percent): self
    {
        return $this->multiply($percent / 100);
    }

    public function equals(self $other): bool
    {
        return $this->amount === $other->amount && $this->currency === $other->currency;
    }

    public function isGreaterThan(self $other): bool
    {
        $this->guardSameCurrency($other);
        return $this->amount > $other->amount;
    }

    public function isZero(): bool { return $this->amount === 0; }

    public function formatted(): string
    {
        return number_format($this->amount / 100, 2) . ' ' . $this->currency;
    }

    public function amount(): int    { return $this->amount; }
    public function currency(): string { return $this->currency; }

    private function guardSameCurrency(self $other): void
    {
        if ($this->currency !== $other->currency) {
            throw new \InvalidArgumentException(
                "Currency mismatch: cannot operate on {$this->currency} and {$other->currency}."
            );
        }
    }
}

// ── Uuid ──────────────────────────────────────────────────────────────────────
final class Uuid
{
    private readonly string $value;

    private function __construct(string $value)
    {
        if (!preg_match(
            '/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/',
            $value
        )) {
            throw new \InvalidArgumentException("'{$value}' is not a valid UUID.");
        }
        $this->value = $value;
    }

    public static function generate(): self
    {
        // UUID v4 via random_bytes
        $bytes = random_bytes(16);
        $bytes[6] = chr((ord($bytes[6]) & 0x0f) | 0x40); // version 4
        $bytes[8] = chr((ord($bytes[8]) & 0x3f) | 0x80); // variant RFC 4122

        return new self(vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($bytes), 4)));
    }

    public static function fromString(string $value): self
    {
        return new self(strtolower($value));
    }

    public function toString(): string            { return $this->value; }
    public function equals(self $other): bool     { return $this->value === $other->value; }
    public function __toString(): string          { return $this->value; }
}

---

## 4. NAMING CONVENTIONS & CODE STRUCTURE

### 4.1 Naming Standards

```php
<?php
declare(strict_types=1);

// Classes — PascalCase noun phrases
class UserRepository {}
class OrderCalculator {}
class BcryptPasswordHasher {}

// Interfaces — PascalCase, often with Interface suffix
interface UserRepositoryInterface {}
interface Cacheable {}
interface EventDispatcherInterface {}

// Traits — PascalCase with "Trait" suffix
trait TimestampableTrait {}
trait SoftDeletableTrait {}

// Enums — PascalCase, cases PascalCase
enum UserStatus: string {
    case Active   = 'active';
    case Inactive = 'inactive';
    case Banned   = 'banned';
}

// Methods — camelCase, verb+noun
class UserService {
    public function findById(int $id): ?User {}
    public function createUser(CreateUserDto $dto): User {}
    public function updateEmail(int $userId, Email $email): void {}
    public function deleteUser(int $id): void {}
    public function isEmailTaken(Email $email): bool {}
    public function countActiveUsers(): int {}
}

// Properties and variables — camelCase
private int $totalAmount;
private \DateTimeImmutable $createdAt;
private UserStatus $status;

// Constants — UPPER_SNAKE_CASE
class HttpStatus {
    public const int OK                    = 200;
    public const int CREATED               = 201;
    public const int NO_CONTENT            = 204;
    public const int BAD_REQUEST           = 400;
    public const int UNAUTHORIZED          = 401;
    public const int FORBIDDEN             = 403;
    public const int NOT_FOUND             = 404;
    public const int CONFLICT              = 409;
    public const int UNPROCESSABLE_ENTITY  = 422;
    public const int TOO_MANY_REQUESTS     = 429;
    public const int INTERNAL_SERVER_ERROR = 500;
}
// One class per file, filename == class name: UserRepository.php, CreateUserDto.php
```

### 4.2 Method Design Rules

```php
<?php
declare(strict_types=1);

// RULE: Max 3 parameters. More -> use a DTO

// Bad
function createUser(string $name, string $email, string $password, string $role, bool $active): User {}

// Good
final class CreateUserDto {
    public function __construct(
        public readonly string $name,
        public readonly string $email,
        public readonly string $password,
        public readonly string $role   = 'user',
        public readonly bool   $active = true,
    ) {}
}
function createUser(CreateUserDto $dto): User {}

// RULE: Guard Clauses over deep nesting

// Bad
function processOrder(Order $order): void {
    if ($order !== null) {
        if ($order->isPaid()) {
            if ($order->hasItems()) {
                $this->ship($order);
            }
        }
    }
}

// Good — early returns
function processOrder(Order $order): void {
    if (!$order->isPaid())   throw new \DomainException('Unpaid order.');
    if (!$order->hasItems()) throw new \DomainException('Empty order.');
    $this->ship($order);
}

// RULE: Avoid boolean flag parameters
// Bad: getUsers(true);
// Good: getActiveUsers(); getAllUsers();

// RULE: No magic numbers
// Bad:  if ($user->role === 2) {}  sleep(86400);
// Good: if ($user->role() === UserRole::Admin) {}
final class Time { public const int SECONDS_IN_DAY = 86_400; }
sleep(Time::SECONDS_IN_DAY);

// RULE: Getters without "get" prefix (PHP style, not Java)
// Bad:  public function getId(): int    { return $this->id; }
// Good: public function id(): int       { return $this->id; }
```

---

## 5. OOP: CLASSES, INTERFACES, TRAITS, ENUMS

### 5.1 Anatomy of a Well-Structured Class

```php
<?php
declare(strict_types=1);
namespace App\Domain\User;

/**
 * Order inside a class:
 *   1. Constants  2. Properties  3. Constructor (private for entities)
 *   4. Static factory methods   5. Command methods (mutators)
 *   6. Query methods (accessors)  7. Private helpers
 */
final class User
{
    public const int MAX_NAME_LENGTH = 255;

    private function __construct(
        private readonly UserId             $id,
        private readonly Email              $email,
        private string                      $name,
        private UserStatus                  $status,
        private readonly \DateTimeImmutable $createdAt,
        private \DateTimeImmutable          $updatedAt,
    ) {
        $this->assertValidName($name);
    }

    // Factory methods
    public static function register(UserId $id, Email $email, string $name): self
    {
        $now = new \DateTimeImmutable();
        return new self($id, $email, $name, UserStatus::Active, $now, $now);
    }

    /** @param array<string, mixed> $data */
    public static function fromState(array $data): self
    {
        return new self(
            new UserId($data['id']),
            new Email($data['email']),
            $data['name'],
            UserStatus::from($data['status']),
            new \DateTimeImmutable($data['created_at']),
            new \DateTimeImmutable($data['updated_at']),
        );
    }

    // Command methods
    public function rename(string $newName): void
    {
        $this->assertValidName($newName);
        $this->name = $newName;
        $this->updatedAt = new \DateTimeImmutable();
    }

    public function deactivate(): void
    {
        if ($this->status === UserStatus::Inactive) {
            throw new \DomainException('User is already inactive.');
        }
        $this->status    = UserStatus::Inactive;
        $this->updatedAt = new \DateTimeImmutable();
    }

    public function ban(): void {
        $this->status    = UserStatus::Banned;
        $this->updatedAt = new \DateTimeImmutable();
    }

    // Accessors
    public function id(): UserId                    { return $this->id; }
    public function email(): Email                  { return $this->email; }
    public function name(): string                  { return $this->name; }
    public function status(): UserStatus            { return $this->status; }
    public function createdAt(): \DateTimeImmutable { return $this->createdAt; }
    public function updatedAt(): \DateTimeImmutable { return $this->updatedAt; }
    public function isActive(): bool                { return $this->status === UserStatus::Active; }
    public function isBanned(): bool                { return $this->status === UserStatus::Banned; }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'id'         => $this->id->value(),
            'email'      => $this->email->toString(),
            'name'       => $this->name,
            'status'     => $this->status->value,
            'created_at' => $this->createdAt->format('Y-m-d H:i:s'),
            'updated_at' => $this->updatedAt->format('Y-m-d H:i:s'),
        ];
    }

    private function assertValidName(string $name): void
    {
        if (trim($name) === '') throw new \InvalidArgumentException('Name cannot be empty.');
        if (mb_strlen($name) > self::MAX_NAME_LENGTH) {
            throw new \InvalidArgumentException('Name exceeds ' . self::MAX_NAME_LENGTH . ' chars.');
        }
    }
}
```

### 5.2 Enums — PHP 8.1+

```php
<?php
declare(strict_types=1);

enum OrderStatus: string
{
    case Pending    = 'pending';
    case Processing = 'processing';
    case Shipped    = 'shipped';
    case Delivered  = 'delivered';
    case Cancelled  = 'cancelled';

    public function isFinal(): bool
    {
        return $this === self::Delivered || $this === self::Cancelled;
    }

    public function label(): string
    {
        return match($this) {
            self::Pending    => 'Pending',
            self::Processing => 'Processing',
            self::Shipped    => 'Shipped',
            self::Delivered  => 'Delivered',
            self::Cancelled  => 'Cancelled',
        };
    }

    public function canTransitionTo(self $next): bool
    {
        return match($this) {
            self::Pending    => in_array($next, [self::Processing, self::Cancelled]),
            self::Processing => in_array($next, [self::Shipped, self::Cancelled]),
            self::Shipped    => $next === self::Delivered,
            default          => false,
        };
    }
}

// Usage
$status = OrderStatus::from('pending');    // throws if invalid
$status = OrderStatus::tryFrom('bad');     // returns null — safe

// Enum implementing interface
interface HasColor { public function color(): string; }

enum Priority: int implements HasColor
{
    case Low    = 1;
    case Medium = 5;
    case High   = 10;

    public function color(): string
    {
        return match($this) {
            self::Low    => '#00FF00',
            self::Medium => '#FFA500',
            self::High   => '#FF0000',
        };
    }
}
```

### 5.3 Interfaces — System Contracts

```php
<?php
declare(strict_types=1);
namespace App\Domain\User;

interface UserRepositoryInterface
{
    public function findById(UserId $id): ?User;
    public function findByEmail(Email $email): ?User;
    /** @return list<User> */
    public function findAll(int $limit = 100, int $offset = 0): array;
    /** @return list<User> */
    public function findByStatus(UserStatus $status): array;
    public function save(User $user): void;
    public function delete(UserId $id): void;
    public function exists(UserId $id): bool;
    public function countByStatus(UserStatus $status): int;
}

// Segregated for read-only use cases
interface UserReaderInterface
{
    public function findById(UserId $id): ?User;
    public function findByEmail(Email $email): ?User;
    /** @return list<User> */
    public function findAll(int $limit = 100, int $offset = 0): array;
}

interface UserWriterInterface
{
    public function save(User $user): void;
    public function delete(UserId $id): void;
}
```

### 5.4 Traits — Use Sparingly

```php
<?php
declare(strict_types=1);
namespace App\Domain\Concern;

// ONLY for reusable cross-cutting technical behaviour — NOT for business logic

trait TimestampableTrait
{
    private \DateTimeImmutable $createdAt;
    private \DateTimeImmutable $updatedAt;

    public function initTimestamps(): void
    {
        $this->createdAt = $this->updatedAt = new \DateTimeImmutable();
    }

    public function touch(): void { $this->updatedAt = new \DateTimeImmutable(); }

    public function createdAt(): \DateTimeImmutable { return $this->createdAt; }
    public function updatedAt(): \DateTimeImmutable { return $this->updatedAt; }
}

trait SoftDeletableTrait
{
    private ?\DateTimeImmutable $deletedAt = null;

    public function softDelete(): void    { $this->deletedAt = new \DateTimeImmutable(); }
    public function restore(): void       { $this->deletedAt = null; }
    public function isDeleted(): bool     { return $this->deletedAt !== null; }
    public function deletedAt(): ?\DateTimeImmutable { return $this->deletedAt; }
}

final class Article
{
    use TimestampableTrait;
    use SoftDeletableTrait;

    public function __construct(private string $title)
    {
        $this->initTimestamps();
    }
}
```

---

## 6. SOLID PRINCIPLES — DEEP DIVE

### 6.1 Single Responsibility (SRP)

> *A class has one and only one reason to change.*

```php
<?php
declare(strict_types=1);

// Bad — one class, multiple responsibilities
class UserManager {
    public function create(array $data): User {}
    public function sendWelcomeEmail(User $user): void {}
    public function exportToCsv(): string {}
    public function generateReport(): array {}
    public function checkPermission(User $user): bool {}
}

// Good — each class has exactly one responsibility
final class UserService          { public function createUser(CreateUserDto $dto): User {} }
final class UserNotifier         { public function sendWelcomeEmail(User $user): void {} }
final class UserCsvExporter      { public function export(array $users): string {} }
final class UserReporter         { public function generate(UserFilter $f): array {} }
final class UserPermissionChecker{ public function can(User $user, string $p): bool {} }
```

### 6.2 Open/Closed (OCP)

> *Open for extension, closed for modification.*

```php
<?php
declare(strict_types=1);

// Bad — adding a channel requires modifying this class
class NotificationSender {
    public function send(User $user, string $type, string $msg): void {
        if ($type === 'email') { /* ... */ }
        elseif ($type === 'sms') { /* ... */ }
        // Adding 'slack' requires editing this class — violation
    }
}

// Good — adding a channel = adding a new class, zero existing code changes
interface NotificationChannelInterface {
    public function send(User $user, string $message): void;
    public function supports(string $channel): bool;
}

final class EmailChannel implements NotificationChannelInterface {
    public function __construct(private readonly MailerInterface $mailer) {}
    public function send(User $user, string $message): void {
        $this->mailer->send($user->email()->toString(), $message);
    }
    public function supports(string $channel): bool { return $channel === 'email'; }
}

final class SmsChannel implements NotificationChannelInterface {
    public function __construct(private readonly SmsGateway $gateway) {}
    public function send(User $user, string $message): void {
        $this->gateway->send($user->phone(), $message);
    }
    public function supports(string $channel): bool { return $channel === 'sms'; }
}

// Adding Slack = one new class, no modifications anywhere:
final class SlackChannel implements NotificationChannelInterface { /* ... */ }

final class NotificationService {
    /** @param list<NotificationChannelInterface> $channels */
    public function __construct(private readonly array $channels) {}

    public function notify(User $user, string $channel, string $message): void {
        foreach ($this->channels as $ch) {
            if ($ch->supports($channel)) { $ch->send($user, $message); return; }
        }
        throw new \DomainException("Unsupported channel: {$channel}");
    }
}
```

### 6.3 Liskov Substitution (LSP)

> *Subtypes must be substitutable for their base types without altering program correctness.*

```php
<?php
declare(strict_types=1);

// Classic violation: Square extends Rectangle, breaks setWidth contract
// Fix: use a common interface instead of inheritance

interface Shape {
    public function area(): float;
    public function perimeter(): float;
}

final class Rectangle implements Shape {
    public function __construct(private readonly float $w, private readonly float $h) {}
    public function area(): float      { return $this->w * $this->h; }
    public function perimeter(): float { return 2 * ($this->w + $this->h); }
}

final class Square implements Shape {
    public function __construct(private readonly float $side) {}
    public function area(): float      { return $this->side ** 2; }
    public function perimeter(): float { return 4 * $this->side; }
}

// Both are fully substitutable as Shape — no contract broken
function printShapeInfo(Shape $shape): void {
    echo "Area: {$shape->area()}, Perimeter: {$shape->perimeter()}\n";
}
```

### 6.4 Interface Segregation (ISP)

> *No client should depend on methods it does not use.*

```php
<?php
declare(strict_types=1);

// Bad — fat interface forces unrelated methods
interface UserInterface {
    public function findById(int $id): ?User;
    public function save(User $user): void;
    public function sendEmail(User $user): void;  // unrelated to persistence!
    public function exportCsv(): string;           // unrelated to persistence!
}

// Good — segregated
interface UserReaderInterface {
    public function findById(int $id): ?User;
    public function findByEmail(Email $email): ?User;
    /** @return list<User> */
    public function findAll(int $limit = 100, int $offset = 0): array;
}
interface UserWriterInterface {
    public function save(User $user): void;
    public function delete(int $id): void;
}
// Combine when full access is needed
interface UserRepositoryInterface extends UserReaderInterface, UserWriterInterface {}

// A read-only cache only implements what it needs:
final class CachedUserReader implements UserReaderInterface { /* ... */ }
```

### 6.5 Dependency Inversion (DIP)

> *Depend on abstractions, not concretions.*

```php
<?php
declare(strict_types=1);

// Bad — high-level module creates its own low-level dependencies
class OrderService {
    private MysqlOrderRepository $repo;
    private SmtpMailer $mailer;
    public function __construct() {
        $this->repo   = new MysqlOrderRepository(); // hard dependency
        $this->mailer = new SmtpMailer();           // hard dependency — untestable
    }
}

// Good — inject abstractions, concrete wiring happens only in container
final class OrderService {
    public function __construct(
        private readonly OrderRepositoryInterface $repository,
        private readonly MailerInterface          $mailer,
        private readonly LoggerInterface          $logger,
        private readonly EventDispatcherInterface $dispatcher,
    ) {}

    public function placeOrder(PlaceOrderDto $dto): Order {
        $order = Order::create($dto);
        $this->repository->save($order);
        $this->dispatcher->dispatch(new OrderPlacedEvent($order->id()));
        $this->logger->info('Order placed', ['id' => $order->id()->value()]);
        return $order;
    }
}
```

---

## 7. DESIGN PATTERNS

### 7.1 Repository Pattern

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Repository;

final class PdoUserRepository extends AbstractRepository implements UserRepositoryInterface
{
    public function findById(UserId $id): ?User
    {
        $row = $this->fetchOne(
            'SELECT * FROM users WHERE id=:id AND deleted_at IS NULL',
            ['id' => $id->value()]
        );
        return $row !== null ? User::fromState($row) : null;
    }

    public function findByEmail(Email $email): ?User
    {
        $row = $this->fetchOne(
            'SELECT * FROM users WHERE email=:email AND deleted_at IS NULL',
            ['email' => $email->toString()]
        );
        return $row !== null ? User::fromState($row) : null;
    }

    public function findAll(int $limit = 100, int $offset = 0): array
    {
        return array_map(User::fromState(...), $this->fetchAll(
            'SELECT * FROM users WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT :l OFFSET :o',
            ['l' => $limit, 'o' => $offset]
        ));
    }

    public function findByStatus(UserStatus $status): array
    {
        return array_map(User::fromState(...), $this->fetchAll(
            'SELECT * FROM users WHERE status=:s AND deleted_at IS NULL',
            ['s' => $status->value]
        ));
    }

    public function save(User $user): void
    {
        $d = $user->toArray();
        $this->execute(
            'INSERT INTO users (id,email,name,status,created_at,updated_at)
             VALUES (:id,:email,:name,:status,:created_at,:updated_at)
             ON DUPLICATE KEY UPDATE name=VALUES(name),status=VALUES(status),updated_at=VALUES(updated_at)',
            $d
        );
    }

    public function delete(UserId $id): void
    {
        $this->execute('UPDATE users SET deleted_at=NOW() WHERE id=:id', ['id' => $id->value()]);
    }

    public function exists(UserId $id): bool
    {
        return $this->fetchOne('SELECT 1 FROM users WHERE id=:id AND deleted_at IS NULL',
                               ['id' => $id->value()]) !== null;
    }

    public function countByStatus(UserStatus $status): int
    {
        $row = $this->fetchOne(
            'SELECT COUNT(*) AS cnt FROM users WHERE status=:s AND deleted_at IS NULL',
            ['s' => $status->value]
        );
        return (int)($row['cnt'] ?? 0);
    }
}
```

### 7.2 Observer / Event Pattern

```php
<?php
declare(strict_types=1);
namespace App\Domain\Event;

interface DomainEventInterface {
    public function occurredAt(): \DateTimeImmutable;
    public function eventId(): string;
}

final class UserRegisteredEvent implements DomainEventInterface
{
    public readonly \DateTimeImmutable $occurredAt;
    public readonly string $eventId;

    public function __construct(
        public readonly int $userId,
        public readonly string $email,
        public readonly string $name,
    ) {
        $this->occurredAt = new \DateTimeImmutable();
        $this->eventId    = bin2hex(random_bytes(16));
    }

    public function occurredAt(): \DateTimeImmutable { return $this->occurredAt; }
    public function eventId(): string                { return $this->eventId; }
}

interface EventListenerInterface {
    public function handle(DomainEventInterface $event): void;
    /** @return list<class-string<DomainEventInterface>> */
    public function subscribesTo(): array;
}

final class SendWelcomeEmailListener implements EventListenerInterface {
    public function __construct(private readonly MailerInterface $mailer) {}
    public function handle(DomainEventInterface $event): void {
        assert($event instanceof UserRegisteredEvent);
        $this->mailer->sendWelcome($event->email, $event->name);
    }
    public function subscribesTo(): array { return [UserRegisteredEvent::class]; }
}

final class EventDispatcher {
    /** @var array<class-string, list<EventListenerInterface>> */
    private array $listeners = [];

    public function subscribe(EventListenerInterface $l): void {
        foreach ($l->subscribesTo() as $class) $this->listeners[$class][] = $l;
    }

    public function dispatch(DomainEventInterface $event): void {
        foreach ($this->listeners[$event::class] ?? [] as $l) $l->handle($event);
    }
}
```

### 7.3 Decorator Pattern

```php
<?php
declare(strict_types=1);

final class CachedUserRepository implements UserRepositoryInterface
{
    public function __construct(
        private readonly UserRepositoryInterface $inner,
        private readonly CacheInterface          $cache,
        private readonly int                     $ttl = 300,
    ) {}

    public function findById(UserId $id): ?User {
        $key = "users:id:{$id->value()}";
        $hit = $this->cache->get($key);
        if ($hit !== null) return $hit;
        $user = $this->inner->findById($id);
        if ($user !== null) $this->cache->set($key, $user, $this->ttl);
        return $user;
    }

    public function findByEmail(Email $email): ?User {
        return $this->cache->remember(
            "users:email:{$email->toString()}", $this->ttl,
            fn() => $this->inner->findByEmail($email)
        );
    }

    public function save(User $user): void {
        $this->inner->save($user);
        $this->cache->delete("users:id:{$user->id()->value()}");
        $this->cache->delete("users:email:{$user->email()->toString()}");
    }

    public function delete(UserId $id): void { $this->inner->delete($id); $this->cache->delete("users:id:{$id->value()}"); }
    public function findAll(int $l=100, int $o=0): array { return $this->inner->findAll($l,$o); }
    public function findByStatus(UserStatus $s): array   { return $this->inner->findByStatus($s); }
    public function exists(UserId $id): bool             { return $this->inner->exists($id); }
    public function countByStatus(UserStatus $s): int    { return $this->inner->countByStatus($s); }
}
```

### 7.4 Strategy Pattern

```php
<?php
declare(strict_types=1);

interface DiscountStrategyInterface {
    public function calculate(Money $price, User $user): Money;
}

final class PercentageDiscount implements DiscountStrategyInterface {
    public function __construct(private readonly int $percent) {}
    public function calculate(Money $price, User $user): Money { return $price->percentage($this->percent); }
}

final class VipDiscount implements DiscountStrategyInterface {
    public function calculate(Money $price, User $user): Money {
        return $user->isVip() ? $price->percentage(20) : Money::zero($price->currency());
    }
}

final class PricingService {
    /** @param list<DiscountStrategyInterface> $strategies */
    public function __construct(private readonly array $strategies) {}

    public function finalPrice(Money $price, User $user): Money {
        $total = Money::zero($price->currency());
        foreach ($this->strategies as $s) $total = $total->add($s->calculate($price, $user));
        return $total->isGreaterThan($price) ? Money::zero($price->currency())
                                              : $price->subtract($total);
    }
}
```

### 7.5 Command Bus Pattern

```php
<?php
declare(strict_types=1);

interface CommandInterface {}
interface CommandHandlerInterface { public function handle(CommandInterface $command): mixed; }

final class CreateUserCommand implements CommandInterface {
    public function __construct(
        public readonly string $email,
        public readonly string $name,
        public readonly string $password,
    ) {}
}

final class CreateUserHandler implements CommandHandlerInterface {
    public function __construct(
        private readonly UserRepositoryInterface $users,
        private readonly PasswordHasherInterface $hasher,
        private readonly EventDispatcher         $dispatcher,
    ) {}

    public function handle(CommandInterface $command): User {
        assert($command instanceof CreateUserCommand);
        if ($this->users->findByEmail(new Email($command->email)) !== null) {
            throw new ConflictException("Email '{$command->email}' is already taken.");
        }
        $user = User::register(new UserId($this->nextId()), new Email($command->email), $command->name);
        $this->users->save($user);
        $this->dispatcher->dispatch(new UserRegisteredEvent($user->id()->value(), $user->email()->toString(), $user->name()));
        return $user;
    }
    private function nextId(): int { return (int)(microtime(true) * 1000); }
}

final class CommandBus {
    /** @var array<class-string, CommandHandlerInterface> */
    private array $handlers = [];

    public function register(string $cmd, CommandHandlerInterface $handler): void {
        $this->handlers[$cmd] = $handler;
    }
    public function dispatch(CommandInterface $cmd): mixed {
        $class = $cmd::class;
        if (!isset($this->handlers[$class])) throw new \RuntimeException("No handler for: {$class}");
        return $this->handlers[$class]->handle($cmd);
    }
}
```

### 7.6 Query Builder (Immutable)

```php
<?php
declare(strict_types=1);

final class QueryBuilder
{
    private string $table   = '';
    private array  $selects = ['*'];
    private array  $wheres  = [];
    private array  $params  = [];
    private array  $orderBy = [];
    private ?int   $limit   = null;
    private ?int   $offset  = null;

    public function from(string $t): static { $c=clone $this; $c->table=$t; return $c; }
    public function select(string ...$cols): static { $c=clone $this; $c->selects=$cols; return $c; }

    public function where(string $col, mixed $val, string $op='='): static {
        $c=clone $this; $k='p'.count($c->params);
        $c->wheres[]="{$col} {$op} :{$k}"; $c->params[$k]=$val; return $c;
    }

    public function whereIn(string $col, array $vals): static {
        if (empty($vals)) return $this->where('1','0');
        $c=clone $this; $keys=[]; $base=count($c->params);
        foreach ($vals as $i=>$v) { $k="in_{$base}_{$i}"; $c->params[$k]=$v; $keys[]=":{$k}"; }
        $c->wheres[]="{$col} IN (".implode(',',$keys).")"; return $c;
    }

    public function whereNull(string $col): static { $c=clone $this; $c->wheres[]="{$col} IS NULL"; return $c; }
    public function whereNotNull(string $col): static { $c=clone $this; $c->wheres[]="{$col} IS NOT NULL"; return $c; }

    public function orderBy(string $col, string $dir='ASC'): static {
        $c=clone $this; $c->orderBy[]="{$col} ".(strtoupper($dir)==='DESC'?'DESC':'ASC'); return $c;
    }

    public function limit(int $n): static  { $c=clone $this; $c->limit=$n;  return $c; }
    public function offset(int $n): static { $c=clone $this; $c->offset=$n; return $c; }
    public function forPage(int $page, int $per): static { return $this->limit($per)->offset(($page-1)*$per); }

    public function toSql(): string {
        $sql='SELECT '.implode(', ',$this->selects).' FROM '.$this->table;
        if ($this->wheres)  $sql.=' WHERE '.implode(' AND ',$this->wheres);
        if ($this->orderBy) $sql.=' ORDER BY '.implode(', ',$this->orderBy);
        if ($this->limit!==null)  $sql.=' LIMIT '.$this->limit;
        if ($this->offset!==null) $sql.=' OFFSET '.$this->offset;
        return $sql;
    }

    public function params(): array { return $this->params; }

    public function get(\PDO $pdo): array {
        $s=$pdo->prepare($this->toSql()); $s->execute($this->params()); return $s->fetchAll();
    }
    public function first(\PDO $pdo): ?array { $r=$this->limit(1)->get($pdo); return $r[0]??null; }
    public function count(\PDO $pdo): int {
        $r=$this->select('COUNT(*) AS _c')->first($pdo); return (int)($r['_c']??0);
    }
}

// Usage:
$users = (new QueryBuilder())
    ->from('users')
    ->select('id','email','name')
    ->where('status', 'active')
    ->whereIn('role', ['admin','moderator'])
    ->whereNotNull('email_verified_at')
    ->orderBy('created_at', 'DESC')
    ->forPage(1, 20)
    ->get($pdo);
```

---

## 8. DOMAIN-DRIVEN DESIGN (DDD) IN PHP

### 8.1 Layered Architecture

```
┌───────────────────────────────────────────────┐
│           Infrastructure Layer                 │  PDO, Redis, HTTP, Mailer, Queue
├───────────────────────────────────────────────┤
│            Application Layer                   │  Use Cases, Commands, Queries, DTOs
├───────────────────────────────────────────────┤
│              Domain Layer                      │  Entities, Value Objects, Aggregates,
│                                               │  Domain Events, Repository Interfaces
└───────────────────────────────────────────────┘
Rule: each layer depends ONLY on layers below it.
Domain Layer has ZERO external dependencies.
```

### 8.2 Aggregate Root

```php
<?php
declare(strict_types=1);
namespace App\Domain\Order;

final class Order
{
    /** @var list<OrderItem> */
    private array $items  = [];
    /** @var list<DomainEventInterface> */
    private array $events = [];

    private function __construct(
        private readonly OrderId            $id,
        private readonly UserId             $userId,
        private OrderStatus                 $status,
        private Money                       $total,
        private readonly \DateTimeImmutable $createdAt,
    ) {}

    public static function place(OrderId $id, UserId $userId, array $items): self
    {
        if (empty($items)) throw new \DomainException('Order must have at least one item.');
        $order = new self($id, $userId, OrderStatus::Pending, Money::zero('USD'), new \DateTimeImmutable());
        foreach ($items as $item) $order->addItem($item);
        $order->record(new OrderPlacedEvent($order->id, $order->userId, $order->total));
        return $order;
    }

    public function addItem(OrderItem $item): void {
        if ($this->status !== OrderStatus::Pending) throw new \DomainException('Non-pending order.');
        $this->items[] = $item;
        $this->total   = $this->total->add($item->subtotal());
    }

    public function confirm(): void {
        $this->guard(OrderStatus::Pending, 'confirm');
        $this->status = OrderStatus::Processing;
        $this->record(new OrderConfirmedEvent($this->id));
    }

    public function ship(string $trackingCode): void {
        $this->guard(OrderStatus::Processing, 'ship');
        $this->status = OrderStatus::Shipped;
        $this->record(new OrderShippedEvent($this->id, $trackingCode));
    }

    public function cancel(string $reason): void {
        if ($this->status->isFinal()) throw new \DomainException("Cannot cancel in status: {$this->status->value}");
        $this->status = OrderStatus::Cancelled;
        $this->record(new OrderCancelledEvent($this->id, $reason));
    }

    public function id(): OrderId         { return $this->id; }
    public function status(): OrderStatus { return $this->status; }
    public function total(): Money        { return $this->total; }

    /** @return list<DomainEventInterface> */
    public function pullEvents(): array { $e=$this->events; $this->events=[]; return $e; }

    private function record(DomainEventInterface $e): void { $this->events[] = $e; }
    private function guard(OrderStatus $expected, string $action): void {
        if ($this->status !== $expected) {
            throw new \DomainException("Cannot {$action} order with status {$this->status->value}. Expected: {$expected->value}.");
        }
    }
}
```

### 8.3 Domain Service

```php
<?php
declare(strict_types=1);

// Domain Service — stateless logic that doesn't belong to a single entity
final class PricingService
{
    /** @param list<DiscountStrategyInterface> $strategies */
    public function __construct(private readonly array $strategies) {}

    public function calculatePrice(Product $product, User $user, int $qty): Money
    {
        $base  = $product->price()->multiply($qty);
        $total = Money::zero($base->currency());
        foreach ($this->strategies as $s) $total = $total->add($s->calculate($base, $user));
        return $total->isGreaterThan($base) ? Money::zero($base->currency()) : $base->subtract($total);
    }
}

// Domain Policy — encapsulates a business rule
final class OrderCancellationPolicy
{
    private const int WINDOW_HOURS = 24;

    public function canCancel(Order $order): bool
    {
        if ($order->status()->isFinal()) return false;
        return (new \DateTimeImmutable())->diff($order->createdAt())->h <= self::WINDOW_HOURS;
    }

    public function assertCanCancel(Order $order): void
    {
        if (!$this->canCancel($order)) {
            throw new \DomainException('Cancellation window of '.self::WINDOW_HOURS.'h has passed.');
        }
    }
}
```

---

## 9. ERROR HANDLING & EXCEPTIONS

### 9.1 Exception Hierarchy

```php
<?php
declare(strict_types=1);
namespace App\Domain\Exception;

class AppException          extends \RuntimeException {}
class DomainException       extends AppException {}
class InvariantException    extends DomainException {}
class ApplicationException  extends AppException {}

class NotFoundException extends ApplicationException {
    public function __construct(string $res='Resource', int|string $id='', ?\Throwable $p=null) {
        parent::__construct($id!==''?"{$res} '{$id}' not found.":"{$res} not found.", 404, $p);
    }
}

class ConflictException extends ApplicationException {
    public function __construct(string $msg='Conflict.', ?\Throwable $p=null) { parent::__construct($msg, 409, $p); }
}

class ValidationException extends ApplicationException {
    /** @param array<string, list<string>> $errors */
    public function __construct(private readonly array $errors, ?\Throwable $p=null) {
        parent::__construct('Validation failed.', 422, $p);
    }
    /** @return array<string, list<string>> */
    public function errors(): array { return $this->errors; }
}

class UnauthorizedException  extends ApplicationException {
    public function __construct(string $m='Unauthorized.', ?\Throwable $p=null) { parent::__construct($m,401,$p); }
}
class ForbiddenException     extends ApplicationException {
    public function __construct(string $m='Forbidden.', ?\Throwable $p=null) { parent::__construct($m,403,$p); }
}
class TooManyRequestsException extends ApplicationException {
    public function __construct(private readonly int $retryAfter=60, ?\Throwable $p=null) {
        parent::__construct('Too many requests.', 429, $p);
    }
    public function retryAfter(): int { return $this->retryAfter; }
}

class InfrastructureException extends AppException {}
class DatabaseException       extends InfrastructureException {}
class CacheException          extends InfrastructureException {}
```

### 9.2 Global Exception Handler

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http;

final class ExceptionHandler
{
    public function __construct(
        private readonly LoggerInterface $logger,
        private readonly bool $debug = false,
    ) {}

    public function handle(\Throwable $e): Response
    {
        $this->log($e);
        return match(true) {
            $e instanceof ValidationException      => Response::json(['error'=>'Validation Failed','errors'=>$e->errors()], 422),
            $e instanceof NotFoundException        => Response::json(['error'=>$e->getMessage()], 404),
            $e instanceof ConflictException        => Response::json(['error'=>$e->getMessage()], 409),
            $e instanceof UnauthorizedException    => Response::json(['error'=>$e->getMessage()], 401),
            $e instanceof ForbiddenException       => Response::json(['error'=>$e->getMessage()], 403),
            $e instanceof TooManyRequestsException => Response::json(['error'=>'Too Many Requests'],429)
                                                        ->withHeader('Retry-After',(string)$e->retryAfter()),
            $e instanceof AppException             => Response::json(['error'=>$e->getMessage()], $e->getCode()?:500),
            default                                => $this->serverError($e),
        };
    }

    private function serverError(\Throwable $e): Response {
        $b = ['error' => 'Internal Server Error'];
        if ($this->debug) $b['debug'] = ['message'=>$e->getMessage(),'class'=>$e::class,'line'=>$e->getLine()];
        return Response::json($b, 500);
    }

    private function log(\Throwable $e): void {
        $ctx = ['class'=>$e::class,'file'=>$e->getFile(),'line'=>$e->getLine()];
        if ($e instanceof AppException && $e->getCode() < 500) $this->logger->warning($e->getMessage(), $ctx);
        else $this->logger->error($e->getMessage(), $ctx+['trace'=>$e->getTraceAsString()]);
    }
}
```

### 9.3 Result Type

```php
<?php
declare(strict_types=1);

/**
 * @template TValue
 */
final class Result
{
    private function __construct(
        private readonly mixed $value,
        private readonly ?\Throwable $error,
    ) {}

    public static function ok(mixed $value = null): self { return new self($value, null); }
    public static function fail(\Throwable $error): self { return new self(null, $error); }

    public function isOk(): bool   { return $this->error === null; }
    public function isFail(): bool { return $this->error !== null; }

    public function value(): mixed {
        if ($this->error !== null) throw new \LogicException('Result is failed.', 0, $this->error);
        return $this->value;
    }
    public function error(): \Throwable {
        if ($this->error === null) throw new \LogicException('Result is successful.');
        return $this->error;
    }
    public function valueOr(mixed $default): mixed { return $this->isOk() ? $this->value : $default; }

    public function map(callable $fn): self {
        if ($this->isFail()) return self::fail($this->error);
        try { return self::ok($fn($this->value)); }
        catch (\Throwable $e) { return self::fail($e); }
    }
}

// Usage
$result = $paymentService->charge($dto);
if ($result->isFail()) return Response::json(['error' => $result->error()->getMessage()], 422);
$transaction = $result->value();
```



---

## 10. DATABASE LAYER (PDO)

### 10.1 Connection Factory

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Database;

final class DatabaseConfig
{
    public function __construct(
        public readonly string $driver   = 'mysql',
        public readonly string $host     = '127.0.0.1',
        public readonly int    $port     = 3306,
        public readonly string $database = '',
        public readonly string $username = '',
        public readonly string $password = '',
        public readonly string $charset  = 'utf8mb4',
    ) {}
}

final class PdoFactory
{
    public static function create(DatabaseConfig $config): \PDO
    {
        $dsn = sprintf('%s:host=%s;port=%d;dbname=%s;charset=%s',
            $config->driver, $config->host, $config->port,
            $config->database, $config->charset
        );

        return new \PDO($dsn, $config->username, $config->password, [
            \PDO::ATTR_ERRMODE            => \PDO::ERRMODE_EXCEPTION,
            \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC,
            \PDO::ATTR_EMULATE_PREPARES   => false,  // native prepared statements
            \PDO::ATTR_PERSISTENT         => false,  // no persistent connections
            \PDO::ATTR_TIMEOUT            => 5,
            \PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'",
        ]);
    }
}
```

### 10.2 Abstract Repository Base

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Repository;

abstract class AbstractRepository
{
    public function __construct(protected readonly \PDO $pdo) {}

    protected function fetchOne(string $sql, array $params = []): ?array
    {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $row = $stmt->fetch();
        return $row !== false ? $row : null;
    }

    /** @return array<int, array<string, mixed>> */
    protected function fetchAll(string $sql, array $params = []): array
    {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll();
    }

    protected function fetchColumn(string $sql, array $params = []): mixed
    {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchColumn();
    }

    protected function execute(string $sql, array $params = []): int
    {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->rowCount();
    }

    protected function lastInsertId(): int { return (int)$this->pdo->lastInsertId(); }
}
```

### 10.3 Transaction Manager

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Database;

final class TransactionManager
{
    public function __construct(private readonly \PDO $pdo) {}

    /**
     * Run a callback in a transaction. Auto-commits or rolls back.
     * @template T
     * @param callable(): T $callback
     * @return T
     */
    public function run(callable $callback): mixed
    {
        $this->pdo->beginTransaction();
        try {
            $result = $callback();
            $this->pdo->commit();
            return $result;
        } catch (\Throwable $e) {
            if ($this->pdo->inTransaction()) $this->pdo->rollBack();
            throw $e;
        }
    }

    /** Nested transactions via savepoints */
    public function runNested(callable $callback): mixed
    {
        if (!$this->pdo->inTransaction()) return $this->run($callback);

        $sp = 'sp_' . uniqid();
        $this->pdo->exec("SAVEPOINT {$sp}");
        try {
            $result = $callback();
            $this->pdo->exec("RELEASE SAVEPOINT {$sp}");
            return $result;
        } catch (\Throwable $e) {
            $this->pdo->exec("ROLLBACK TO SAVEPOINT {$sp}");
            throw $e;
        }
    }
}

// Usage
$transactionManager->run(function () use ($from, $to, $amount): void {
    $from->debit($amount);
    $to->credit($amount);
    $this->accounts->save($from);
    $this->accounts->save($to);
});
```

### 10.4 Safe SQL Patterns

```php
<?php
declare(strict_types=1);

// ALWAYS: prepared statements with named parameters
$stmt = $pdo->prepare('SELECT * FROM users WHERE email=:email AND status=:status');
$stmt->execute(['email' => $email, 'status' => 'active']);

// Integer binding with explicit PARAM_INT
$stmt = $pdo->prepare('SELECT * FROM orders WHERE user_id=:id');
$stmt->bindValue(':id', $userId, \PDO::PARAM_INT);
$stmt->execute();

// Dynamic column names — whitelist ONLY
function safeOrderBy(string $col, string $dir): string
{
    $cols = ['id','name','email','created_at'];
    $dirs = ['ASC','DESC'];
    if (!in_array($col, $cols, true))   throw new \InvalidArgumentException("Bad column: {$col}");
    if (!in_array(strtoupper($dir), $dirs, true)) throw new \InvalidArgumentException("Bad direction: {$dir}");
    return "{$col} " . strtoupper($dir);
}

// Batch insert
function batchInsert(\PDO $pdo, string $table, array $rows): void
{
    if (empty($rows)) return;
    $cols  = array_keys($rows[0]);
    $place = '(' . implode(',', array_map(fn($c)=>":{$c}_ROW", $cols)) . ')';
    $all   = [];
    $params = [];
    foreach ($rows as $i => $row) {
        $rowPlace = '(' . implode(',', array_map(fn($c)=>":{$c}_{$i}", $cols)) . ')';
        $all[]    = $rowPlace;
        foreach ($cols as $c) $params["{$c}_{$i}"] = $row[$c];
    }
    $pdo->prepare("INSERT INTO {$table} (".implode(',',$cols).") VALUES ".implode(',',$all))
        ->execute($params);
}

// Pagination
function paginate(\PDO $pdo, int $page, int $perPage): array
{
    $offset = ($page - 1) * $perPage;
    $total  = (int)$pdo->query('SELECT COUNT(*) FROM users')->fetchColumn();
    $stmt   = $pdo->prepare('SELECT * FROM users ORDER BY created_at DESC LIMIT :l OFFSET :o');
    $stmt->bindValue(':l', $perPage, \PDO::PARAM_INT);
    $stmt->bindValue(':o', $offset,  \PDO::PARAM_INT);
    $stmt->execute();
    return [
        'data'         => $stmt->fetchAll(),
        'total'        => $total,
        'per_page'     => $perPage,
        'current_page' => $page,
        'last_page'    => (int)ceil($total / $perPage),
    ];
}

// NEVER do these:
// $sql = "SELECT * FROM users WHERE id = {$_GET['id']}";   // SQL injection
// $sql = "SELECT * FROM users WHERE name = '{$name}'";     // SQL injection
// $sql = "SELECT * FROM users ORDER BY " . $_GET['sort']; // SQL injection
```

### 10.5 Migrations

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Database\Migration;

interface MigrationInterface {
    public function up(\PDO $pdo): void;
    public function down(\PDO $pdo): void;
    public function name(): string;
}

final class CreateUsersTable implements MigrationInterface
{
    public function name(): string { return '001_create_users_table'; }

    public function up(\PDO $pdo): void
    {
        $pdo->exec("
            CREATE TABLE IF NOT EXISTS users (
                id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                email             VARCHAR(320)  NOT NULL,
                name              VARCHAR(255)  NOT NULL,
                password_hash     VARCHAR(255)  NOT NULL,
                status            ENUM('active','inactive','banned') NOT NULL DEFAULT 'active',
                role              ENUM('user','admin','moderator')   NOT NULL DEFAULT 'user',
                email_verified_at DATETIME NULL,
                created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                deleted_at        DATETIME NULL,
                UNIQUE KEY uq_email (email),
                INDEX idx_status (status),
                INDEX idx_deleted_at (deleted_at),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        ");
    }

    public function down(\PDO $pdo): void { $pdo->exec('DROP TABLE IF EXISTS users'); }
}

final class MigrationRunner
{
    public function __construct(private readonly \PDO $pdo) {}

    public function migrate(): void
    {
        $this->ensureMigrationsTable();
        $applied    = $this->applied();
        $migrations = $this->all();

        foreach ($migrations as $m) {
            if (in_array($m->name(), $applied, true)) continue;
            echo "Migrating: {$m->name()} ... ";
            $this->pdo->beginTransaction();
            try {
                $m->up($this->pdo);
                $this->record($m->name());
                $this->pdo->commit();
                echo "done.\n";
            } catch (\Throwable $e) {
                $this->pdo->rollBack();
                echo "FAILED: {$e->getMessage()}\n";
                throw $e;
            }
        }
    }

    private function ensureMigrationsTable(): void
    {
        $this->pdo->exec("CREATE TABLE IF NOT EXISTS migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )");
    }

    private function applied(): array
    {
        return $this->pdo->query('SELECT name FROM migrations ORDER BY id')->fetchAll(\PDO::FETCH_COLUMN);
    }

    private function record(string $name): void
    {
        $this->pdo->prepare('INSERT INTO migrations (name) VALUES (:n)')->execute(['n' => $name]);
    }

    /** @return list<MigrationInterface> */
    private function all(): array
    {
        return [new CreateUsersTable()]; // add new migrations here in order
    }
}
```

---

## 11. SECURITY — COMPREHENSIVE GUIDE

### 11.1 SQL Injection Prevention

```php
<?php
declare(strict_types=1);

// ALWAYS use prepared statements
$stmt = $pdo->prepare('SELECT * FROM users WHERE email=:email AND status=:s');
$stmt->execute(['email' => $email, 's' => 'active']);

// Integer params — explicit type
$stmt = $pdo->prepare('SELECT * FROM orders WHERE user_id=:id');
$stmt->bindValue(':id', $userId, \PDO::PARAM_INT);
$stmt->execute();

// Dynamic column names — whitelist only
function buildOrderBy(string $col, string $dir): string
{
    $cols = ['id','name','email','created_at'];
    $dirs = ['ASC','DESC'];
    if (!in_array($col, $cols, true))        throw new \InvalidArgumentException("Bad column: {$col}");
    if (!in_array(strtoupper($dir),$dirs,true)) throw new \InvalidArgumentException("Bad dir: {$dir}");
    return "{$col} " . strtoupper($dir);
}

// NEVER:
// "SELECT * FROM users WHERE id = {$_GET['id']}"        — injection
// "SELECT * FROM users WHERE name = '" . $name . "'"    — injection
// sprintf("SELECT * FROM users WHERE id = '%s'", $id)   — injection
```

### 11.2 Password Hashing

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Security;

final class BcryptPasswordHasher implements PasswordHasherInterface
{
    private const int COST = 12; // ~250ms on modern hardware

    public function hash(string $plain): string
    {
        if ($plain === '') throw new \InvalidArgumentException('Password cannot be empty.');
        // Pre-hash if > 72 bytes (bcrypt silently truncates)
        if (strlen($plain) > 72) $plain = base64_encode(hash('sha512', $plain, binary: true));
        $hash = password_hash($plain, PASSWORD_BCRYPT, ['cost' => self::COST]);
        if ($hash === false) throw new \RuntimeException('password_hash() failed.');
        return $hash;
    }

    public function verify(string $plain, string $hash): bool
    {
        if (strlen($plain) > 72) $plain = base64_encode(hash('sha512', $plain, binary: true));
        return password_verify($plain, $hash);
    }

    public function needsRehash(string $hash): bool
    {
        return password_needs_rehash($hash, PASSWORD_BCRYPT, ['cost' => self::COST]);
    }
}

// NEVER:
// md5($password) sha1($password) crypt($password) base64_encode($password)

// On login — upgrade hash if needed
if ($hasher->verify($input, $user->passwordHash())) {
    if ($hasher->needsRehash($user->passwordHash())) {
        $repo->updatePassword($user->id(), $hasher->hash($input));
    }
    // login success
}
```

### 11.3 XSS Prevention

```php
<?php
declare(strict_types=1);

// Escape ALL output in HTML context
function e(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'UTF-8');
}
// In templates: <div><?= e($user->name()) ?></div>

// JSON output
header('Content-Type: application/json; charset=utf-8');
echo json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);

// Security headers
function setSecurityHeaders(): void
{
    header("Content-Security-Policy: default-src 'self'; script-src 'self'; frame-ancestors 'none'");
    header("X-Content-Type-Options: nosniff");
    header("X-Frame-Options: DENY");
    header("Referrer-Policy: strict-origin-when-cross-origin");
    header("Permissions-Policy: geolocation=(), camera=(), microphone=()");
}
```

### 11.4 CSRF Protection

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Security;

final class CsrfTokenManager
{
    private const string KEY   = '__csrf_token';
    private const int    BYTES = 32;

    public function generateToken(): string
    {
        if (session_status() !== PHP_SESSION_ACTIVE) {
            throw new \RuntimeException('Session must be active before generating CSRF token.');
        }
        if (!isset($_SESSION[self::KEY])) {
            $_SESSION[self::KEY] = bin2hex(random_bytes(self::BYTES));
        }
        return $_SESSION[self::KEY];
    }

    public function validateToken(string $submitted): bool
    {
        $expected = $_SESSION[self::KEY] ?? '';
        return $expected !== '' && hash_equals($expected, $submitted); // timing-safe
    }

    public function rotate(): string
    {
        unset($_SESSION[self::KEY]);
        return $this->generateToken();
    }
}
// In form: <input type="hidden" name="_csrf" value="<?= $csrf->generateToken() ?>">
// On submit: if (!$csrf->validateToken($_POST['_csrf'] ?? '')) { throw new ForbiddenException(); }
```

### 11.5 Timing-Safe Comparisons

```php
<?php
declare(strict_types=1);

// ALWAYS use hash_equals() for secrets — regular === leaks timing info

// Bad:  if ($token === $expected) { ... }
// Good: if (hash_equals($expected, $token)) { ... }

// Verify HMAC signatures
function verifyHmac(string $payload, string $signature, string $secret): bool
{
    $expected = hash_hmac('sha256', $payload, $secret);
    return hash_equals($expected, $signature);
}
```

### 11.6 File Upload Security

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Security;

final class SecureFileUploader
{
    private const array ALLOWED = [
        'image/jpeg' => 'jpg', 'image/png' => 'png',
        'image/gif'  => 'gif', 'image/webp' => 'webp',
        'application/pdf' => 'pdf',
    ];
    private const int MAX_SIZE = 10 * 1_048_576; // 10 MB

    public function __construct(private readonly string $uploadDir) {}

    public function upload(array $file): array
    {
        $this->assertNoError($file['error'] ?? UPLOAD_ERR_NO_FILE);
        $this->assertSize($file['size'] ?? 0);

        $mime = (new \finfo(FILEINFO_MIME_TYPE))->file($file['tmp_name']);
        $ext  = self::ALLOWED[$mime] ?? throw new \InvalidArgumentException("Type not allowed: {$mime}");

        if (substr_count(basename($file['name'] ?? ''), '.') > 1) {
            throw new \InvalidArgumentException('Multiple extensions not allowed.');
        }

        $stored = bin2hex(random_bytes(16)) . '.' . $ext;
        $dest   = $this->uploadDir . DIRECTORY_SEPARATOR . $stored;

        if (!move_uploaded_file($file['tmp_name'], $dest)) {
            throw new \RuntimeException('Failed to move uploaded file.');
        }

        return ['stored_name' => $stored, 'mime_type' => $mime, 'size' => $file['size']];
    }

    private function assertNoError(int $code): void
    {
        if ($code === UPLOAD_ERR_OK) return;
        throw new \InvalidArgumentException(match($code) {
            UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE => 'File exceeds size limit.',
            UPLOAD_ERR_PARTIAL  => 'File only partially uploaded.',
            UPLOAD_ERR_NO_FILE  => 'No file uploaded.',
            default             => "Upload error #{$code}.",
        });
    }

    private function assertSize(int $size): void
    {
        if ($size > self::MAX_SIZE) throw new \InvalidArgumentException('File too large.');
    }
}
```

### 11.7 Rate Limiting

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Security;

final class RateLimiter
{
    public function __construct(private readonly \Redis $redis) {}

    public function attempt(string $key, int $max, int $window): bool
    {
        $k       = "rate:{$key}";
        $current = (int)($this->redis->get($k) ?: 0);
        if ($current >= $max) return false;

        $pipe = $this->redis->pipeline();
        $pipe->incr($k);
        if ($current === 0) $pipe->expire($k, $window);
        $pipe->exec();
        return true;
    }

    public function remaining(string $key, int $max): int
    {
        return max(0, $max - (int)($this->redis->get("rate:{$key}") ?: 0));
    }

    public function ttl(string $key): int   { return max(0, $this->redis->ttl("rate:{$key}")); }
    public function clear(string $key): void { $this->redis->del("rate:{$key}"); }
}
```

---

## 12. HTTP: REQUESTS & RESPONSES

### 12.1 Request Object

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http;

final class Request
{
    private ?string $rawBody  = null;
    private ?array  $jsonBody = null;

    private function __construct(
        private readonly string $method,
        private readonly string $path,
        private readonly array  $query,
        private readonly array  $post,
        private readonly array  $files,
        private readonly array  $headers,
        private readonly array  $server,
        private readonly array  $cookies,
        private array           $attributes,
    ) {}

    public static function fromGlobals(): self
    {
        return new self(
            method:     strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET'),
            path:       parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?? '/',
            query:      $_GET,
            post:       $_POST,
            files:      $_FILES,
            headers:    self::extractHeaders(),
            server:     $_SERVER,
            cookies:    $_COOKIE,
            attributes: [],
        );
    }

    public function withAttributes(array $attrs): self
    {
        $clone = clone $this;
        $clone->attributes = array_merge($this->attributes, $attrs);
        return $clone;
    }

    // Method
    public function method(): string   { return $this->method; }
    public function isGet(): bool      { return $this->method === 'GET'; }
    public function isPost(): bool     { return $this->method === 'POST'; }
    public function isPut(): bool      { return $this->method === 'PUT'; }
    public function isPatch(): bool    { return $this->method === 'PATCH'; }
    public function isDelete(): bool   { return $this->method === 'DELETE'; }
    public function isOptions(): bool  { return $this->method === 'OPTIONS'; }

    // URL
    public function path(): string     { return $this->path; }
    public function isSecure(): bool   {
        return ($this->server['HTTPS'] ?? 'off') !== 'off'
            || ($this->server['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
    }

    // Query
    public function query(string $key, mixed $default = null): mixed { return $this->query[$key] ?? $default; }
    public function queryInt(string $key, int $default = 0): int     { return (int)($this->query[$key] ?? $default); }
    public function queryString(string $key, string $default = ''): string { return (string)($this->query[$key] ?? $default); }

    // Body
    public function post_(string $key, mixed $default = null): mixed { return $this->post[$key] ?? $default; }

    public function json(): array
    {
        if ($this->jsonBody !== null) return $this->jsonBody;
        $raw = $this->rawBody();
        if ($raw === '') return $this->jsonBody = [];
        try {
            $d = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
            return $this->jsonBody = is_array($d) ? $d : [];
        } catch (\JsonException $e) {
            throw new \InvalidArgumentException('Invalid JSON: ' . $e->getMessage());
        }
    }

    public function input(string $key, mixed $default = null): mixed
    {
        $json = []; try { $json = $this->json(); } catch (\Throwable) {}
        return $json[$key] ?? $this->post[$key] ?? $this->query[$key] ?? $default;
    }

    public function all(): array
    {
        $json = []; try { $json = $this->json(); } catch (\Throwable) {}
        return array_merge($this->query, $this->post, $json);
    }

    public function rawBody(): string { return $this->rawBody ??= (string)file_get_contents('php://input'); }

    // Headers
    public function header(string $name, ?string $default = null): ?string
    {
        return $this->headers[strtolower($name)] ?? $default;
    }
    public function bearerToken(): ?string
    {
        $auth = $this->header('authorization', '');
        return str_starts_with($auth, 'Bearer ') ? substr($auth, 7) : null;
    }
    public function isJson(): bool    { return str_contains($this->header('content-type',''), 'application/json'); }
    public function isAjax(): bool    { return $this->header('x-requested-with') === 'XMLHttpRequest'; }
    public function acceptsJson(): bool { return str_contains($this->header('accept',''), 'application/json'); }

    // Misc
    public function ip(): string      { return $this->server['REMOTE_ADDR'] ?? '127.0.0.1'; }
    public function userAgent(): string { return $this->server['HTTP_USER_AGENT'] ?? ''; }
    public function file(string $key): ?array  { return $this->files[$key] ?? null; }
    public function cookie(string $key, ?string $default = null): ?string { return $this->cookies[$key] ?? $default; }
    public function attribute(string $key, mixed $default = null): mixed  { return $this->attributes[$key] ?? $default; }

    private static function extractHeaders(): array
    {
        $headers = [];
        if (function_exists('getallheaders')) {
            foreach ((getallheaders() ?: []) as $n => $v) $headers[strtolower($n)] = $v;
            return $headers;
        }
        foreach ($_SERVER as $k => $v) {
            if (str_starts_with($k, 'HTTP_')) $headers[strtolower(str_replace('_','-',substr($k,5)))] = $v;
            elseif ($k === 'CONTENT_TYPE')   $headers['content-type']   = $v;
            elseif ($k === 'CONTENT_LENGTH') $headers['content-length'] = $v;
        }
        return $headers;
    }
}
```

### 12.2 Response Object

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http;

final class Response
{
    private function __construct(
        private readonly int    $status,
        private readonly string $body,
        private readonly array  $headers,
    ) {}

    public static function json(mixed $data, int $status = 200): self
    {
        return new self($status,
            json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            ['Content-Type' => 'application/json; charset=utf-8']
        );
    }

    public static function html(string $html, int $status = 200): self
    {
        return new self($status, $html, ['Content-Type' => 'text/html; charset=utf-8']);
    }

    public static function redirect(string $url, int $status = 302): self
    {
        return new self($status, '', ['Location' => $url]);
    }

    public static function noContent(): self { return new self(204, '', []); }

    public function withHeader(string $name, string $value): self
    {
        $h = $this->headers; $h[$name] = $value;
        return new self($this->status, $this->body, $h);
    }

    public function withCors(string $origin='*'): self
    {
        return $this
            ->withHeader('Access-Control-Allow-Origin',  $origin)
            ->withHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
            ->withHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
            ->withHeader('Access-Control-Max-Age',       '86400');
    }

    public function send(): void
    {
        http_response_code($this->status);
        foreach ($this->headers as $n => $v) header("{$n}: {$v}");
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: DENY');
        if ($this->status !== 204) echo $this->body;
    }

    public function status(): int    { return $this->status; }
    public function body(): string   { return $this->body; }
    public function headers(): array { return $this->headers; }
}
```

---

## 13. ROUTING

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http;

final class Route
{
    public readonly string $regex;
    /** @var list<string> */
    public readonly array $paramNames;

    public function __construct(
        public readonly string          $method,
        public readonly string          $pattern,
        public readonly string|callable $handler,
        /** @var list<string> */
        public readonly array           $middleware = [],
    ) {
        [$this->regex, $this->paramNames] = $this->compile($pattern);
    }

    /** @return array<string,string>|null */
    public function match(string $path): ?array
    {
        if (!preg_match($this->regex, $path, $m)) return null;
        $params = [];
        foreach ($this->paramNames as $i => $n) $params[$n] = urldecode($m[$i+1]);
        return $params;
    }

    /** @return array{string, list<string>} */
    private function compile(string $pattern): array
    {
        $names = [];
        $regex = preg_replace_callback(
            '#\{([a-zA-Z_]\w*)(?::([^}]+))?\}#',
            function (array $m) use (&$names): string {
                $names[] = $m[1];
                return '(' . ($m[2] ?? '[^/]+') . ')';
            },
            $pattern
        );
        return ['#^' . $regex . '$#u', $names];
    }
}

final class Router
{
    /** @var list<Route> */
    private array $routes = [];
    private string $prefix = '';
    /** @var list<string> */
    private array $globalMiddleware = [];

    public function get(string $p, string|callable $h): self    { return $this->add('GET',    $p, $h); }
    public function post(string $p, string|callable $h): self   { return $this->add('POST',   $p, $h); }
    public function put(string $p, string|callable $h): self    { return $this->add('PUT',    $p, $h); }
    public function patch(string $p, string|callable $h): self  { return $this->add('PATCH',  $p, $h); }
    public function delete(string $p, string|callable $h): self { return $this->add('DELETE', $p, $h); }

    public function resource(string $base, string $ctrl): self
    {
        $this->get($base,              "{$ctrl}::index");
        $this->post($base,             "{$ctrl}::store");
        $this->get("{$base}/{id}",     "{$ctrl}::show");
        $this->put("{$base}/{id}",     "{$ctrl}::update");
        $this->patch("{$base}/{id}",   "{$ctrl}::patch");
        $this->delete("{$base}/{id}",  "{$ctrl}::destroy");
        return $this;
    }

    public function group(string $prefix, callable $cb, array $middleware = []): self
    {
        $g = new self();
        $g->prefix           = $this->prefix . $prefix;
        $g->globalMiddleware = array_merge($this->globalMiddleware, $middleware);
        $cb($g);
        foreach ($g->routes as $r) $this->routes[] = $r;
        return $this;
    }

    public function dispatch(Request $request, Container $container): Response
    {
        if ($request->isOptions()) return Response::noContent()->withCors();

        foreach ($this->routes as $route) {
            if ($route->method !== $request->method()) continue;
            $params = $route->match($request->path());
            if ($params === null) continue;
            return $this->run($route, $request->withAttributes($params), $params, $container);
        }

        return Response::json(['error' => 'Not Found'], 404);
    }

    private function add(string $method, string $pattern, string|callable $handler): self
    {
        $this->routes[] = new Route($method, $this->prefix.$pattern, $handler, $this->globalMiddleware);
        return $this;
    }

    private function run(Route $route, Request $request, array $params, Container $c): Response
    {
        $final = function (Request $req) use ($route, $params, $c): Response {
            if (is_callable($route->handler)) return ($route->handler)($req, $params);
            [$class, $method] = explode('::', $route->handler, 2);
            return $c->get($class)->$method($req, $params);
        };

        $stack = array_reverse($route->middleware);
        foreach ($stack as $mwClass) {
            $mw    = $c->get($mwClass);
            $next  = $final;
            $final = fn(Request $req) => $mw->process($req, $next);
        }

        return $final($request);
    }
}
```

---

## 14. MIDDLEWARE PIPELINE

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http\Middleware;

interface MiddlewareInterface
{
    public function process(Request $request, callable $next): Response;
}

// Request Logging
final class RequestLoggingMiddleware implements MiddlewareInterface
{
    public function __construct(private readonly LoggerInterface $logger) {}
    public function process(Request $request, callable $next): Response
    {
        $start = hrtime(true);
        $id    = bin2hex(random_bytes(8));
        $this->logger->info('Request', ['id'=>$id,'method'=>$request->method(),'path'=>$request->path()]);
        $response = $next($request->withAttributes(['request_id' => $id]));
        $ms = round((hrtime(true) - $start) / 1_000_000, 2);
        $this->logger->info('Response', ['id'=>$id,'status'=>$response->status(),'ms'=>$ms]);
        return $response->withHeader('X-Request-Id', $id);
    }
}

// JWT Authentication
final class JwtAuthMiddleware implements MiddlewareInterface
{
    public function __construct(
        private readonly JwtService              $jwt,
        private readonly UserRepositoryInterface $users,
    ) {}
    public function process(Request $request, callable $next): Response
    {
        $token = $request->bearerToken();
        if ($token === null) return Response::json(['error' => 'Missing bearer token.'], 401);
        try {
            $claims = $this->jwt->verify($token);
        } catch (JwtException) {
            return Response::json(['error' => 'Invalid or expired token.'], 401);
        }
        $user = $this->users->findById(new UserId((int)$claims['sub']));
        if ($user === null || !$user->isActive()) return Response::json(['error' => 'User not found.'], 401);
        return $next($request->withAttributes(['authenticated_user' => $user]));
    }
}

// CORS
final class CorsMiddleware implements MiddlewareInterface
{
    /** @param list<string> $allowedOrigins */
    public function __construct(private readonly array $allowedOrigins = ['*']) {}
    public function process(Request $request, callable $next): Response
    {
        $origin = $request->header('origin', '');
        if ($request->isOptions()) return Response::noContent()->withCors($this->resolve($origin));
        return $next($request)->withCors($this->resolve($origin));
    }
    private function resolve(string $origin): string
    {
        return $this->allowedOrigins === ['*'] ? '*'
             : (in_array($origin, $this->allowedOrigins, true) ? $origin : '');
    }
}

// Rate Limiting
final class RateLimitMiddleware implements MiddlewareInterface
{
    public function __construct(
        private readonly RateLimiter $limiter,
        private readonly int $max    = 60,
        private readonly int $window = 60,
    ) {}
    public function process(Request $request, callable $next): Response
    {
        $key = "api:{$request->ip()}";
        if (!$this->limiter->attempt($key, $this->max, $this->window)) {
            return Response::json(['error' => 'Too many requests.'], 429)
                ->withHeader('Retry-After', (string)$this->limiter->ttl($key))
                ->withHeader('X-RateLimit-Remaining', '0');
        }
        return $next($request)
            ->withHeader('X-RateLimit-Limit',     (string)$this->max)
            ->withHeader('X-RateLimit-Remaining', (string)$this->limiter->remaining($key, $this->max));
    }
}

// JSON Content-Type enforcement
final class RequireJsonMiddleware implements MiddlewareInterface
{
    public function process(Request $request, callable $next): Response
    {
        if (in_array($request->method(), ['POST','PUT','PATCH'], true) && !$request->isJson()) {
            return Response::json(['error' => 'Content-Type must be application/json.'], 415);
        }
        return $next($request);
    }
}
```

---

## 15. DEPENDENCY INJECTION & SERVICE CONTAINER

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Container;

final class Container
{
    /** @var array<string, callable> */
    private array $bindings = [];
    /** @var array<string, object> */
    private array $instances = [];
    /** @var array<string, object> */
    private array $singletons = [];

    public function bind(string $id, callable $factory): void
    {
        $this->bindings[$id] = $factory;
    }

    public function singleton(string $id, callable $factory): void
    {
        $this->bindings[$id] = function (self $c) use ($id, $factory): object {
            if (!array_key_exists($id, $this->singletons)) {
                $this->singletons[$id] = $factory($c);
            }
            return $this->singletons[$id];
        };
    }

    public function instance(string $id, object $obj): void
    {
        $this->instances[$id] = $obj;
    }

    public function get(string $id): mixed
    {
        if (array_key_exists($id, $this->instances)) return $this->instances[$id];
        if (array_key_exists($id, $this->bindings))  return ($this->bindings[$id])($this);
        if (class_exists($id)) return $this->autowire($id);
        throw new \RuntimeException("No binding for: {$id}");
    }

    public function has(string $id): bool
    {
        return array_key_exists($id, $this->instances)
            || array_key_exists($id, $this->bindings)
            || class_exists($id);
    }

    public function make(string $class, array $overrides = []): object
    {
        return $this->autowire($class, $overrides);
    }

    /** @param array<string, mixed> $overrides */
    private function autowire(string $class, array $overrides = []): object
    {
        if (!class_exists($class)) throw new \RuntimeException("Class not found: {$class}");
        $ref = new \ReflectionClass($class);
        if (!$ref->isInstantiable()) throw new \RuntimeException("Not instantiable: {$class}");
        $ctor = $ref->getConstructor();
        if ($ctor === null) return $ref->newInstance();

        $args = [];
        foreach ($ctor->getParameters() as $param) {
            $name = $param->getName();
            if (array_key_exists($name, $overrides)) { $args[] = $overrides[$name]; continue; }
            $type = $param->getType();
            if ($type instanceof \ReflectionNamedType && !$type->isBuiltin()) {
                try { $args[] = $this->get($type->getName()); }
                catch (\Throwable $e) {
                    if ($param->isDefaultValueAvailable()) $args[] = $param->getDefaultValue();
                    elseif ($type->allowsNull()) $args[] = null;
                    else throw new \RuntimeException("Cannot resolve '{$name}' in {$class}", 0, $e);
                }
            } elseif ($param->isDefaultValueAvailable()) {
                $args[] = $param->getDefaultValue();
            } else {
                throw new \RuntimeException("Cannot resolve scalar '{$name}' in {$class}.");
            }
        }
        return $ref->newInstanceArgs($args);
    }
}
```

---

## 16. CONFIGURATION & ENVIRONMENT

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Config;

final class EnvLoader
{
    public static function load(string $file): void
    {
        if (!is_file($file) || !is_readable($file)) return;
        foreach (file($file, FILE_IGNORE_NEW_LINES|FILE_SKIP_EMPTY_LINES) ?: [] as $line) {
            $line = trim($line);
            if ($line===''||$line[0]==='#'||!str_contains($line,'=')) continue;
            [$key, $val] = explode('=', $line, 2);
            $key = trim($key); $val = trim($val);
            // Strip quotes
            if (strlen($val)>=2) {
                $f=$val[0]; $l=$val[-1];
                if (($f==='"'&&$l==='"')||($f==="'"&&$l==="'")) $val=substr($val,1,-1);
            }
            if (!array_key_exists($key,$_ENV) && getenv($key)===false) {
                $_ENV[$key]=$val; putenv("{$key}={$val}");
            }
        }
    }
}

final class Config
{
    /** @var array<string, mixed> */
    private static array $cache = [];

    public static function get(string $key, mixed $default = null): mixed
    {
        if (array_key_exists($key, self::$cache)) return self::$cache[$key];
        $raw = $_ENV[$key] ?? getenv($key);
        if ($raw === false || $raw === null) return self::$cache[$key] = $default;
        return self::$cache[$key] = self::cast((string)$raw);
    }

    public static function string(string $key, string $default = ''): string  { return (string)(self::get($key) ?? $default); }
    public static function int(string $key, int $default = 0): int            { return (int)(self::get($key) ?? $default); }
    public static function float(string $key, float $default = 0.0): float    { return (float)(self::get($key) ?? $default); }
    public static function bool(string $key, bool $default = false): bool     { return (bool)(self::get($key) ?? $default); }

    public static function required(string $key): string
    {
        $v = self::get($key);
        if ($v === null || $v === '') throw new \RuntimeException("Required env var '{$key}' is not set.");
        return (string)$v;
    }

    private static function cast(string $v): mixed
    {
        return match(strtolower($v)) {
            'true','(true)'   => true,
            'false','(false)' => false,
            'null','(null)'   => null,
            'empty','(empty)' => '',
            default           => $v,
        };
    }
}

// Usage:
EnvLoader::load(__DIR__ . '/../.env');
$dbHost = Config::string('DB_HOST', '127.0.0.1');
$debug  = Config::bool('APP_DEBUG', false);
$port   = Config::int('DB_PORT', 3306);
$apiKey = Config::required('STRIPE_SECRET_KEY'); // throws if not set
```

---

## 17. CACHING STRATEGIES

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Cache;

interface CacheInterface
{
    public function get(string $key): mixed;
    public function set(string $key, mixed $value, int $ttl = 3600): bool;
    public function delete(string $key): bool;
    public function has(string $key): bool;
    public function flush(): bool;
    /**
     * @template T
     * @param callable(): T $callback
     * @return T
     */
    public function remember(string $key, int $ttl, callable $callback): mixed;
}

final class RedisCache implements CacheInterface
{
    private const string PREFIX = 'cache:';

    public function __construct(private readonly \Redis $redis) {}

    public function get(string $key): mixed
    {
        $v = $this->redis->get(self::PREFIX.$key);
        return $v !== false ? unserialize($v) : null;
    }
    public function set(string $key, mixed $value, int $ttl = 3600): bool
    {
        return (bool)$this->redis->setex(self::PREFIX.$key, $ttl, serialize($value));
    }
    public function delete(string $key): bool { return $this->redis->del(self::PREFIX.$key) > 0; }
    public function has(string $key): bool    { return (bool)$this->redis->exists(self::PREFIX.$key); }
    public function flush(): bool
    {
        $keys = $this->redis->keys(self::PREFIX.'*');
        return empty($keys) || $this->redis->del(...$keys) >= 0;
    }
    public function remember(string $key, int $ttl, callable $cb): mixed
    {
        $v = $this->get($key);
        if ($v !== null) return $v;
        $v = $cb(); $this->set($key, $v, $ttl); return $v;
    }
    public function increment(string $key, int $by = 1): int
    {
        return $this->redis->incrBy(self::PREFIX.$key, $by);
    }
}

final class FileCache implements CacheInterface
{
    public function __construct(private readonly string $dir) {}

    public function get(string $key): mixed
    {
        $f = $this->path($key);
        if (!file_exists($f)) return null;
        $d = unserialize(file_get_contents($f));
        if ($d['expires'] < time()) { $this->delete($key); return null; }
        return $d['value'];
    }
    public function set(string $key, mixed $value, int $ttl = 3600): bool
    {
        return file_put_contents($this->path($key),
            serialize(['value'=>$value,'expires'=>time()+$ttl]), LOCK_EX) !== false;
    }
    public function delete(string $key): bool  { return @unlink($this->path($key)); }
    public function has(string $key): bool     { return $this->get($key) !== null; }
    public function flush(): bool              { foreach (glob($this->dir.'/*.cache')?:[] as $f) unlink($f); return true; }
    public function remember(string $key, int $ttl, callable $cb): mixed
    {
        $v=$this->get($key); if($v!==null)return $v;
        $v=$cb(); $this->set($key,$v,$ttl); return $v;
    }
    private function path(string $key): string { return $this->dir.'/'.md5($key).'.cache'; }
}
```

---

## 18. LOGGING

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Logging;

enum LogLevel: string
{
    case Debug     = 'DEBUG';
    case Info      = 'INFO';
    case Notice    = 'NOTICE';
    case Warning   = 'WARNING';
    case Error     = 'ERROR';
    case Critical  = 'CRITICAL';
    case Alert     = 'ALERT';
    case Emergency = 'EMERGENCY';

    public function weight(): int
    {
        return match($this) {
            self::Debug=>0,self::Info=>1,self::Notice=>2,self::Warning=>3,
            self::Error=>4,self::Critical=>5,self::Alert=>6,self::Emergency=>7,
        };
    }
}

interface LoggerInterface
{
    public function debug(string $msg, array $ctx = []): void;
    public function info(string $msg, array $ctx = []): void;
    public function notice(string $msg, array $ctx = []): void;
    public function warning(string $msg, array $ctx = []): void;
    public function error(string $msg, array $ctx = []): void;
    public function critical(string $msg, array $ctx = []): void;
    public function alert(string $msg, array $ctx = []): void;
    public function emergency(string $msg, array $ctx = []): void;
}

final class FileLogger implements LoggerInterface
{
    public function __construct(
        private readonly string   $file,
        private readonly LogLevel $minLevel = LogLevel::Debug,
    ) {}

    public function debug(string $m, array $c=[]): void     { $this->write(LogLevel::Debug,    $m,$c); }
    public function info(string $m, array $c=[]): void      { $this->write(LogLevel::Info,     $m,$c); }
    public function notice(string $m, array $c=[]): void    { $this->write(LogLevel::Notice,   $m,$c); }
    public function warning(string $m, array $c=[]): void   { $this->write(LogLevel::Warning,  $m,$c); }
    public function error(string $m, array $c=[]): void     { $this->write(LogLevel::Error,    $m,$c); }
    public function critical(string $m, array $c=[]): void  { $this->write(LogLevel::Critical, $m,$c); }
    public function alert(string $m, array $c=[]): void     { $this->write(LogLevel::Alert,    $m,$c); }
    public function emergency(string $m, array $c=[]): void { $this->write(LogLevel::Emergency,$m,$c); }

    private function write(LogLevel $level, string $message, array $context): void
    {
        if ($level->weight() < $this->minLevel->weight()) return;

        $interpolated = preg_replace_callback('/\{([^}]+)\}/', function ($m) use ($context) {
            $v = $context[$m[1]] ?? $m[0];
            return is_scalar($v) ? (string)$v : $m[0];
        }, $message);

        $ctx  = empty($context) ? '' : ' ' . json_encode($context, JSON_UNESCAPED_UNICODE);
        $line = sprintf("[%s] [%s] [pid:%s] %s%s\n",
            (new \DateTimeImmutable())->format('Y-m-d H:i:s.u'),
            $level->value, getmypid(), $interpolated, $ctx
        );
        file_put_contents($this->file, $line, FILE_APPEND|LOCK_EX);
    }
}
```

---

## 19. INPUT VALIDATION

```php
<?php
declare(strict_types=1);
namespace App\Application\Validation;

interface RuleInterface
{
    public function passes(string $field, mixed $value, array $data): bool;
    public function message(string $field): string;
}

final class Required implements RuleInterface {
    public function passes(string $f, mixed $v, array $d): bool { return $v!==null&&$v!==''&&$v!=[]; }
    public function message(string $f): string { return "The {$f} field is required."; }
}
final class EmailRule implements RuleInterface {
    public function passes(string $f, mixed $v, array $d): bool {
        return is_string($v) && filter_var($v, FILTER_VALIDATE_EMAIL) !== false;
    }
    public function message(string $f): string { return "The {$f} must be a valid email."; }
}
final class MinLength implements RuleInterface {
    public function __construct(private readonly int $min) {}
    public function passes(string $f, mixed $v, array $d): bool { return is_string($v)&&mb_strlen($v)>=$this->min; }
    public function message(string $f): string { return "The {$f} must be at least {$this->min} characters."; }
}
final class MaxLength implements RuleInterface {
    public function __construct(private readonly int $max) {}
    public function passes(string $f, mixed $v, array $d): bool { return is_string($v)&&mb_strlen($v)<=$this->max; }
    public function message(string $f): string { return "The {$f} must not exceed {$this->max} characters."; }
}
final class IsInteger implements RuleInterface {
    public function passes(string $f, mixed $v, array $d): bool { return filter_var($v,FILTER_VALIDATE_INT)!==false; }
    public function message(string $f): string { return "The {$f} must be an integer."; }
}
final class Min implements RuleInterface {
    public function __construct(private readonly int|float $min) {}
    public function passes(string $f, mixed $v, array $d): bool { return is_numeric($v)&&$v>=$this->min; }
    public function message(string $f): string { return "The {$f} must be at least {$this->min}."; }
}
final class Max implements RuleInterface {
    public function __construct(private readonly int|float $max) {}
    public function passes(string $f, mixed $v, array $d): bool { return is_numeric($v)&&$v<=$this->max; }
    public function message(string $f): string { return "The {$f} must not exceed {$this->max}."; }
}
final class InList implements RuleInterface {
    /** @param list<mixed> $allowed */
    public function __construct(private readonly array $allowed) {}
    public function passes(string $f, mixed $v, array $d): bool { return in_array($v,$this->allowed,true); }
    public function message(string $f): string { return "The {$f} must be one of: ".implode(', ',$this->allowed)."."; }
}
final class Confirmed implements RuleInterface {
    public function passes(string $f, mixed $v, array $d): bool { return ($d["{$f}_confirmation"]??null)===$v; }
    public function message(string $f): string { return "The {$f} confirmation does not match."; }
}
final class UrlRule implements RuleInterface {
    public function passes(string $f, mixed $v, array $d): bool {
        return is_string($v)&&filter_var($v,FILTER_VALIDATE_URL)!==false;
    }
    public function message(string $f): string { return "The {$f} must be a valid URL."; }
}
final class Regex implements RuleInterface {
    public function __construct(private readonly string $pattern, private readonly string $hint='') {}
    public function passes(string $f, mixed $v, array $d): bool { return is_string($v)&&(bool)preg_match($this->pattern,$v); }
    public function message(string $f): string { return $this->hint?:"The {$f} format is invalid."; }
}

final class Validator
{
    /** @var array<string, list<string>> */
    private array $errors = [];

    /**
     * @param array<string, list<RuleInterface>> $rules
     */
    public function validate(array $data, array $rules): bool
    {
        $this->errors = [];
        foreach ($rules as $field => $fieldRules) {
            $value = $data[$field] ?? null;
            foreach ($fieldRules as $rule) {
                if (!$rule->passes($field, $value, $data)) {
                    $this->errors[$field][] = $rule->message($field);
                }
            }
        }
        return empty($this->errors);
    }

    public function fails(): bool { return !empty($this->errors); }
    /** @return array<string, list<string>> */
    public function errors(): array { return $this->errors; }
    /** @throws ValidationException */
    public function throwIfFails(): void {
        if ($this->fails()) throw new ValidationException($this->errors);
    }
}

// Usage in controller:
$v = new Validator();
if (!$v->validate($request->json(), [
    'email'                 => [new Required(), new EmailRule(), new MaxLength(320)],
    'password'              => [new Required(), new MinLength(8), new MaxLength(72)],
    'password_confirmation' => [new Required(), new Confirmed()],
    'name'                  => [new Required(), new MinLength(2), new MaxLength(100)],
    'role'                  => [new Required(), new InList(['user','admin','moderator'])],
])) {
    return Response::json(['errors' => $v->errors()], 422);
}
```



---

## 20. REST API DESIGN & IMPLEMENTATION

### 20.1 RESTful Controller

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http\Controller;

final class UserController
{
    public function __construct(
        private readonly UserService $service,
        private readonly Validator   $validator,
    ) {}

    // GET /api/v1/users?page=1&per_page=20
    public function index(Request $request, array $params): Response
    {
        $page    = max(1, $request->queryInt('page', 1));
        $perPage = min(100, max(1, $request->queryInt('per_page', 20)));

        $result = $this->service->paginate($page, $perPage);

        return Response::json([
            'data' => array_map($this->transform(...), $result['data']),
            'meta' => [
                'total'        => $result['total'],
                'per_page'     => $result['per_page'],
                'current_page' => $result['current_page'],
                'last_page'    => $result['last_page'],
            ],
        ]);
    }

    // GET /api/v1/users/{id}
    public function show(Request $request, array $params): Response
    {
        $user = $this->service->findById((int)$params['id']);
        if ($user === null) return Response::json(['error' => 'User not found.'], 404);
        return Response::json(['data' => $this->transform($user)]);
    }

    // POST /api/v1/users
    public function store(Request $request, array $params): Response
    {
        $body = $request->json();
        $v    = new Validator();

        if (!$v->validate($body, [
            'email'    => [new Required(), new EmailRule(), new MaxLength(320)],
            'name'     => [new Required(), new MinLength(2), new MaxLength(100)],
            'password' => [new Required(), new MinLength(8)],
        ])) {
            return Response::json(['errors' => $v->errors()], 422);
        }

        try {
            $user = $this->service->createUser(new CreateUserDto(
                email:    $body['email'],
                name:     $body['name'],
                password: $body['password'],
            ));
        } catch (ConflictException $e) {
            return Response::json(['error' => $e->getMessage()], 409);
        }

        return Response::json(['data' => $this->transform($user)], 201);
    }

    // PUT /api/v1/users/{id}
    public function update(Request $request, array $params): Response
    {
        $body = $request->json();
        $v    = new Validator();

        if (!$v->validate($body, [
            'name' => [new Required(), new MinLength(2), new MaxLength(100)],
        ])) {
            return Response::json(['errors' => $v->errors()], 422);
        }

        try {
            $user = $this->service->updateUser((int)$params['id'], new UpdateUserDto(name: $body['name']));
        } catch (NotFoundException $e) {
            return Response::json(['error' => 'User not found.'], 404);
        }

        return Response::json(['data' => $this->transform($user)]);
    }

    // DELETE /api/v1/users/{id}
    public function destroy(Request $request, array $params): Response
    {
        try {
            $this->service->deleteUser((int)$params['id']);
        } catch (NotFoundException) {
            return Response::json(['error' => 'User not found.'], 404);
        }
        return Response::noContent();
    }

    private function transform(User $user): array
    {
        return [
            'id'         => $user->id()->value(),
            'email'      => $user->email()->toString(),
            'name'       => $user->name(),
            'status'     => $user->status()->value,
            'created_at' => $user->createdAt()->format(\DATE_ATOM),
            'updated_at' => $user->updatedAt()->format(\DATE_ATOM),
        ];
    }
}
```

### 20.2 API Response Standards

```
// Success with data
HTTP 200 OK
{ "data": { "id": 1, "email": "user@example.com", "name": "John" } }

// Created resource
HTTP 201 Created
{ "data": { "id": 42, ... } }

// Success with pagination
HTTP 200 OK
{
  "data": [...],
  "meta": { "total": 100, "per_page": 20, "current_page": 1, "last_page": 5 }
}

// No content (DELETE success)
HTTP 204 No Content
(empty body)

// Validation error
HTTP 422 Unprocessable Entity
{ "errors": { "email": ["Required.", "Invalid email."], "name": ["Required."] } }

// Single error
HTTP 404 Not Found
{ "error": "User not found." }

// Too many requests
HTTP 429 Too Many Requests
{ "error": "Too many requests." }
Headers: Retry-After: 60

// Server error (no details in production)
HTTP 500 Internal Server Error
{ "error": "Internal Server Error" }
```

### 20.3 Resource Transformer

```php
<?php
declare(strict_types=1);

final class UserResource
{
    public function __construct(private readonly User $user) {}

    public function toArray(): array
    {
        return [
            'id'         => $this->user->id()->value(),
            'type'       => 'user',
            'attributes' => [
                'email'      => $this->user->email()->toString(),
                'name'       => $this->user->name(),
                'status'     => $this->user->status()->value,
                'created_at' => $this->user->createdAt()->format(\DATE_ATOM),
                'updated_at' => $this->user->updatedAt()->format(\DATE_ATOM),
            ],
        ];
    }

    /** @param list<User> $users */
    public static function collection(array $users): array
    {
        return array_map(fn(User $u) => (new self($u))->toArray(), $users);
    }
}

// Paginated collection
final class PaginatedResource
{
    /**
     * @param list<array<string,mixed>> $data
     * @param array{total:int,per_page:int,current_page:int,last_page:int} $meta
     */
    public function __construct(
        private readonly array $data,
        private readonly array $meta,
    ) {}

    public function toArray(): array
    {
        return ['data' => $this->data, 'meta' => $this->meta];
    }
}
```

### 20.4 Application Service (Use Case)

```php
<?php
declare(strict_types=1);
namespace App\Application\Service;

final class UserService
{
    public function __construct(
        private readonly UserRepositoryInterface  $users,
        private readonly PasswordHasherInterface  $hasher,
        private readonly EventDispatcherInterface $dispatcher,
        private readonly LoggerInterface          $logger,
    ) {}

    public function createUser(CreateUserDto $dto): User
    {
        if ($this->users->findByEmail(new Email($dto->email)) !== null) {
            throw new ConflictException("Email '{$dto->email}' is already taken.");
        }

        $user = User::register(
            new UserId($this->nextId()),
            new Email($dto->email),
            $dto->name,
        );

        $this->users->save($user);

        $this->dispatcher->dispatch(new UserRegisteredEvent(
            $user->id()->value(),
            $user->email()->toString(),
            $user->name(),
        ));

        $this->logger->info('User registered', ['id' => $user->id()->value()]);

        return $user;
    }

    public function findById(int $id): ?User
    {
        return $this->users->findById(new UserId($id));
    }

    public function updateUser(int $id, UpdateUserDto $dto): User
    {
        $user = $this->users->findById(new UserId($id))
            ?? throw new NotFoundException('User', $id);

        if (isset($dto->name)) $user->rename($dto->name);

        $this->users->save($user);
        return $user;
    }

    public function deleteUser(int $id): void
    {
        $user = $this->users->findById(new UserId($id))
            ?? throw new NotFoundException('User', $id);

        $this->users->delete($user->id());
        $this->logger->info('User deleted', ['id' => $id]);
    }

    public function paginate(int $page, int $perPage): array
    {
        $offset = ($page - 1) * $perPage;
        $users  = $this->users->findAll($perPage, $offset);
        $total  = $this->users->countByStatus(UserStatus::Active);

        return [
            'data'         => $users,
            'total'        => $total,
            'per_page'     => $perPage,
            'current_page' => $page,
            'last_page'    => (int)ceil($total / $perPage),
        ];
    }

    private function nextId(): int { return (int)(microtime(true) * 1000); }
}
```

---

## 21. AUTHENTICATION & AUTHORIZATION

### 21.1 JWT Service

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Security;

final class JwtService
{
    private const string ALG = 'HS256';
    private const int    TTL = 3600;       // 1 hour
    private const int    REF = 2592000;    // 30 days (refresh token)

    public function __construct(
        private readonly string $secret,
        private readonly int    $ttl     = self::TTL,
        private readonly int    $refresh = self::REF,
    ) {}

    /** @param array<string, mixed> $payload */
    public function issue(array $payload): array
    {
        $now = time();
        $accessClaims = array_merge($payload, [
            'iat' => $now,
            'exp' => $now + $this->ttl,
            'jti' => bin2hex(random_bytes(16)),
            'type' => 'access',
        ]);
        $refreshClaims = [
            'sub'  => $payload['sub'],
            'iat'  => $now,
            'exp'  => $now + $this->refresh,
            'jti'  => bin2hex(random_bytes(16)),
            'type' => 'refresh',
        ];

        return [
            'access_token'  => $this->encode($accessClaims),
            'refresh_token' => $this->encode($refreshClaims),
            'expires_in'    => $this->ttl,
            'token_type'    => 'Bearer',
        ];
    }

    /** @return array<string, mixed> */
    public function verify(string $token, string $type = 'access'): array
    {
        $parts = explode('.', $token);
        if (count($parts) !== 3) throw new JwtException('Malformed token.');

        [$header, $payload, $signature] = $parts;

        if (!hash_equals($this->sign("{$header}.{$payload}"), $signature)) {
            throw new JwtException('Invalid signature.');
        }

        $claims = json_decode($this->base64decode($payload), true, 512, JSON_THROW_ON_ERROR);

        if (!is_array($claims)) throw new JwtException('Invalid payload.');

        if (isset($claims['exp']) && $claims['exp'] < time()) {
            throw new JwtException('Token expired.');
        }
        if (($claims['type'] ?? '') !== $type) {
            throw new JwtException("Expected {$type} token.");
        }

        return $claims;
    }

    private function encode(array $claims): string
    {
        $header  = $this->base64encode(json_encode(['typ'=>'JWT','alg'=>self::ALG]));
        $payload = $this->base64encode(json_encode($claims));
        $sig     = $this->sign("{$header}.{$payload}");
        return "{$header}.{$payload}.{$sig}";
    }

    private function sign(string $data): string
    {
        return $this->base64encode(hash_hmac('sha256', $data, $this->secret, true));
    }

    private function base64encode(string $data): string
    {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }

    private function base64decode(string $data): string
    {
        return base64_decode(strtr($data, '-_', '+/') . str_repeat('=', 3-(3+strlen($data))%4));
    }
}

class JwtException extends \RuntimeException {}
```

### 21.2 Auth Controller

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http\Controller;

final class AuthController
{
    public function __construct(
        private readonly UserRepositoryInterface $users,
        private readonly PasswordHasherInterface $hasher,
        private readonly JwtService              $jwt,
        private readonly RateLimiter             $limiter,
    ) {}

    // POST /api/v1/auth/login
    public function login(Request $request, array $params): Response
    {
        // Rate limit login attempts per IP
        if (!$this->limiter->attempt("login:{$request->ip()}", 5, 60)) {
            return Response::json(['error' => 'Too many login attempts. Try in 1 minute.'], 429);
        }

        $body = $request->json();
        $v    = new Validator();
        if (!$v->validate($body, [
            'email'    => [new Required(), new EmailRule()],
            'password' => [new Required()],
        ])) {
            return Response::json(['errors' => $v->errors()], 422);
        }

        $user = $this->users->findByEmail(new Email($body['email']));

        if ($user === null || !$this->hasher->verify($body['password'], $user->passwordHash())) {
            // Same message for both cases — don't leak whether email exists
            return Response::json(['error' => 'Invalid credentials.'], 401);
        }

        if (!$user->isActive()) {
            return Response::json(['error' => 'Account is not active.'], 403);
        }

        // Clear rate limit on success
        $this->limiter->clear("login:{$request->ip()}");

        // Upgrade hash if needed
        if ($this->hasher->needsRehash($user->passwordHash())) {
            $user->updatePasswordHash($this->hasher->hash($body['password']));
            $this->users->save($user);
        }

        $tokens = $this->jwt->issue(['sub' => $user->id()->value(), 'email' => $user->email()->toString()]);

        return Response::json(['data' => $tokens]);
    }

    // POST /api/v1/auth/refresh
    public function refresh(Request $request, array $params): Response
    {
        $body = $request->json();
        $refreshToken = $body['refresh_token'] ?? '';

        if ($refreshToken === '') {
            return Response::json(['error' => 'Refresh token required.'], 400);
        }

        try {
            $claims = $this->jwt->verify($refreshToken, 'refresh');
        } catch (JwtException $e) {
            return Response::json(['error' => 'Invalid or expired refresh token.'], 401);
        }

        $user = $this->users->findById(new UserId((int)$claims['sub']));
        if ($user === null || !$user->isActive()) {
            return Response::json(['error' => 'User not found or inactive.'], 401);
        }

        $tokens = $this->jwt->issue(['sub' => $user->id()->value(), 'email' => $user->email()->toString()]);
        return Response::json(['data' => $tokens]);
    }
}
```

### 21.3 Role-Based Authorization (RBAC)

```php
<?php
declare(strict_types=1);
namespace App\Domain\Auth;

enum Permission: string
{
    case ViewUsers    = 'users.view';
    case CreateUsers  = 'users.create';
    case EditUsers    = 'users.edit';
    case DeleteUsers  = 'users.delete';
    case ViewOrders   = 'orders.view';
    case ManageOrders = 'orders.manage';
    case ViewReports  = 'reports.view';
    case ManageSystem = 'system.manage';
}

enum Role: string
{
    case User      = 'user';
    case Moderator = 'moderator';
    case Admin     = 'admin';

    /** @return list<Permission> */
    public function permissions(): array
    {
        return match($this) {
            self::Admin => Permission::cases(), // all permissions
            self::Moderator => [
                Permission::ViewUsers,
                Permission::EditUsers,
                Permission::ViewOrders,
                Permission::ManageOrders,
                Permission::ViewReports,
            ],
            self::User => [
                Permission::ViewOrders,
            ],
        };
    }

    public function hasPermission(Permission $p): bool
    {
        return in_array($p, $this->permissions(), true);
    }
}

final class AuthorizationService
{
    public function can(User $user, Permission $permission): bool
    {
        return $user->role()->hasPermission($permission);
    }

    public function authorize(User $user, Permission $permission): void
    {
        if (!$this->can($user, $permission)) {
            throw new ForbiddenException(
                "Permission denied: '{$permission->value}' required."
            );
        }
    }
}

// Authorization middleware
final class RequirePermissionMiddleware implements MiddlewareInterface
{
    public function __construct(
        private readonly Permission           $permission,
        private readonly AuthorizationService $auth,
    ) {}

    public function process(Request $request, callable $next): Response
    {
        $user = $request->attribute('authenticated_user');
        if (!$user instanceof User) {
            return Response::json(['error' => 'Unauthorized.'], 401);
        }

        try {
            $this->auth->authorize($user, $this->permission);
        } catch (ForbiddenException $e) {
            return Response::json(['error' => $e->getMessage()], 403);
        }

        return $next($request);
    }
}
```

---

## 22. SESSIONS

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Http;

final class SessionManager
{
    private bool $started = false;

    public function start(): void
    {
        if ($this->started || session_status() === PHP_SESSION_ACTIVE) return;

        session_set_cookie_params([
            'lifetime' => 0,
            'path'     => '/',
            'domain'   => '',
            'secure'   => true,
            'httponly' => true,
            'samesite' => 'Strict',
        ]);

        if (!session_start()) {
            throw new \RuntimeException('Failed to start session.');
        }

        $this->started = true;
        $this->regenerateIfNeeded();
    }

    public function get(string $key, mixed $default = null): mixed
    {
        $this->assertStarted();
        return $_SESSION[$key] ?? $default;
    }

    public function set(string $key, mixed $value): void
    {
        $this->assertStarted();
        $_SESSION[$key] = $value;
    }

    public function has(string $key): bool
    {
        $this->assertStarted();
        return isset($_SESSION[$key]);
    }

    public function delete(string $key): void
    {
        $this->assertStarted();
        unset($_SESSION[$key]);
    }

    public function flash(string $key, mixed $value): void
    {
        $this->set("_flash_{$key}", $value);
    }

    public function getFlash(string $key, mixed $default = null): mixed
    {
        $flashKey = "_flash_{$key}";
        $value    = $this->get($flashKey, $default);
        $this->delete($flashKey);
        return $value;
    }

    public function regenerate(bool $deleteOld = true): void
    {
        $this->assertStarted();
        session_regenerate_id($deleteOld);
    }

    public function destroy(): void
    {
        $this->assertStarted();
        $_SESSION = [];
        if (ini_get('session.use_cookies')) {
            $p = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000,
                $p['path'], $p['domain'], $p['secure'], $p['httponly']
            );
        }
        session_destroy();
        $this->started = false;
    }

    public function id(): string { return session_id() ?: ''; }

    private function regenerateIfNeeded(): void
    {
        // Regenerate session ID every 30 minutes
        $last = $_SESSION['_last_regeneration'] ?? 0;
        if (time() - $last > 1800) {
            $this->regenerate();
            $_SESSION['_last_regeneration'] = time();
        }
    }

    private function assertStarted(): void
    {
        if (!$this->started && session_status() !== PHP_SESSION_ACTIVE) {
            throw new \RuntimeException('Session not started. Call start() first.');
        }
    }
}
```

---

## 23. EMAIL

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Mail;

final class Email
{
    /** @var list<string> */
    private array $to      = [];
    /** @var list<string> */
    private array $cc      = [];
    /** @var list<string> */
    private array $bcc     = [];
    /** @var list<array{path:string,name:string}> */
    private array $attachments = [];

    private function __construct(
        private string $subject,
        private string $htmlBody,
        private string $textBody = '',
        private string $from     = '',
        private string $replyTo  = '',
    ) {}

    public static function compose(string $subject, string $htmlBody): self
    {
        return new self($subject, $htmlBody);
    }

    public function to(string ...$addresses): self
    {
        $this->to = array_merge($this->to, $addresses);
        return $this;
    }

    public function cc(string ...$addresses): self
    {
        $this->cc = array_merge($this->cc, $addresses);
        return $this;
    }

    public function bcc(string ...$addresses): self
    {
        $this->bcc = array_merge($this->bcc, $addresses);
        return $this;
    }

    public function from(string $address): self { $this->from = $address; return $this; }
    public function replyTo(string $address): self { $this->replyTo = $address; return $this; }
    public function text(string $body): self   { $this->textBody = $body; return $this; }

    public function attach(string $path, string $name = ''): self
    {
        $this->attachments[] = ['path' => $path, 'name' => $name ?: basename($path)];
        return $this;
    }

    public function subject(): string  { return $this->subject; }
    public function htmlBody(): string { return $this->htmlBody; }
    public function textBody(): string { return $this->textBody; }
    public function from_(): string   { return $this->from; }
    public function replyTo_(): string { return $this->replyTo; }
    /** @return list<string> */
    public function to_(): array  { return $this->to; }
    /** @return list<string> */
    public function cc_(): array  { return $this->cc; }
    /** @return list<string> */
    public function bcc_(): array { return $this->bcc; }
    /** @return list<array{path:string,name:string}> */
    public function attachments(): array { return $this->attachments; }
}

interface MailerInterface
{
    public function send(Email $email): void;
}

// SMTP implementation using native PHP
final class SmtpMailer implements MailerInterface
{
    public function __construct(
        private readonly string $host,
        private readonly int    $port,
        private readonly string $username,
        private readonly string $password,
        private readonly string $defaultFrom = '',
        private readonly bool   $tls         = true,
    ) {}

    public function send(Email $email): void
    {
        $to      = implode(', ', $email->to_());
        $from    = $email->from_() ?: $this->defaultFrom;
        $subject = $email->subject();
        $uid     = md5(uniqid((string)mt_rand(), true));

        $headers  = "From: {$from}\r\n";
        $headers .= "Reply-To: " . ($email->replyTo_() ?: $from) . "\r\n";
        if ($email->cc_())  $headers .= "Cc: "  . implode(', ', $email->cc_())  . "\r\n";
        if ($email->bcc_()) $headers .= "Bcc: " . implode(', ', $email->bcc_()) . "\r\n";
        $headers .= "MIME-Version: 1.0\r\n";
        $headers .= "Content-Type: multipart/alternative; boundary=\"{$uid}\"\r\n";

        $body  = "--{$uid}\r\n";
        $body .= "Content-Type: text/plain; charset=UTF-8\r\n\r\n";
        $body .= ($email->textBody() ?: strip_tags($email->htmlBody())) . "\r\n";
        $body .= "--{$uid}\r\n";
        $body .= "Content-Type: text/html; charset=UTF-8\r\n\r\n";
        $body .= $email->htmlBody() . "\r\n";
        $body .= "--{$uid}--";

        // For production use a proper SMTP library (league/mime, symfony/mailer)
        if (!mail($to, $subject, $body, $headers)) {
            throw new \RuntimeException("Failed to send email to {$to}");
        }
    }
}

// Logging mailer for development/testing
final class LoggingMailer implements MailerInterface
{
    public function __construct(private readonly LoggerInterface $logger) {}

    public function send(Email $email): void
    {
        $this->logger->info('Email would be sent', [
            'to'      => $email->to_(),
            'subject' => $email->subject(),
        ]);
    }
}

// Null mailer for tests
final class NullMailer implements MailerInterface
{
    /** @var list<Email> */
    private array $sent = [];

    public function send(Email $email): void { $this->sent[] = $email; }

    /** @return list<Email> */
    public function sent(): array { return $this->sent; }
    public function wasNotSent(): bool { return empty($this->sent); }
}
```

---

## 24. QUEUES & BACKGROUND JOBS

### 24.1 Job Interface and Concrete Jobs

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Queue;

interface JobInterface
{
    public function handle(): void;
    public function failed(\Throwable $e): void;
    public function maxAttempts(): int;
}

abstract class AbstractJob implements JobInterface
{
    public function failed(\Throwable $e): void { /* default: do nothing */ }
    public function maxAttempts(): int          { return 3; }
}

final class SendWelcomeEmailJob extends AbstractJob
{
    public function __construct(
        private readonly int    $userId,
        private readonly string $email,
        private readonly string $name,
    ) {}

    public function handle(): void
    {
        $mailer = app()->get(MailerInterface::class);
        $mailer->send(
            Email::compose('Welcome!', "<h1>Hello, {$this->name}!</h1>")
                ->to($this->email)
        );
    }

    public function failed(\Throwable $e): void
    {
        app()->get(LoggerInterface::class)->error('Welcome email failed', [
            'user_id' => $this->userId,
            'error'   => $e->getMessage(),
        ]);
    }
}

final class ProcessImageJob extends AbstractJob
{
    public function __construct(
        private readonly string $filePath,
        private readonly int    $targetWidth,
    ) {}

    public function handle(): void
    {
        // Heavy image processing
        $img = imagecreatefromjpeg($this->filePath);
        // ... resize, save
        imagedestroy($img);
    }

    public function maxAttempts(): int { return 1; } // image processing: don't retry
}
```

### 24.2 Redis-backed Queue Manager

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Queue;

final class QueueManager
{
    private const string DEFAULT = 'default';

    public function __construct(private readonly \Redis $redis) {}

    public function push(JobInterface $job, string $queue = self::DEFAULT): void
    {
        $payload = json_encode([
            'class'     => $job::class,
            'data'      => serialize($job),
            'attempts'  => 0,
            'max'       => $job->maxAttempts(),
            'pushed_at' => time(),
        ], JSON_THROW_ON_ERROR);

        $this->redis->lPush("queue:{$queue}", $payload);
    }

    public function later(JobInterface $job, int $delaySeconds, string $queue = self::DEFAULT): void
    {
        $payload = json_encode([
            'class'    => $job::class,
            'data'     => serialize($job),
            'attempts' => 0,
            'max'      => $job->maxAttempts(),
        ], JSON_THROW_ON_ERROR);

        $this->redis->zAdd("queue:delayed:{$queue}", time() + $delaySeconds, $payload);
    }

    public function pop(string $queue = self::DEFAULT): ?array
    {
        $this->promoteDelayed($queue);
        $raw = $this->redis->rPop("queue:{$queue}");
        if ($raw === false) return null;
        return json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    }

    public function bury(array $payload, string $queue = self::DEFAULT): void
    {
        $this->redis->lPush("queue:failed:{$queue}", json_encode($payload));
    }

    public function size(string $queue = self::DEFAULT): int
    {
        return (int)$this->redis->lLen("queue:{$queue}");
    }

    private function promoteDelayed(string $queue): void
    {
        $jobs = $this->redis->zRangeByScore("queue:delayed:{$queue}", '0', (string)time());
        foreach ($jobs as $job) {
            $this->redis->multi();
            $this->redis->lPush("queue:{$queue}", $job);
            $this->redis->zRem("queue:delayed:{$queue}", $job);
            $this->redis->exec();
        }
    }
}
```

### 24.3 Queue Worker

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\Queue;

final class QueueWorker
{
    private bool $shouldStop = false;

    public function __construct(
        private readonly QueueManager    $queue,
        private readonly LoggerInterface $logger,
        private readonly Container       $container,
    ) {}

    public function work(string $queue = 'default', int $sleep = 1, int $maxJobs = 0): void
    {
        // Handle graceful shutdown signals
        if (extension_loaded('pcntl')) {
            pcntl_signal(SIGTERM, function (): void { $this->shouldStop = true; });
            pcntl_signal(SIGINT,  function (): void { $this->shouldStop = true; });
        }

        $this->logger->info("Worker started on queue '{$queue}'");
        $processed = 0;

        while (!$this->shouldStop) {
            if (extension_loaded('pcntl')) pcntl_signal_dispatch();

            $payload = $this->queue->pop($queue);

            if ($payload === null) {
                sleep($sleep);
                continue;
            }

            $this->process($payload, $queue);
            $processed++;

            if ($maxJobs > 0 && $processed >= $maxJobs) {
                $this->logger->info("Max jobs ({$maxJobs}) reached. Stopping.");
                break;
            }
        }

        $this->logger->info('Worker stopped gracefully.');
    }

    private function process(array $payload, string $queue): void
    {
        $attempts = $payload['attempts'] + 1;
        $payload['attempts'] = $attempts;

        try {
            /** @var JobInterface $job */
            $job = unserialize($payload['data']);
            $this->logger->info("Processing: {$payload['class']}", ['attempt' => $attempts]);
            $job->handle();
            $this->logger->info("Completed: {$payload['class']}");
        } catch (\Throwable $e) {
            $this->logger->error("Job failed: {$payload['class']}", [
                'attempt' => $attempts,
                'max'     => $payload['max'],
                'error'   => $e->getMessage(),
            ]);

            if ($attempts < ($payload['max'] ?? 3)) {
                // Retry with exponential backoff
                $delay = 2 ** $attempts * 5; // 10s, 20s, 40s
                $this->queue->later(unserialize($payload['data']), $delay, $queue);
            } else {
                // Bury in failed queue
                $this->queue->bury($payload, $queue);
                try { $job->failed($e); } catch (\Throwable) {}
            }
        }
    }
}
```

---

## 25. TESTING — UNIT, INTEGRATION, API

### 25.1 Unit Tests

```php
<?php
declare(strict_types=1);
namespace Tests\Unit\Domain;

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\{Test, DataProvider, CoversClass};

#[CoversClass(User::class)]
final class UserTest extends TestCase
{
    private function makeUser(string $email = 'test@example.com', string $name = 'John'): User
    {
        return User::register(new UserId(1), new Email($email), $name);
    }

    #[Test]
    public function it_creates_user_with_active_status(): void
    {
        $user = $this->makeUser();
        $this->assertTrue($user->isActive());
        $this->assertSame(UserStatus::Active, $user->status());
    }

    #[Test]
    public function it_can_be_deactivated(): void
    {
        $user = $this->makeUser();
        $user->deactivate();
        $this->assertFalse($user->isActive());
        $this->assertSame(UserStatus::Inactive, $user->status());
    }

    #[Test]
    public function it_throws_when_deactivating_already_inactive_user(): void
    {
        $user = $this->makeUser();
        $user->deactivate();

        $this->expectException(\DomainException::class);
        $this->expectExceptionMessage('already inactive');

        $user->deactivate();
    }

    #[Test]
    public function it_can_be_renamed(): void
    {
        $user = $this->makeUser(name: 'Old Name');
        $user->rename('New Name');
        $this->assertSame('New Name', $user->name());
    }

    #[Test]
    public function it_throws_on_empty_name(): void
    {
        $user = $this->makeUser();
        $this->expectException(\InvalidArgumentException::class);
        $user->rename('');
    }

    #[Test]
    public function it_normalises_email_to_lowercase(): void
    {
        $email = new Email('TEST@EXAMPLE.COM');
        $this->assertSame('test@example.com', $email->toString());
    }

    #[Test]
    #[DataProvider('invalidEmails')]
    public function it_rejects_invalid_email(string $email): void
    {
        $this->expectException(\InvalidArgumentException::class);
        new Email($email);
    }

    /** @return array<string, array{string}> */
    public static function invalidEmails(): array
    {
        return [
            'empty'            => [''],
            'no at sign'       => ['notanemail'],
            'no domain'        => ['user@'],
            'no local part'    => ['@example.com'],
            'spaces inside'    => ['user name@example.com'],
            'double at'        => ['user@@example.com'],
        ];
    }

    #[Test]
    public function money_add_works_correctly(): void
    {
        $a = new Money(1000, 'USD'); // $10.00
        $b = new Money(500,  'USD'); // $5.00
        $this->assertEquals(new Money(1500, 'USD'), $a->add($b));
    }

    #[Test]
    public function money_throws_on_currency_mismatch(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        (new Money(100, 'USD'))->add(new Money(100, 'EUR'));
    }

    #[Test]
    public function order_status_transitions_are_validated(): void
    {
        $this->assertTrue(OrderStatus::Pending->canTransitionTo(OrderStatus::Processing));
        $this->assertFalse(OrderStatus::Delivered->canTransitionTo(OrderStatus::Cancelled));
        $this->assertTrue(OrderStatus::Delivered->isFinal());
    }
}
```

### 25.2 Tests with Mock Objects

```php
<?php
declare(strict_types=1);
namespace Tests\Unit\Application;

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;
use PHPUnit\Framework\Attributes\Test;

final class UserServiceTest extends TestCase
{
    private UserRepositoryInterface&MockObject $users;
    private PasswordHasherInterface&MockObject $hasher;
    private EventDispatcherInterface&MockObject $dispatcher;
    private UserService $service;

    protected function setUp(): void
    {
        $this->users      = $this->createMock(UserRepositoryInterface::class);
        $this->hasher     = $this->createMock(PasswordHasherInterface::class);
        $this->dispatcher = $this->createMock(EventDispatcherInterface::class);
        $this->service    = new UserService($this->users, $this->hasher, $this->dispatcher,
                                            $this->createMock(LoggerInterface::class));
    }

    #[Test]
    public function it_creates_a_user_and_dispatches_event(): void
    {
        $this->users->expects($this->once())->method('findByEmail')->willReturn(null);
        $this->users->expects($this->once())->method('save');
        $this->dispatcher->expects($this->once())->method('dispatch')
            ->with($this->isInstanceOf(UserRegisteredEvent::class));

        $user = $this->service->createUser(new CreateUserDto(
            email:    'new@example.com',
            name:     'New User',
            password: 'secret123',
        ));

        $this->assertSame('new@example.com', $user->email()->toString());
        $this->assertSame('New User', $user->name());
        $this->assertTrue($user->isActive());
    }

    #[Test]
    public function it_throws_conflict_when_email_is_taken(): void
    {
        $existing = User::register(new UserId(1), new Email('taken@example.com'), 'Jane');

        $this->users->method('findByEmail')->willReturn($existing);
        $this->users->expects($this->never())->method('save');
        $this->dispatcher->expects($this->never())->method('dispatch');

        $this->expectException(ConflictException::class);

        $this->service->createUser(new CreateUserDto(
            email:    'taken@example.com',
            name:     'John',
            password: 'secret123',
        ));
    }

    #[Test]
    public function it_throws_not_found_on_delete_nonexistent(): void
    {
        $this->users->method('findById')->willReturn(null);

        $this->expectException(NotFoundException::class);
        $this->service->deleteUser(999);
    }
}
```

### 25.3 Integration Tests (SQLite in-memory)

```php
<?php
declare(strict_types=1);
namespace Tests\Integration;

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

abstract class DatabaseTestCase extends TestCase
{
    protected static \PDO $pdo;

    public static function setUpBeforeClass(): void
    {
        self::$pdo = new \PDO('sqlite::memory:', options: [
            \PDO::ATTR_ERRMODE            => \PDO::ERRMODE_EXCEPTION,
            \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC,
        ]);
    }

    // Wrap each test in a transaction and roll back for isolation
    protected function setUp(): void    { self::$pdo->beginTransaction(); }
    protected function tearDown(): void { if (self::$pdo->inTransaction()) self::$pdo->rollBack(); }
}

final class UserRepositoryTest extends DatabaseTestCase
{
    private PdoUserRepository $repo;

    public static function setUpBeforeClass(): void
    {
        parent::setUpBeforeClass();
        self::$pdo->exec("
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT NULL
            )
        ");
    }

    protected function setUp(): void
    {
        parent::setUp();
        $this->repo = new PdoUserRepository(self::$pdo);
    }

    #[Test]
    public function it_saves_and_retrieves_user(): void
    {
        $user = User::register(new UserId(1), new Email('alice@test.com'), 'Alice');
        $this->repo->save($user);

        $found = $this->repo->findByEmail(new Email('alice@test.com'));

        $this->assertNotNull($found);
        $this->assertSame('Alice', $found->name());
        $this->assertSame('alice@test.com', $found->email()->toString());
    }

    #[Test]
    public function it_soft_deletes_user(): void
    {
        $user = User::register(new UserId(2), new Email('bob@test.com'), 'Bob');
        $this->repo->save($user);
        $this->repo->delete(new UserId(2));

        $found = $this->repo->findById(new UserId(2));
        $this->assertNull($found, 'Soft-deleted user should not be found.');
    }

    #[Test]
    public function exists_returns_false_for_deleted(): void
    {
        $user = User::register(new UserId(3), new Email('carol@test.com'), 'Carol');
        $this->repo->save($user);
        $this->assertTrue($this->repo->exists(new UserId(3)));
        $this->repo->delete(new UserId(3));
        $this->assertFalse($this->repo->exists(new UserId(3)));
    }
}
```

### 25.4 API / HTTP Tests

```php
<?php
declare(strict_types=1);
namespace Tests\Api;

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

final class UserApiTest extends TestCase
{
    private Application $app;

    protected function setUp(): void
    {
        $this->app = Application::createForTesting(); // uses InMemory repositories
    }

    #[Test]
    public function get_users_returns_empty_list(): void
    {
        $response = $this->get('/api/v1/users');

        $this->assertSame(200, $response->status());
        $body = $this->decodeJson($response);
        $this->assertArrayHasKey('data', $body);
        $this->assertArrayHasKey('meta', $body);
        $this->assertSame(0, $body['meta']['total']);
    }

    #[Test]
    public function create_user_returns_201(): void
    {
        $response = $this->postJson('/api/v1/users', [
            'email'    => 'new@example.com',
            'name'     => 'New User',
            'password' => 'secret123',
        ]);

        $this->assertSame(201, $response->status());
        $body = $this->decodeJson($response);
        $this->assertSame('new@example.com', $body['data']['email']);
        $this->assertSame('New User', $body['data']['name']);
    }

    #[Test]
    public function create_user_validates_required_fields(): void
    {
        $response = $this->postJson('/api/v1/users', ['email' => 'bad-email']);

        $this->assertSame(422, $response->status());
        $body = $this->decodeJson($response);
        $this->assertArrayHasKey('errors', $body);
        $this->assertArrayHasKey('email', $body['errors']);
        $this->assertArrayHasKey('name', $body['errors']);
        $this->assertArrayHasKey('password', $body['errors']);
    }

    #[Test]
    public function create_user_rejects_duplicate_email(): void
    {
        $this->postJson('/api/v1/users', ['email'=>'dup@test.com','name'=>'A','password'=>'secret123']);
        $response = $this->postJson('/api/v1/users', ['email'=>'dup@test.com','name'=>'B','password'=>'secret123']);

        $this->assertSame(409, $response->status());
    }

    #[Test]
    public function get_user_returns_404_for_nonexistent(): void
    {
        $response = $this->get('/api/v1/users/99999');
        $this->assertSame(404, $response->status());
    }

    // Helper methods
    private function get(string $path): Response
    {
        return $this->app->handle(Request::fromArray(['method'=>'GET','path'=>$path]));
    }

    private function postJson(string $path, array $body): Response
    {
        return $this->app->handle(Request::fromArray([
            'method'  => 'POST',
            'path'    => $path,
            'body'    => $body,
            'headers' => ['content-type' => 'application/json'],
        ]));
    }

    private function decodeJson(Response $response): array
    {
        return json_decode($response->body(), true, 512, JSON_THROW_ON_ERROR);
    }
}
```

### 25.5 phpunit.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
         colors="true"
         stopOnFailure="false">

    <testsuites>
        <testsuite name="Unit">        <directory>tests/Unit</directory> </testsuite>
        <testsuite name="Integration"> <directory>tests/Integration</directory> </testsuite>
        <testsuite name="Api">         <directory>tests/Api</directory> </testsuite>
    </testsuites>

    <coverage>
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <report>
            <html outputDirectory=".coverage"/>
            <clover outputFile=".coverage/clover.xml"/>
        </report>
    </coverage>

    <php>
        <env name="APP_ENV"  value="testing"/>
        <env name="APP_DEBUG" value="true"/>
        <env name="DB_DRIVER" value="sqlite"/>
    </php>
</phpunit>
```

---

## 26. PSR STANDARDS — FULL REFERENCE

```
PSR-1  Basic Coding Standard
  - Only <?php or <?= tags
  - UTF-8 without BOM
  - Declare symbols OR produce side effects — not both
  - Namespaces and classes must follow PSR-4
  - Class names: PascalCase
  - Constants: UPPER_CASE
  - Methods: camelCase

PSR-2/PSR-12  Extended Coding Style (PSR-12 supersedes PSR-2)
  - 4 spaces, no tabs
  - Opening brace for class/function on next line
  - Opening brace for control structures on same line
  - One blank line before return in a method body is optional
  - Visibility required on all methods/properties
  - abstract/final before visibility; static after visibility
  - No trailing whitespace; one blank line at end of file

PSR-4  Autoloading
  - Vendor\Package\Sub\ClassName → /vendor_dir/Package/Sub/ClassName.php
  - Fully Qualified Class Name maps directly to file path

PSR-3  Logger Interface
  - emergency/alert/critical/error/warning/notice/info/debug
  - log(level, message, context)
  - {placeholder} substitution from context

PSR-7  HTTP Message Interfaces (if building framework-compatible layer)
  - ServerRequestInterface, ResponseInterface, StreamInterface, etc.
  - All messages are immutable — use withX() methods

PSR-11  Container Interface
  - get(string $id): mixed
  - has(string $id): bool

PSR-14  Event Dispatcher
  - EventDispatcherInterface::dispatch(object $event): object
  - ListenerProviderInterface::getListenersForEvent(object $event): iterable

PSR-15  HTTP Server Request Handlers
  - RequestHandlerInterface::handle(ServerRequestInterface $request): ResponseInterface
  - MiddlewareInterface::process(request, handler): ResponseInterface

PSR-16  Simple Cache
  - get/set/delete/clear/getMultiple/setMultiple/deleteMultiple/has
```

---

## 27. PERFORMANCE OPTIMIZATION

### 27.1 OPcache Configuration

```ini
opcache.enable                  = 1
opcache.jit                     = 1255    ; PHP 8.0+ JIT
opcache.jit_buffer_size         = 128M
opcache.memory_consumption      = 256
opcache.interned_strings_buffer = 16
opcache.max_accelerated_files   = 20000
opcache.validate_timestamps     = 0       ; production: never revalidate
opcache.revalidate_freq         = 0
opcache.save_comments           = 1
```

### 27.2 Memory-Efficient Processing

```php
<?php
declare(strict_types=1);

// Generator — process millions of rows without loading into memory
function streamUsers(\PDO $pdo): \Generator
{
    $stmt = $pdo->query('SELECT * FROM users ORDER BY id');
    while ($row = $stmt->fetch()) {
        yield $row;
    }
}

foreach (streamUsers($pdo) as $row) {
    processUser($row); // only one row in memory at a time
}

// Chunked processing
function processInChunks(\PDO $pdo, callable $fn, int $chunk = 500): void
{
    $offset = 0;
    do {
        $stmt = $pdo->prepare('SELECT * FROM users LIMIT :l OFFSET :o');
        $stmt->bindValue(':l', $chunk,  \PDO::PARAM_INT);
        $stmt->bindValue(':o', $offset, \PDO::PARAM_INT);
        $stmt->execute();
        $rows = $stmt->fetchAll();
        if (empty($rows)) break;
        $fn($rows);
        $offset += $chunk;
        unset($rows);
        gc_collect_cycles();
    } while (true);
}

// Lazy evaluation with first-class callables (PHP 8.1+)
$emailsOfActiveUsers = array_map(
    fn(User $u) => $u->email()->toString(),
    array_filter($users, fn(User $u) => $u->isActive())
);

// Use SplFixedArray for large integer-indexed arrays
$arr = new \SplFixedArray(1_000_000); // ~4× less memory than array

// Use array_column instead of loops
$ids   = array_column($rows, 'id');
$byId  = array_column($rows, null, 'id');  // index by id
```

### 27.3 Database Performance

```php
<?php
declare(strict_types=1);

// NEVER select * in production
// Bad:  SELECT * FROM users
// Good: SELECT id, email, name FROM users

// Always paginate
$stmt = $pdo->prepare('SELECT id, email FROM users LIMIT :l OFFSET :o');

// Use covering indexes (index covers all selected columns)
// CREATE INDEX idx_users_email_name ON users (email, name);

// Avoid N+1 queries — use JOINs
// Bad: foreach ($orders as $order) { $user = findUser($order->user_id); }
// Good: SELECT o.*, u.name FROM orders o JOIN users u ON u.id = o.user_id

// Batch inserts
$values  = implode(',', array_fill(0, count($rows), '(?,?,?)'));
$stmt    = $pdo->prepare("INSERT INTO logs (level, message, created_at) VALUES {$values}");
$flat    = array_merge(...array_map(fn($r) => [$r['level'],$r['msg'],date('Y-m-d H:i:s')], $rows));
$stmt->execute($flat);

// Use EXPLAIN to profile
// EXPLAIN SELECT * FROM orders WHERE user_id = 5 AND status = 'pending';
```

### 27.4 Profiling

```php
<?php
declare(strict_types=1);

// Simple inline profiler
final class Profiler
{
    private array $marks = [];

    public function mark(string $label): void
    {
        $this->marks[$label] = ['time' => hrtime(true), 'mem' => memory_get_usage(true)];
    }

    /** @return array<string, array{time_ms: float, mem_kb: float}> */
    public function report(): array
    {
        $keys   = array_keys($this->marks);
        $result = [];
        for ($i = 1; $i < count($keys); $i++) {
            $from = $this->marks[$keys[$i-1]];
            $to   = $this->marks[$keys[$i]];
            $result["{$keys[$i-1]} → {$keys[$i]}"] = [
                'time_ms' => round(($to['time'] - $from['time']) / 1_000_000, 3),
                'mem_kb'  => round(($to['mem']  - $from['mem'])  / 1024, 2),
            ];
        }
        return $result;
    }
}
```

---

## 28. CLI APPLICATIONS

```php
<?php
declare(strict_types=1);
namespace App\Console;

abstract class Command
{
    abstract public function handle(array $args, array $opts): int;
    abstract public function signature(): string;
    abstract public function description(): string;

    protected function line(string $msg): void  { echo $msg . PHP_EOL; }
    protected function info(string $msg): void  { echo "\033[36m[INFO]\033[0m {$msg}" . PHP_EOL; }
    protected function success(string $msg): void { echo "\033[32m[OK]\033[0m {$msg}" . PHP_EOL; }
    protected function error(string $msg): void { fwrite(STDERR, "\033[31m[ERROR]\033[0m {$msg}" . PHP_EOL); }
    protected function warn(string $msg): void  { echo "\033[33m[WARN]\033[0m {$msg}" . PHP_EOL; }

    protected function ask(string $question): string
    {
        echo $question . ' ';
        return trim((string)fgets(STDIN));
    }

    protected function confirm(string $question): bool
    {
        $answer = strtolower($this->ask($question . ' [y/N]'));
        return in_array($answer, ['y','yes'], true);
    }

    protected function table(array $headers, array $rows): void
    {
        $widths = array_map('strlen', $headers);
        foreach ($rows as $row) {
            foreach (array_values($row) as $i => $cell) {
                $widths[$i] = max($widths[$i] ?? 0, strlen((string)$cell));
            }
        }
        $line = '+' . implode('+', array_map(fn($w) => str_repeat('-', $w+2), $widths)) . '+';
        echo $line . PHP_EOL;
        echo '| ' . implode(' | ', array_map(fn($h,$w) => str_pad($h,$w), $headers,$widths)) . ' |' . PHP_EOL;
        echo $line . PHP_EOL;
        foreach ($rows as $row) {
            echo '| ' . implode(' | ', array_map(fn($v,$w) => str_pad((string)$v,$w), array_values($row),$widths)) . ' |' . PHP_EOL;
        }
        echo $line . PHP_EOL;
    }
}

// Concrete command
final class MigrateCommand extends Command
{
    public function __construct(private readonly MigrationRunner $runner) {}

    public function signature(): string    { return 'db:migrate'; }
    public function description(): string  { return 'Run pending database migrations'; }

    public function handle(array $args, array $opts): int
    {
        $this->info('Running migrations...');
        try {
            $this->runner->migrate();
            $this->success('Migrations completed.');
            return 0;
        } catch (\Throwable $e) {
            $this->error('Migration failed: ' . $e->getMessage());
            return 1;
        }
    }
}

final class UserCreateCommand extends Command
{
    public function __construct(private readonly UserService $service) {}

    public function signature(): string   { return 'user:create'; }
    public function description(): string { return 'Create a new user interactively'; }

    public function handle(array $args, array $opts): int
    {
        $email    = $args[0] ?? $this->ask('Email:');
        $name     = $args[1] ?? $this->ask('Name:');
        $password = $args[2] ?? $this->ask('Password:');

        try {
            $user = $this->service->createUser(new CreateUserDto($email, $name, $password));
            $this->success("User created with ID {$user->id()->value()}");
            return 0;
        } catch (\Throwable $e) {
            $this->error($e->getMessage());
            return 1;
        }
    }
}

// Console Kernel
final class ConsoleKernel
{
    /** @var array<string, Command> */
    private array $commands = [];

    public function register(Command ...$commands): void
    {
        foreach ($commands as $cmd) $this->commands[$cmd->signature()] = $cmd;
    }

    public function run(array $argv): int
    {
        $signature = $argv[1] ?? 'list';

        if ($signature === 'list') { $this->list(); return 0; }

        if (!isset($this->commands[$signature])) {
            fwrite(STDERR, "Unknown command: {$signature}\n");
            return 1;
        }

        $rest = array_slice($argv, 2);
        $opts = $this->parseOptions($rest);
        $args = array_values(array_filter($rest, fn($a) => !str_starts_with($a, '--')));

        return $this->commands[$signature]->handle($args, $opts);
    }

    private function list(): void
    {
        echo "Available commands:\n";
        foreach ($this->commands as $sig => $cmd) {
            echo sprintf("  %-25s %s\n", $sig, $cmd->description());
        }
    }

    private function parseOptions(array $args): array
    {
        $opts = [];
        foreach ($args as $arg) {
            if (!str_starts_with($arg, '--')) continue;
            $parts = explode('=', substr($arg, 2), 2);
            $opts[$parts[0]] = $parts[1] ?? true;
        }
        return $opts;
    }
}

// bin/console.php
// $kernel = new ConsoleKernel();
// $kernel->register(new MigrateCommand($runner), new UserCreateCommand($service));
// exit($kernel->run($argv));
```

---

## 29. PROJECT STRUCTURE

```
project-root/
├── bin/
│   ├── console.php           Entry point for CLI
│   └── worker.php            Queue worker entry point
├── config/
│   ├── app.php               Main config (returns array)
│   ├── database.php
│   ├── container.php         DI container bootstrap
│   └── routes.php            Route definitions
├── public/
│   └── index.php             HTTP entry point (webroot)
├── src/
│   ├── Domain/               Pure business logic — ZERO external dependencies
│   │   ├── User/
│   │   │   ├── User.php
│   │   │   ├── UserId.php
│   │   │   ├── UserStatus.php
│   │   │   └── UserRepositoryInterface.php
│   │   ├── Order/
│   │   │   ├── Order.php
│   │   │   ├── OrderItem.php
│   │   │   ├── OrderStatus.php
│   │   │   └── OrderRepositoryInterface.php
│   │   ├── Event/
│   │   │   ├── DomainEventInterface.php
│   │   │   ├── UserRegisteredEvent.php
│   │   │   └── OrderPlacedEvent.php
│   │   ├── Exception/
│   │   │   ├── AppException.php
│   │   │   ├── NotFoundException.php
│   │   │   ├── ValidationException.php
│   │   │   └── ConflictException.php
│   │   └── ValueObject/
│   │       ├── Email.php
│   │       ├── Money.php
│   │       └── Uuid.php
│   ├── Application/          Use cases, orchestration
│   │   ├── Service/
│   │   │   ├── UserService.php
│   │   │   └── OrderService.php
│   │   ├── Dto/
│   │   │   ├── CreateUserDto.php
│   │   │   ├── UpdateUserDto.php
│   │   │   └── PlaceOrderDto.php
│   │   ├── Command/           (if using CQRS)
│   │   │   ├── CreateUserCommand.php
│   │   │   └── CreateUserHandler.php
│   │   ├── Query/
│   │   │   ├── GetUserQuery.php
│   │   │   └── GetUserHandler.php
│   │   └── Validation/
│   │       ├── Validator.php
│   │       └── Rules/
│   └── Infrastructure/       Concrete implementations
│       ├── Http/
│       │   ├── Controller/
│       │   │   ├── UserController.php
│       │   │   └── AuthController.php
│       │   ├── Middleware/
│       │   │   ├── JwtAuthMiddleware.php
│       │   │   ├── CorsMiddleware.php
│       │   │   └── RateLimitMiddleware.php
│       │   ├── Request.php
│       │   ├── Response.php
│       │   ├── Router.php
│       │   └── ExceptionHandler.php
│       ├── Repository/
│       │   ├── AbstractRepository.php
│       │   ├── PdoUserRepository.php
│       │   └── CachedUserRepository.php
│       ├── Database/
│       │   ├── PdoFactory.php
│       │   ├── TransactionManager.php
│       │   └── Migration/
│       ├── Cache/
│       │   ├── CacheInterface.php
│       │   ├── RedisCache.php
│       │   └── FileCache.php
│       ├── Queue/
│       │   ├── QueueManager.php
│       │   ├── QueueWorker.php
│       │   └── Jobs/
│       ├── Security/
│       │   ├── JwtService.php
│       │   ├── BcryptPasswordHasher.php
│       │   ├── CsrfTokenManager.php
│       │   └── RateLimiter.php
│       ├── Mail/
│       │   ├── Email.php
│       │   ├── MailerInterface.php
│       │   ├── SmtpMailer.php
│       │   └── LoggingMailer.php
│       ├── Logging/
│       │   ├── LoggerInterface.php
│       │   └── FileLogger.php
│       └── Container/
│           └── Container.php
├── tests/
│   ├── Unit/
│   │   ├── Domain/UserTest.php
│   │   └── Application/UserServiceTest.php
│   ├── Integration/
│   │   └── Repository/UserRepositoryTest.php
│   ├── Api/
│   │   └── UserApiTest.php
│   └── bootstrap.php
├── migrations/
│   └── 001_create_users_table.php
├── storage/
│   ├── logs/
│   └── cache/
├── .env
├── .env.example
├── .gitignore
├── composer.json
├── phpunit.xml
├── phpstan.neon
└── .php-cs-fixer.dist.php
```

### 29.1 Entry Points

```php
<?php
// public/index.php
declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use App\Infrastructure\Config\EnvLoader;
use App\Infrastructure\Http\{ExceptionHandler, Request};

EnvLoader::load(__DIR__ . '/../.env');
$config    = require __DIR__ . '/../config/app.php';
$container = (require __DIR__ . '/../config/container.php')($config);
$router    = require __DIR__ . '/../config/routes.php';

$request = Request::fromGlobals();

try {
    $response = $router->dispatch($request, $container);
} catch (\Throwable $e) {
    $response = $container->get(ExceptionHandler::class)->handle($e);
}

$response->withSecurityHeaders()->send();
```

```php
<?php
// bin/worker.php
declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use App\Infrastructure\Config\EnvLoader;
use App\Infrastructure\Queue\QueueWorker;

EnvLoader::load(__DIR__ . '/../.env');
$config    = require __DIR__ . '/../config/app.php';
$container = (require __DIR__ . '/../config/container.php')($config);

/** @var QueueWorker $worker */
$worker = $container->get(QueueWorker::class);
$queue  = $argv[1] ?? 'default';
$worker->work($queue);
```

---

## 30. DEPLOYMENT & INFRASTRUCTURE

### 30.1 Nginx Configuration

```nginx
server {
    listen 80;
    listen 443 ssl http2;
    server_name example.com;
    root /var/www/app/public;
    index index.php;

    # Security
    server_tokens off;
    add_header X-Frame-Options          "DENY"                            always;
    add_header X-Content-Type-Options   "nosniff"                         always;
    add_header Referrer-Policy          "strict-origin-when-cross-origin" always;
    add_header X-XSS-Protection         "0"                               always;

    # Route all requests to index.php
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # PHP-FPM
    location ~ \.php$ {
        fastcgi_pass   unix:/run/php/php8.3-fpm.sock;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include        fastcgi_params;
        fastcgi_read_timeout 30;
        fastcgi_buffer_size  128k;
        fastcgi_buffers      8 128k;
    }

    # Block sensitive files
    location ~ /\.(env|git|htaccess) { deny all; return 404; }
    location ~ ^/(vendor|src|tests|config|storage)/  { deny all; return 404; }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1000;
}
```

### 30.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.9'
services:
  nginx:
    image: nginx:1.25-alpine
    ports: ["80:80", "443:443"]
    volumes:
      - .:/var/www/app:ro
      - ./docker/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on: [php]

  php:
    build: ./docker/php
    volumes: [".:/var/www/app:cached"]
    environment:
      APP_ENV: production
    depends_on: [mysql, redis]

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes: [mysql_data:/var/lib/mysql]
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

  redis:
    image: redis:7-alpine
    volumes: [redis_data:/data]
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

  worker:
    build: ./docker/php
    command: php bin/worker.php default
    depends_on: [mysql, redis]
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:
```

### 30.3 Deploy Script

```bash
#!/usr/bin/env bash
# bin/deploy.sh
set -euo pipefail

APP_DIR="/var/www/app"
BRANCH="${1:-main}"

echo "==> Deploying branch: ${BRANCH}"
cd "$APP_DIR"

echo "==> Pulling code..."
git fetch origin
git reset --hard "origin/${BRANCH}"

echo "==> Installing dependencies..."
composer install --no-dev --optimize-autoloader --no-interaction --quiet

echo "==> Running migrations..."
php bin/console.php db:migrate

echo "==> Clearing caches..."
php bin/console.php cache:clear 2>/dev/null || true

echo "==> Reloading PHP-FPM..."
sudo systemctl reload php8.3-fpm

echo "==> Done at $(date)"
```

---

## 31. MODERN PHP 8.x FEATURES — COMPLETE REFERENCE

### 31.1 PHP 8.0

```php
<?php
declare(strict_types=1);

// Named arguments
function createUser(string $name, string $email, bool $active = true): User {}
$user = createUser(email: 'a@b.com', name: 'Alice'); // order doesn't matter

// Constructor property promotion
class Point {
    public function __construct(
        public readonly float $x,
        public readonly float $y,
        public readonly float $z = 0.0,
    ) {}
}

// Match expression (no fallthrough, exhaustive)
$label = match($status) {
    'active'   => 'Active',
    'inactive' => 'Inactive',
    'banned'   => 'Banned',
    default    => throw new \UnhandledMatchError("Unknown: {$status}"),
};

// Nullsafe operator
$city = $order?->getUser()?->getAddress()?->city;

// Union types
function parseId(int|string $id): int { return (int)$id; }

// throw as expression
$value = $this->cache->get($key) ?? throw new \RuntimeException("Missing: {$key}");

// str_contains / str_starts_with / str_ends_with
str_contains('hello world', 'world');   // true
str_starts_with('https://...', 'https'); // true
str_ends_with('file.php', '.php');       // true

// Attributes
#[\Attribute(\Attribute::TARGET_CLASS | \Attribute::TARGET_METHOD)]
final class Route {
    public function __construct(
        public readonly string $path,
        public readonly string $method = 'GET',
    ) {}
}

class UserController {
    #[Route('/api/users', method: 'GET')]
    public function index(): Response {}
}

// Reading attributes via reflection
$ref   = new \ReflectionClass(UserController::class);
$attrs = $ref->getMethods()[0]->getAttributes(Route::class);
foreach ($attrs as $attr) {
    $route = $attr->newInstance(); // Route instance
}
```

### 31.2 PHP 8.1

```php
<?php
declare(strict_types=1);

// Enums (see Section 5.2 for full coverage)
enum Status: string { case Active = 'active'; }

// Readonly properties
class User {
    public function __construct(
        public readonly int    $id,     // cannot be modified after construction
        public readonly string $email,
    ) {}
}

// Fibers — cooperative multitasking
$fiber = new \Fiber(function (): string {
    $value = \Fiber::suspend('paused');  // suspend, yield 'paused' to caller
    return "got: {$value}";
});

$yielded = $fiber->start();          // 'paused'
$result  = $fiber->resume('hello');  // fiber returns, $result = null
echo $fiber->getReturn();            // 'got: hello'

// Intersection types
function processCollection(Countable&Iterator $col): void {}

// never return type
function redirect(string $url): never { header("Location: {$url}"); exit(); }

// Array unpacking with string keys
$merged = [...['a' => 1], ...['b' => 2]]; // ['a'=>1,'b'=>2]

// new in initializers
class Service {
    public function __construct(
        private readonly Logger $log = new NullLogger(),
    ) {}
}

// First-class callables
$fn  = strlen(...);         // Closure wrapping strlen
$arr = array_map(trim(...), $strings);
```

### 31.3 PHP 8.2

```php
<?php
declare(strict_types=1);

// readonly classes — all properties readonly automatically
readonly class Coordinate {
    public function __construct(
        public float $lat,
        public float $lng,
    ) {}
}

// DNF (Disjunctive Normal Form) types
function process((Countable&Stringable)|null $val): void {}

// Constants in traits
trait HasVersion {
    public const string VERSION = '1.0.0';
}

// Deprecated: dynamic properties on non-stdClass
// Use #[AllowDynamicProperties] to opt in
class Legacy {
    public string $name = 'ok'; // explicit — fine
    // $this->unknownProp = 'bad'; // deprecated → error in 9.0
}

// New functions: array_is_list, ini_parse_quantity, ...
$list = ['a','b','c'];
var_dump(array_is_list($list)); // true
```

### 31.4 PHP 8.3

```php
<?php
declare(strict_types=1);

// Typed class constants
class Config {
    public const string VERSION    = '2.0.0';
    public const int    MAX_RETRY  = 3;
    public const float  TIMEOUT    = 30.5;
    public const bool   DEBUG      = false;
}

// #[Override] attribute — compile-time safety
class ParentClass { public function process(): void {} }
class ChildClass extends ParentClass {
    #[\Override]
    public function process(): void {}  // error if parent method doesn't exist
}

// json_validate() — validate without decoding
if (json_validate($jsonString)) {
    $data = json_decode($jsonString, true);
}

// Readonly properties can be deep-cloned in PHP 8.3
$clone = clone $object; // readonly props can be re-initialized in __clone

// Dynamic class constant fetch
$class = 'App\Domain\User\UserStatus';
$const = 'Active';
$value = constant("{$class}::{$const}");
```

### 31.5 PHP 8.4

```php
<?php
declare(strict_types=1);

// Property Hooks — get/set with custom logic
class User {
    public string $email {
        get => $this->email;
        set(string $value) {
            if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
                throw new \ValueError("Invalid email: {$value}");
            }
            $this->email = strtolower($value);
        }
    }
    // Computed property (no backing storage)
    public string $displayName {
        get => ucfirst($this->name) . ' <' . $this->email . '>';
    }
}

// Asymmetric Visibility
class Order {
    public private(set) int    $id;      // public read, private write
    public protected(set) string $status; // public read, protected write
}

// new without parentheses for chaining
$result = new Request()->withMethod('GET')->withPath('/api');

// Array functions
$users = [/* User objects */];
$first  = array_find($users, fn(User $u) => $u->isAdmin());       // first match or null
$key    = array_find_key($users, fn(User $u) => $u->isAdmin());   // key of first match
$hasAny = array_any($users, fn(User $u) => $u->isAdmin());        // bool
$allOk  = array_all($users, fn(User $u) => $u->isActive());       // bool

// #[Deprecated] attribute
class OldApi {
    #[\Deprecated('Use newMethod() instead', since: '2.0')]
    public function oldMethod(): void {}
}
```

---

## 32. ADVANCED PATTERNS

### 32.1 CQRS — Command Query Responsibility Segregation

```php
<?php
declare(strict_types=1);
namespace App\Application;

// COMMANDS — write side (change state, no return value or return created ID)
interface CommandInterface {}
interface CommandHandlerInterface { public function handle(CommandInterface $cmd): mixed; }

final class PlaceOrderCommand implements CommandInterface {
    public function __construct(
        public readonly int   $userId,
        public readonly array $items, // [{product_id, quantity, price}]
    ) {}
}

final class PlaceOrderHandler implements CommandHandlerInterface {
    public function __construct(
        private readonly OrderRepositoryInterface $orders,
        private readonly EventDispatcher          $dispatcher,
    ) {}

    public function handle(CommandInterface $cmd): string // returns order ID
    {
        assert($cmd instanceof PlaceOrderCommand);
        $items = array_map(fn($i) => OrderItem::create($i['product_id'],$i['quantity'],new Money($i['price'],'USD')), $cmd->items);
        $order = Order::place(new OrderId(uniqid()), new UserId($cmd->userId), $items);
        $this->orders->save($order);
        $this->dispatcher->dispatchAll($order->pullEvents());
        return $order->id()->toString();
    }
}

// QUERIES — read side (no state change, return DTOs)
interface QueryInterface {}
interface QueryHandlerInterface { public function handle(QueryInterface $query): mixed; }

final class GetOrderSummaryQuery implements QueryInterface {
    public function __construct(public readonly string $orderId) {}
}

final class OrderSummaryDto {
    public function __construct(
        public readonly string $id,
        public readonly string $status,
        public readonly string $total,
        public readonly int    $itemCount,
        public readonly string $createdAt,
    ) {}
}

final class GetOrderSummaryHandler implements QueryHandlerInterface {
    public function __construct(private readonly \PDO $pdo) {}

    public function handle(QueryInterface $query): ?OrderSummaryDto
    {
        assert($query instanceof GetOrderSummaryQuery);
        // Query handlers read directly from DB — no domain objects needed
        $row = $this->pdo->prepare(
            'SELECT o.id, o.status, o.total, COUNT(i.id) AS item_count, o.created_at
             FROM orders o LEFT JOIN order_items i ON i.order_id=o.id
             WHERE o.id=:id GROUP BY o.id'
        );
        $row->execute(['id' => $query->orderId]);
        $data = $row->fetch();
        if (!$data) return null;

        return new OrderSummaryDto(
            id:        $data['id'],
            status:    $data['status'],
            total:     $data['total'],
            itemCount: (int)$data['item_count'],
            createdAt: $data['created_at'],
        );
    }
}

// Buses
final class CommandBus {
    /** @var array<class-string, CommandHandlerInterface> */
    private array $map = [];
    public function register(string $cmd, CommandHandlerInterface $h): void { $this->map[$cmd]=$h; }
    public function dispatch(CommandInterface $cmd): mixed {
        $c=$cmd::class;
        if (!isset($this->map[$c])) throw new \RuntimeException("No handler: {$c}");
        return $this->map[$c]->handle($cmd);
    }
}

final class QueryBus {
    /** @var array<class-string, QueryHandlerInterface> */
    private array $map = [];
    public function register(string $q, QueryHandlerInterface $h): void { $this->map[$q]=$h; }
    public function ask(QueryInterface $q): mixed {
        $c=$q::class;
        if (!isset($this->map[$c])) throw new \RuntimeException("No handler: {$c}");
        return $this->map[$c]->handle($q);
    }
}
```

### 32.2 Hexagonal Architecture (Ports and Adapters)

```
                         ┌─────────────────────────────┐
   HTTP  ──► Adapter ──► │                             │ ◄── Adapter ◄── CLI
   Queue ──► Adapter ──► │    Application Core         │ ◄── Adapter ◄── Tests
                         │  (Domain + Use Cases)       │
   MySQL ◄── Adapter ◄── │                             │ ──► Adapter ──► Console
   Redis ◄── Adapter ◄── │                             │ ──► Adapter ──► Mailer
                         └─────────────────────────────┘

Ports (interfaces in Application/Domain):
  - UserRepositoryInterface  (driven port)
  - MailerInterface          (driven port)
  - HttpRequestPort          (driving port)
  - CliCommandPort           (driving port)

Adapters (implementations in Infrastructure):
  - PdoUserRepository  implements UserRepositoryInterface
  - SmtpMailer         implements MailerInterface
  - HttpController     uses HttpRequestPort
  - ConsoleCommand     uses CliCommandPort
```

### 32.3 Circuit Breaker Pattern

```php
<?php
declare(strict_types=1);

final class CircuitBreaker
{
    private int $failures    = 0;
    private int $lastFailure = 0;
    private bool $open       = false;

    public function __construct(
        private readonly int $threshold  = 5,
        private readonly int $timeout    = 60, // seconds before trying again
    ) {}

    public function call(callable $fn): mixed
    {
        if ($this->isOpen()) {
            throw new \RuntimeException('Circuit breaker is OPEN — service unavailable.');
        }

        try {
            $result       = $fn();
            $this->failures = 0;
            $this->open   = false;
            return $result;
        } catch (\Throwable $e) {
            $this->failures++;
            $this->lastFailure = time();

            if ($this->failures >= $this->threshold) {
                $this->open = true;
            }

            throw $e;
        }
    }

    public function isOpen(): bool
    {
        if (!$this->open) return false;

        // Half-open: allow one attempt after timeout
        if (time() - $this->lastFailure > $this->timeout) {
            $this->open = false;
            return false;
        }

        return true;
    }

    public function state(): string
    {
        if (!$this->open) return 'CLOSED';
        if (time() - $this->lastFailure > $this->timeout) return 'HALF-OPEN';
        return 'OPEN';
    }
}

// Usage
$breaker = new CircuitBreaker(threshold: 5, timeout: 60);

try {
    $result = $breaker->call(fn() => $externalApi->fetchData($id));
} catch (\RuntimeException $e) {
    // Fallback: return cached data
    $result = $cache->get("api:{$id}");
}
```

### 32.4 Retry Pattern

```php
<?php
declare(strict_types=1);

final class RetryPolicy
{
    public function __construct(
        private readonly int   $maxAttempts  = 3,
        private readonly int   $baseDelayMs  = 100,
        private readonly float $backoff       = 2.0,
        /** @var list<class-string<\Throwable>> */
        private readonly array $retryOn      = [\RuntimeException::class],
    ) {}

    public function execute(callable $fn): mixed
    {
        $attempt = 0;

        while (true) {
            $attempt++;
            try {
                return $fn();
            } catch (\Throwable $e) {
                if ($attempt >= $this->maxAttempts || !$this->shouldRetry($e)) {
                    throw $e;
                }
                $delay = (int)($this->baseDelayMs * ($this->backoff ** ($attempt - 1)));
                usleep($delay * 1000);
            }
        }
    }

    private function shouldRetry(\Throwable $e): bool
    {
        foreach ($this->retryOn as $class) {
            if ($e instanceof $class) return true;
        }
        return false;
    }
}

// Usage
$retry  = new RetryPolicy(maxAttempts: 3, baseDelayMs: 200, backoff: 2.0);
$result = $retry->execute(fn() => $externalService->call($payload));
```

---

## 33. INTERNATIONALIZATION & LOCALIZATION

```php
<?php
declare(strict_types=1);
namespace App\Infrastructure\I18n;

interface TranslatorInterface
{
    /** @param array<string, string|int|float> $params */
    public function translate(string $key, array $params = [], string $locale = ''): string;
    public function setLocale(string $locale): void;
    public function locale(): string;
}

final class FileTranslator implements TranslatorInterface
{
    private string $currentLocale;
    /** @var array<string, array<string, string>> */
    private array $messages = [];

    public function __construct(
        private readonly string $dir,
        string                  $defaultLocale = 'en',
    ) {
        $this->currentLocale = $defaultLocale;
    }

    public function translate(string $key, array $params = [], string $locale = ''): string
    {
        $locale = $locale ?: $this->currentLocale;
        $this->load($locale);

        $message = $this->messages[$locale][$key]
            ?? $this->messages['en'][$key]
            ?? $key;

        foreach ($params as $placeholder => $value) {
            $message = str_replace(":{$placeholder}", (string)$value, $message);
        }

        return $message;
    }

    public function setLocale(string $locale): void { $this->currentLocale = $locale; }
    public function locale(): string               { return $this->currentLocale; }

    private function load(string $locale): void
    {
        if (isset($this->messages[$locale])) return;
        $file = "{$this->dir}/{$locale}.php";
        $this->messages[$locale] = file_exists($file) ? require $file : [];
    }
}

// lang/en.php
return [
    'auth.invalid_credentials'  => 'Invalid email or password.',
    'auth.account_inactive'     => 'Your account is not active.',
    'user.created'              => 'User :name was created successfully.',
    'order.placed'              => 'Order #:id has been placed. Total: :total',
    'validation.required'       => 'The :field field is required.',
    'validation.email'          => 'The :field must be a valid email address.',
    'validation.min_length'     => 'The :field must be at least :min characters.',
];

// lang/de.php
return [
    'auth.invalid_credentials'  => 'Ungültige E-Mail oder Passwort.',
    'user.created'              => 'Benutzer :name wurde erfolgreich erstellt.',
];

// Usage
$t = new FileTranslator(__DIR__ . '/lang', 'en');
$t->setLocale('de');
echo $t->translate('user.created', ['name' => 'Alice']); // Benutzer Alice wurde...
echo $t->translate('auth.invalid_credentials');           // Ungültige E-Mail...
```

---

## 34. QUALITY GATES & CHECKLISTS

### 34.1 Pre-Commit Checklist

```
STRICT TYPING
 [ ] declare(strict_types=1) in EVERY file
 [ ] All method parameters have type declarations
 [ ] All return types declared (never use implicit void)
 [ ] readonly wherever mutation is not needed
 [ ] Enum instead of string/int constants for closed sets

SECURITY
 [ ] All SQL uses prepared statements with named params
 [ ] Passwords hashed with password_hash() bcrypt cost >= 12
 [ ] All HTML output escaped with htmlspecialchars()
 [ ] File uploads validated by MIME type (not extension)
 [ ] No @ error suppression anywhere
 [ ] No eval(), system(), exec() in application code
 [ ] Rate limiting on auth endpoints

ARCHITECTURE
 [ ] Each class has exactly one responsibility
 [ ] All dependencies injected via constructor
 [ ] Classes depend on interfaces, not concrete implementations
 [ ] final on all concrete classes unless designed for extension
 [ ] Value Objects for domain data with validation
 [ ] No global state ($GLOBALS, static mutable properties)
 [ ] No die()/exit() inside business logic

ERROR HANDLING
 [ ] Typed exception hierarchy (NotFoundException, ConflictException, etc.)
 [ ] Global exception handler catches all Throwable
 [ ] No empty catch blocks — always handle or rethrow
 [ ] Logging at appropriate levels (warning for 4xx, error for 5xx)

TESTING
 [ ] Unit test for every domain entity method
 [ ] Mock objects via interfaces — tests are isolated
 [ ] Integration test for each repository
 [ ] PHPStan at level max — zero errors
 [ ] Code coverage > 80% for domain layer

CODE STYLE
 [ ] php-cs-fixer passes — zero diff
 [ ] No commented-out code committed
 [ ] No debugging output (var_dump, print_r, dd)
 [ ] Methods named with verb+noun (createUser, findById)
 [ ] Constants in UPPER_SNAKE_CASE

PERFORMANCE
 [ ] OPcache enabled in production
 [ ] No SELECT * queries
 [ ] All list endpoints paginated
 [ ] Indexes on foreign keys and frequently queried columns
 [ ] No N+1 query patterns
```

### 34.2 Code Review Standards

```php
<?php
declare(strict_types=1);

// These patterns should be REJECTED in code review:

// 1. Missing declare strict_types
// (file without declare(strict_types=1))

// 2. Untyped parameters or return types
function process($data) { return $data; } // rejected

// 3. Direct superglobal access in non-bootstrap code
$name = $_GET['name']; // inside a service/controller method — rejected

// 4. SQL injection risk
$sql = "SELECT * FROM users WHERE id = {$id}"; // rejected

// 5. Swallowed exceptions
try { $this->service->do(); } catch (\Throwable $e) {} // rejected

// 6. God class — too many dependencies
class SomeService {
    public function __construct(
        private readonly A $a, private readonly B $b, private readonly C $c,
        private readonly D $d, private readonly E $e, private readonly F $f,
    ) {} // > 4-5 dependencies signals SRP violation — discuss refactoring
}

// 7. Boolean parameters
function sendEmail(User $u, bool $urgent, bool $queued, bool $html): void {} // rejected

// 8. Returning null on error instead of throwing
public function findOrFail(int $id): ?User { return null; } // if "fail" is the intent, throw

// 9. Business logic in constructor
final class UserService {
    public function __construct(private readonly \PDO $pdo) {
        $this->setupDatabase(); // side effects in constructor — rejected
    }
}
```

---

## 35. GLOSSARY

| Term | Definition |
|---|---|
| **Aggregate Root** | Entry point to an aggregate; all external access goes through it |
| **Bounded Context** | Explicit boundary within which a domain model applies |
| **Circuit Breaker** | Pattern that stops calling a failing service to prevent cascading failures |
| **Command** | Immutable object expressing intent to change state |
| **CQRS** | Command Query Responsibility Segregation — separate read/write models |
| **DTO** | Data Transfer Object — simple immutable carrier of data between layers |
| **DI** | Dependency Injection — providing dependencies from outside a class |
| **DIP** | Dependency Inversion Principle — depend on abstractions |
| **Domain Event** | Immutable record of something that happened in the domain |
| **Entity** | Object with a unique identity tracked across time |
| **Enum** | PHP 8.1 first-class enumeration type |
| **Fiber** | PHP 8.1 cooperative coroutine / lightweight thread |
| **Guard Clause** | Early return/throw at the top of a method to handle edge cases |
| **Hydration** | Reconstructing a domain object from raw data (DB row, array) |
| **ISP** | Interface Segregation Principle — small, focused interfaces |
| **JIT** | Just-In-Time compilation — PHP 8.0 OPcache extension |
| **LSP** | Liskov Substitution Principle — subtypes must honour the base contract |
| **Middleware** | Handler in a processing pipeline that can inspect/modify request/response |
| **Never** | PHP return type for functions that never return (always throw or exit) |
| **OCP** | Open/Closed Principle — open for extension, closed for modification |
| **Primitive Obsession** | Anti-pattern of using raw scalars instead of Value Objects |
| **PSR** | PHP Standard Recommendation — community coding standards |
| **Query** | Read-only request that returns data without changing state |
| **Readonly** | PHP 8.1 property modifier preventing post-construction mutation |
| **Repository** | Abstraction layer between domain and data storage |
| **Result Type** | Type that represents either success (Ok) or failure (Fail) |
| **Service** | Stateless class containing domain logic not belonging to a single entity |
| **SOLID** | 5 OOP design principles: SRP, OCP, LSP, ISP, DIP |
| **SRP** | Single Responsibility Principle — one reason to change |
| **Union Type** | PHP 8.0 type declaration accepting multiple types: `int\|string` |
| **Use Case** | Application-layer class orchestrating domain logic for a single operation |
| **Value Object** | Immutable object whose equality is based on its value, not identity |
| **Void** | Return type for functions that return nothing |

---

*PHP 8.1–8.4 Canonical Reference · Edition 2025*
*Follow these standards as absolute defaults. Every deviation requires an explicit justification in code comments.*
