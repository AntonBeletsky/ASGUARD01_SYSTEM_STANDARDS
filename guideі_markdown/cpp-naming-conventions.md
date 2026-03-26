# C / C++ Naming Conventions — The Complete Guide

> Covers ISO C++, Allman brace style, Google C++ Style Guide, LLVM, Microsoft, Qt, and modern C++17/20/23 standards.

---

## Table of Contents

1. [General Principles](#1-general-principles)
2. [Brace Style — Allman](#2-brace-style--allman)
3. [Variables](#3-variables)
4. [Constants & `constexpr`](#4-constants--constexpr)
5. [Functions](#5-functions)
6. [Classes & Structs](#6-classes--structs)
7. [Abstract Classes & Interfaces](#7-abstract-classes--interfaces)
8. [Methods](#8-methods)
9. [Properties & Fields](#9-properties--fields)
10. [Private / Protected Members](#10-private--protected-members)
11. [Parameters](#11-parameters)
12. [Namespaces](#12-namespaces)
13. [Templates & Concepts](#13-templates--concepts)
14. [Enums](#14-enums)
15. [Macros & Preprocessor](#15-macros--preprocessor)
16. [Type Aliases & `typedef`](#16-type-aliases--typedef)
17. [Pointers & References](#17-pointers--references)
18. [Boolean Variables](#18-boolean-variables)
19. [Exceptions](#19-exceptions)
20. [Files & Directories](#20-files--directories)
21. [Header Guards & `#pragma once`](#21-header-guards--pragma-once)
22. [Operator Overloading](#22-operator-overloading)
23. [C-style Naming (Pure C)](#23-c-style-naming-pure-c)
24. [Style Guide Comparison](#24-style-guide-comparison)
25. [Naming Anti-patterns](#25-naming-anti-patterns)
26. [Quick Reference Cheatsheet](#26-quick-reference-cheatsheet)
27. [References & Further Reading](#27-references--further-reading)

---

## 1. General Principles

- **No single official standard** — C++ has multiple competing style guides. Choose one and enforce it with tooling (clang-format, clang-tidy).
- **This guide uses the most widely adopted "canonical" C++ style** — a blend of ISO C++ Core Guidelines + common industry practice with Allman braces.
- **Be descriptive.** `user_account_list` beats `ul` or `data`.
- **Be consistent.** The worst convention is an inconsistent one.
- **Avoid abbreviations** unless universally known (`url`, `id`, `http`, `ptr`, `idx`, `buf`).
- **Don't encode the type in the name** (no Hungarian notation): `pUser` → `user`, `nCount` → `count`.
- **Exception:** `p_` or `ptr_` for raw pointers is still seen in some embedded/systems codebases — avoid in modern C++.

---

## 2. Brace Style — Allman

Opening brace goes on its **own line**, at the same indentation level as the statement. This is the **Allman** (BSD) style — used in ISO C++ standard library docs, LLVM, many game studios, and embedded systems.

```cpp
// ✅ Allman style — braces on their own line
class UserService
{
public:
    UserService();
    ~UserService();

    User GetUserById(int user_id);
};

void UserService::DoSomething()
{
    if (condition)
    {
        DoWork();
    }
    else
    {
        DoOtherWork();
    }

    for (int i = 0; i < count; ++i)
    {
        Process(i);
    }

    while (is_running)
    {
        Update();
    }

    switch (state)
    {
        case State::Active:
            HandleActive();
            break;
        case State::Idle:
            HandleIdle();
            break;
        default:
            break;
    }
}
```

### Single-line bodies — still use braces (safer)

```cpp
// ✅ Always use braces, even for single statements
if (user == nullptr)
{
    return;
}

// ❌ Dangerous — easy to break when adding lines
if (user == nullptr)
    return;
```

### Initializer lists & lambdas — inline braces acceptable

```cpp
// ✅ Initializer list — inline acceptable
std::vector<int> numbers = {1, 2, 3, 4, 5};
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}};

// ✅ Short lambda — inline
auto square = [](int x) { return x * x; };

// ✅ Multi-line lambda — Allman
auto process = [this](const User& user)
{
    Validate(user);
    Save(user);
};
```

### Class / struct definition braces

```cpp
// ✅ Allman — opening brace on new line
class User
{
public:
    User(int id, std::string name);
    ~User() = default;

    int GetId() const;
    const std::string& GetName() const;

private:
    int id_;
    std::string name_;
};

struct Point
{
    float x = 0.0f;
    float y = 0.0f;
};
```

### Namespace braces — inline or Allman (both common)

```cpp
// ✅ Inline namespace braces (common — reduces nesting)
namespace MyApp {

class UserService
{
    // ...
};

} // namespace MyApp


// ✅ Allman for namespaces (consistent but verbose)
namespace MyApp
{

class UserService
{
    // ...
};

} // namespace MyApp
```

---

## 3. Variables

Two dominant conventions — **choose one project-wide**:

### Option A — `snake_case` (ISO C++ Core Guidelines, LLVM, Google)

```cpp
// ✅ snake_case — most common in modern open-source C++
int user_count = 0;
std::string first_name = "Alice";
bool is_active = true;
float order_total = 99.95f;
std::vector<User> fetched_users;
```

### Option B — `camelCase` (Microsoft, some game studios, Qt)

```cpp
// ✅ camelCase — common in Windows/game/Qt codebases
int userCount = 0;
std::string firstName = "Alice";
bool isActive = true;
float orderTotal = 99.95f;
std::vector<User> fetchedUsers;
```

### Naming patterns by type

| Data | snake_case | camelCase |
|------|-----------|-----------|
| Integer | `item_count`, `page_index` | `itemCount`, `pageIndex` |
| Float/Double | `total_price`, `tax_rate` | `totalPrice`, `taxRate` |
| String | `first_name`, `page_title` | `firstName`, `pageTitle` |
| Vector/Array | `users`, `order_items` (plural) | `users`, `orderItems` |
| Map | `user_by_id`, `score_map` | `userById`, `scoreMap` |
| Pointer | `raw_ptr`, `node_ptr` | `rawPtr`, `nodePtr` |
| Smart pointer | `user_ptr`, `session` | `userPtr`, `session` |
| Iterator | `it`, `user_it`, `begin` | `it`, `userIt` |
| Index | `idx`, `user_idx`, `i` | `idx`, `userIdx`, `i` |

---

## 4. Constants & `constexpr`

Use **`kPascalCase`** (Google style) or **`SCREAMING_SNAKE_CASE`** (C tradition):

```cpp
// ✅ Google style — kPascalCase for constants
constexpr int kMaxRetryCount = 3;
constexpr double kPi = 3.14159265358979;
constexpr std::size_t kDefaultBufferSize = 1024;

// ✅ Traditional C++ — SCREAMING_SNAKE_CASE
constexpr int MAX_RETRY_COUNT = 3;
constexpr double PI = 3.14159265358979;
const std::string DEFAULT_LOCALE = "en_US";

// ✅ Class-level constants — same rules
class HttpClient
{
public:
    static constexpr int kDefaultTimeoutMs = 5000;
    static constexpr std::size_t kMaxConnections = 100;

private:
    static constexpr const char* kUserAgent = "MyApp/1.0";
};

// ❌ Bad
const int maxRetryCount = 3;    // looks like a variable
const int max_retry_count = 3;  // same — no visual distinction
```

---

## 5. Functions

### `snake_case` (LLVM, Google, modern C++)

```cpp
// ✅ snake_case
User get_user_by_id(int user_id);
float calculate_total_price(const std::vector<CartItem>& items);
std::string format_date(const std::chrono::system_clock::time_point& date);
bool is_email_valid(const std::string& email);
void send_notification(const User& user, const std::string& message);
```

### `PascalCase` (Microsoft, MSVC, Qt, game engines like Unreal)

```cpp
// ✅ PascalCase — Microsoft / Unreal Engine style
User GetUserById(int UserId);
float CalculateTotalPrice(const std::vector<CartItem>& Items);
bool IsEmailValid(const std::string& Email);
void SendNotification(const User& User, const std::string& Message);
```

> **Pick one and be consistent.** For new projects without framework constraints, `snake_case` aligns with the C++ standard library (`std::find`, `std::sort`, `std::make_shared`).

### Common verb prefixes

| Prefix | Use case | Example |
|--------|----------|---------|
| `get_` / `Get` | Returns a value | `get_user_by_id()` |
| `set_` / `Set` | Sets a value | `set_user_name()` |
| `find_` / `Find` | Search, may return null/empty | `find_by_email()` |
| `fetch_` / `Fetch` | External / async retrieval | `fetch_from_api()` |
| `create_` / `Create` | Factory / allocation | `create_session()` |
| `make_` / `Make` | Same as create | `make_request()` |
| `build_` / `Build` | Builder pattern | `build_query()` |
| `update_` / `Update` | Partial update | `update_profile()` |
| `delete_` / `Delete` | Deletion | `delete_user()` |
| `remove_` / `Remove` | Remove from collection | `remove_item()` |
| `clear_` / `Clear` | Empty collection | `clear_cache()` |
| `init_` / `Init` / `Initialize` | Setup | `init_database()` |
| `reset_` / `Reset` | Restore defaults | `reset_state()` |
| `load_` / `Load` | Load from storage | `load_config()` |
| `save_` / `Save` | Persist | `save_settings()` |
| `send_` / `Send` | Communication | `send_email()` |
| `handle_` / `Handle` | Event handler | `handle_request()` |
| `process_` / `Process` | Multi-step action | `process_payment()` |
| `parse_` / `Parse` | Parse raw data | `parse_response()` |
| `format_` / `Format` | Format for display | `format_currency()` |
| `calculate_` / `Calculate` | Math | `calculate_discount()` |
| `validate_` / `Validate` | Validation | `validate_input()` |
| `serialize_` / `Serialize` | Encoding | `serialize_to_json()` |
| `is_` / `Is` | Boolean predicate | `is_valid()`, `is_active()` |
| `has_` / `Has` | Boolean check | `has_permission()` |
| `can_` / `Can` | Capability check | `can_edit()` |

---

## 6. Classes & Structs

Always **PascalCase** — universal across all C++ style guides:

```cpp
// ✅ Classes — PascalCase
class UserRepository
{
    // ...
};

class ShoppingCart
{
    // ...
};

class AuthenticationService
{
    // ...
};

class HttpClient
{
    // ...
};

// ✅ Structs — PascalCase
// Use struct for plain data (POD / aggregate types)
struct Point
{
    float x = 0.0f;
    float y = 0.0f;
};

struct UserConfig
{
    std::string name;
    std::string email;
    int max_connections = 10;
    bool is_active = true;
};

// ❌ Bad
class userRepository {};     // lowercase
class manage_users {};       // snake_case + verb
class USERREPOSITORY {};     // all caps
```

### Class vs Struct — when to use each

```cpp
// ✅ struct — POD, aggregate, value type, no invariants
struct Vector3
{
    float x, y, z;
};

struct Config
{
    std::string host = "localhost";
    int port = 8080;
    int timeout_ms = 5000;
};

// ✅ class — has invariants, encapsulation, non-trivial methods
class BankAccount
{
public:
    BankAccount(double initial_balance);
    void Deposit(double amount);
    void Withdraw(double amount);
    double GetBalance() const;

private:
    double balance_;
    std::vector<Transaction> transactions_;
};
```

### Naming suffixes by responsibility

| Suffix | Purpose | Example |
|--------|---------|---------|
| `Service` | Business logic | `UserService`, `PaymentService` |
| `Repository` | Data access | `UserRepository` |
| `Manager` | Lifecycle management | `ConnectionManager`, `MemoryManager` |
| `Handler` | Handles request/event | `RequestHandler`, `ErrorHandler` |
| `Controller` | Request orchestration | `UserController` |
| `Factory` | Object creation | `UserFactory`, `WidgetFactory` |
| `Builder` | Fluent construction | `QueryBuilder`, `UriBuilder` |
| `Observer` / `Listener` | Observer pattern | `EventListener`, `FrameObserver` |
| `Visitor` | Visitor pattern | `AstVisitor`, `NodeVisitor` |
| `Adapter` | Adapter pattern | `DatabaseAdapter` |
| `Decorator` | Decorator pattern | `LoggingDecorator` |
| `Command` | Command pattern | `MoveCommand`, `UndoCommand` |
| `Strategy` | Strategy pattern | `SortStrategy`, `CompressionStrategy` |
| `Iterator` | Custom iterator | `TreeIterator` |
| `Exception` / `Error` | Custom exception | `FileNotFoundException` |
| `Config` | Configuration | `DatabaseConfig`, `AppConfig` |
| `Info` | Data holder (read-only) | `SystemInfo`, `BuildInfo` |
| `Context` | Execution context | `RenderContext`, `ExecutionContext` |
| `Task` | Async task | `DownloadTask`, `RenderTask` |

---

## 7. Abstract Classes & Interfaces

C++ has no `interface` keyword. Use pure virtual classes. Two naming conventions:

### Option 1 — `I` prefix (Microsoft, COM, Qt, game engines)

```cpp
// ✅ I prefix — explicit interface signal
class IUserRepository
{
public:
    virtual ~IUserRepository() = default;

    virtual User FindById(int user_id) = 0;
    virtual std::vector<User> FindAll() = 0;
    virtual void Save(const User& user) = 0;
    virtual void Delete(int user_id) = 0;
};

class ILogger
{
public:
    virtual ~ILogger() = default;
    virtual void Log(const std::string& message) = 0;
    virtual void LogError(const std::string& message) = 0;
};
```

### Option 2 — Plain name (ISO Core Guidelines, LLVM, modern style)

```cpp
// ✅ No prefix — treat as a regular abstract class
class UserRepository
{
public:
    virtual ~UserRepository() = default;

    virtual User FindById(int user_id) = 0;
    virtual std::vector<User> FindAll() = 0;
    virtual void Save(const User& user) = 0;
    virtual void Delete(int user_id) = 0;
};

// Concrete implementation
class SqlUserRepository : public UserRepository
{
public:
    User FindById(int user_id) override;
    std::vector<User> FindAll() override;
    void Save(const User& user) override;
    void Delete(int user_id) override;

private:
    SqlConnection connection_;
};
```

### Abstract base classes — `Base` or `Abstract` prefix

```cpp
class BaseRepository
{
public:
    virtual ~BaseRepository() = default;

protected:
    virtual void Connect() = 0;
    virtual void Disconnect() = 0;

    std::string connection_string_;
};

class AbstractSerializer
{
public:
    virtual ~AbstractSerializer() = default;

    virtual std::string Serialize(const std::any& data) = 0;
    virtual std::any Deserialize(const std::string& raw) = 0;

protected:
    virtual void ValidateInput(const std::string& input) = 0;
};
```

---

## 8. Methods

Methods follow the **same convention as functions** (snake_case or PascalCase) — whichever you chose project-wide:

```cpp
// ✅ snake_case methods
class UserService
{
public:
    User get_user_by_id(int user_id) const;
    User create_user(const CreateUserDto& dto);
    void update_user_email(int user_id, const std::string& email);
    void delete_user(int user_id);
    bool is_admin(const User& user) const;
    bool has_permission(const User& user, const std::string& action) const;

private:
    void validate_user_data(const CreateUserDto& dto) const;
    User build_user_from_dto(const CreateUserDto& dto) const;
};


// ✅ PascalCase methods (Microsoft / game engine style)
class UserService
{
public:
    User GetUserById(int UserId) const;
    User CreateUser(const CreateUserDto& Dto);
    void UpdateUserEmail(int UserId, const std::string& Email);
    void DeleteUser(int UserId);
    bool IsAdmin(const User& User) const;
    bool HasPermission(const User& User, const std::string& Action) const;

private:
    void ValidateUserData(const CreateUserDto& Dto) const;
    User BuildUserFromDto(const CreateUserDto& Dto) const;
};
```

### `const` methods — always mark when appropriate

```cpp
class User
{
public:
    int GetId() const { return id_; }                      // ✅ const — doesn't modify
    const std::string& GetName() const { return name_; }   // ✅ const
    void SetName(const std::string& name) { name_ = name; } // non-const — modifies

    bool IsActive() const { return is_active_; }           // ✅ const predicate
};
```

---

## 9. Properties & Fields

Public fields in structs — `snake_case` or `camelCase` (match your variable convention).
Private fields in classes — suffix or prefix with `_` (see Section 10).

```cpp
// ✅ Public struct fields — snake_case
struct UserConfig
{
    std::string first_name;
    std::string last_name;
    std::string email;
    int max_connections = 10;
    bool is_active = true;
};

// ✅ Class with getters/setters
class User
{
public:
    User(int id, std::string name) : id_(id), name_(std::move(name)) {}

    int GetId() const { return id_; }
    const std::string& GetName() const { return name_; }
    void SetName(const std::string& name) { name_ = name; }

    bool IsActive() const { return is_active_; }
    void SetActive(bool active) { is_active_ = active; }

private:
    int id_;
    std::string name_;
    bool is_active_ = true;
};
```

---

## 10. Private / Protected Members

### Trailing underscore `_` (Google, LLVM, ISO Core Guidelines — recommended)

```cpp
class UserService
{
private:
    UserRepository* repository_;      // ✅ trailing underscore
    LoggerInterface* logger_;
    std::string connection_string_;
    int max_retry_count_ = 3;

protected:
    EventDispatcher* dispatcher_;
};
```

### Leading underscore `m_` (Microsoft, game engines, embedded)

```cpp
class UserService
{
private:
    UserRepository* m_repository;     // ✅ m_ prefix (member)
    LoggerInterface* m_logger;
    std::string m_connectionString;
    int m_maxRetryCount = 3;

    static int s_instance_count;      // s_ for static members
};
```

### Leading underscore `_` alone (avoid in public headers)

```cpp
// ⚠️ Legal but reserved in some contexts
// Names starting with _ followed by uppercase OR double __ are RESERVED by the standard
// _Name   — reserved at global scope
// __name  — reserved everywhere

// ❌ Never do this
class Foo
{
    int _value;      // risky at global/namespace scope — avoid
    int __value;     // ALWAYS reserved by the standard — NEVER use
};

// ✅ Safe alternatives
int value_;   // trailing underscore — safe
int m_value;  // m_ prefix — safe
```

### Summary of field naming options

| Style | Private | Static | Used by |
|-------|---------|--------|---------|
| Trailing `_` | `name_` | `count_` | Google, LLVM, ISO |
| `m_` prefix | `m_name` | `s_count` | Microsoft, Qt, Unreal |
| No prefix | `name` | `count` | Some small projects |
| `_` prefix | `_name` | `_count` | Avoid — risky/reserved |

---

## 11. Parameters

Follow the same snake_case / PascalCase convention as your functions:

```cpp
// ✅ snake_case parameters
void CreateUser(const std::string& first_name, const std::string& last_name, UserRole role);
std::vector<Order> FetchOrders(const std::chrono::system_clock::time_point& start_date,
                               const std::chrono::system_clock::time_point& end_date);

// ✅ PascalCase parameters (Unreal Engine style)
void CreateUser(const FString& FirstName, const FString& LastName, EUserRole Role);
```

### Pass-by-value vs pass-by-reference naming

```cpp
// ✅ const reference for "input" — cheap to read, no copy
void Save(const User& user);
void Log(const std::string& message);

// ✅ Non-const reference for "output" / in-out
void FillBuffer(std::vector<uint8_t>& buffer);
bool TryParse(const std::string& input, int& out_value);  // out_ prefix optional but clear

// ✅ Move semantics
void SetName(std::string name);         // value — caller can move into it
void Append(std::vector<User> users);   // value — cheap to move

// ✅ Pointer for optional / nullable
void SetLogger(ILogger* logger);        // nullptr = no logger
```

### Avoid shadowing member names

```cpp
class User
{
public:
    // ❌ Parameter shadows member — confusing
    void SetName(const std::string& name)
    {
        name = name;   // BUG: assigns to itself!
    }

    // ✅ Option 1 — trailing underscore on member (clear distinction)
    void SetName(const std::string& name)
    {
        name_ = name;  // clear
    }

    // ✅ Option 2 — 'new_' prefix on parameter
    void SetName(const std::string& new_name)
    {
        name = new_name;
    }

private:
    std::string name_;
};
```

---

## 12. Namespaces

Use **snake_case** or **PascalCase** (pick one). Keep names short:

```cpp
// ✅ snake_case (common in open-source / LLVM style)
namespace my_app
{
namespace http
{
namespace detail
{
    // ...
} // namespace detail
} // namespace http
} // namespace my_app

// ✅ PascalCase (common in enterprise / game engines)
namespace MyApp
{
namespace Http
{
namespace Detail
{
    // ...
} // namespace Detail
} // namespace Http
} // namespace MyApp

// ✅ Nested namespace (C++17)
namespace MyApp::Http::Detail
{
    // ...
} // namespace MyApp::Http::Detail


// ✅ Anonymous namespace — instead of static for file-local things
namespace
{
    void helper_function()
    {
        // only visible in this translation unit
    }

    constexpr int kLocalConstant = 42;
} // namespace


// ✅ Inline namespace — versioning
namespace MyLib
{
    inline namespace V2
    {
        class Connection { ... };
    } // namespace V2

    namespace V1
    {
        class Connection { ... };
    } // namespace V1
} // namespace MyLib
```

---

## 13. Templates & Concepts

### Template parameters — single letter or descriptive PascalCase

```cpp
// ✅ Simple / universal templates — single uppercase letter
template <typename T>
T Max(T a, T b)
{
    return a > b ? a : b;
}

template <typename T, typename U>
auto Add(T lhs, U rhs) -> decltype(lhs + rhs)
{
    return lhs + rhs;
}

// ✅ Descriptive names for domain-specific templates
template <typename TEntity, typename TId = int>
class Repository
{
public:
    virtual TEntity* FindById(TId id) = 0;
    virtual void Save(const TEntity& entity) = 0;
};

template <typename TKey, typename TValue>
class Cache
{
public:
    void Set(const TKey& key, const TValue& value);
    std::optional<TValue> Get(const TKey& key) const;

private:
    std::unordered_map<TKey, TValue> store_;
};

// ✅ Non-type template parameters — SCREAMING or snake (treat like constants)
template <std::size_t N>
class FixedBuffer { ... };

template <int MaxSize, bool ThreadSafe = false>
class Queue { ... };
```

### Concepts (C++20)

Use **PascalCase** — they describe a type requirement:

```cpp
// ✅ Concept names — PascalCase, describe capability
template <typename T>
concept Printable = requires(T t)
{
    { std::cout << t } -> std::same_as<std::ostream&>;
};

template <typename T>
concept Comparable = requires(T a, T b)
{
    { a < b } -> std::convertible_to<bool>;
    { a == b } -> std::convertible_to<bool>;
};

template <typename T>
concept Hashable = requires(T t)
{
    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;
};

template <typename Container>
concept Iterable = requires(Container c)
{
    { c.begin() } -> std::input_iterator;
    { c.end() } -> std::input_iterator;
};

// ✅ Usage
template <Comparable T>
T Clamp(T value, T min_val, T max_val)
{
    if (value < min_val) return min_val;
    if (max_val < value) return max_val;
    return value;
}
```

---

## 14. Enums

### `enum class` (scoped, preferred in modern C++) — PascalCase

```cpp
// ✅ Enum class — PascalCase name, PascalCase members
enum class UserRole
{
    Admin,
    Editor,
    Viewer,
};

enum class HttpStatus : int
{
    Ok = 200,
    Created = 201,
    BadRequest = 400,
    Unauthorized = 401,
    NotFound = 404,
    InternalServerError = 500,
};

enum class Direction
{
    Up,
    Down,
    Left,
    Right,
};

// ✅ Flags — combine with bitwise ops
enum class Permission : unsigned int
{
    None    = 0,
    Read    = 1 << 0,
    Write   = 1 << 1,
    Execute = 1 << 2,
    All     = Read | Write | Execute,
};

// Usage — scoped, no pollution
UserRole role = UserRole::Admin;
HttpStatus status = HttpStatus::NotFound;

if (status == HttpStatus::Ok)
{
    // ...
}
```

### Old-style `enum` — avoid, but if used, prefix members

```cpp
// ⚠️ Unscoped enum — members pollute the surrounding namespace
// If you must use it, prefix members with the enum name
enum Color
{
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
};

// ❌ Don't do this — name collisions
enum Color
{
    RED,    // conflicts with anything else named RED
    GREEN,
    BLUE,
};
```

---

## 15. Macros & Preprocessor

Use **SCREAMING_SNAKE_CASE** with a project prefix:

```cpp
// ✅ Good — project prefix prevents name collisions
#define MYAPP_MAX_BUFFER_SIZE 4096
#define MYAPP_ASSERT(condition, message) \
    do \
    { \
        if (!(condition)) \
        { \
            throw std::runtime_error(message); \
        } \
    } while (false)

#define MYAPP_DISALLOW_COPY(ClassName) \
    ClassName(const ClassName&) = delete; \
    ClassName& operator=(const ClassName&) = delete

// ❌ Bad — no prefix, easy to collide
#define MAX_SIZE 4096
#define ASSERT(x) ...
#define CHECK(x) ...

// ✅ Prefer constexpr over macros for constants
constexpr std::size_t kMaxBufferSize = 4096;

// ✅ Prefer inline functions over function-like macros
template <typename T>
inline T MyApp_Max(T a, T b)
{
    return a > b ? a : b;
}
```

---

## 16. Type Aliases & `typedef`

Use **PascalCase** with `using` (prefer over `typedef` in modern C++):

```cpp
// ✅ using (C++11+) — preferred
using UserId = int;
using UserList = std::vector<User>;
using UserMap = std::unordered_map<int, User>;
using Callback = std::function<void(const User&)>;
using JsonObject = std::map<std::string, std::any>;
using Byte = std::uint8_t;
using Size = std::size_t;

// ✅ Template aliases
template <typename T>
using Optional = std::optional<T>;

template <typename T>
using SharedPtr = std::shared_ptr<T>;

template <typename TKey, typename TValue>
using HashMap = std::unordered_map<TKey, TValue>;

// ✅ typedef — legacy, avoid in new code
typedef int UserId;               // old style
typedef void (*Callback)(int);    // function pointer typedef


// ❌ Bad
using userId = int;           // camelCase
using USER_ID = int;          // SCREAMING (looks like a macro)
using user_id_t = int;        // _t suffix is reserved in POSIX
```

---

## 17. Pointers & References

Attach `*` and `&` to the **type**, not the variable name:

```cpp
// ✅ Attach to type (C++ style)
int* ptr;
int& ref = value;
const std::string& name = user.GetName();
std::unique_ptr<User> user_ptr = std::make_unique<User>();

// ❌ Attach to variable (C style)
int *ptr;
int &ref = value;


// ✅ Pointer naming — suffix with _ptr for raw pointers (optional but clear)
User* user_ptr = nullptr;
Node* next_ptr = head;

// ✅ Smart pointers — no suffix needed (type system shows ownership)
std::unique_ptr<User> user;                      // owns it
std::shared_ptr<Session> session;                // shared ownership
std::weak_ptr<Observer> observer;                // non-owning reference


// Multiple declarations on one line — DON'T (confusing)
// ❌ Bad
int* a, b;    // b is int, not int*!

// ✅ Good — one per line
int* a;
int b;
```

---

## 18. Boolean Variables

Use **`is_`, `has_`, `can_`, `should_`, `was_`, `did_`** prefixes:

```cpp
// ✅ snake_case boolean names
bool is_loading = false;
bool is_authenticated = false;
bool is_active = true;
bool has_errors = false;
bool has_permission = true;
bool can_edit = false;
bool should_retry = true;
bool was_modified = false;

// ✅ PascalCase boolean names
bool IsLoading = false;
bool IsAuthenticated = false;
bool HasErrors = false;
bool CanEdit = false;

// ✅ In class
class User
{
public:
    bool IsActive() const { return is_active_; }
    bool HasSubscription() const { return has_subscription_; }
    bool CanEdit(const Document& doc) const;

private:
    bool is_active_ = true;
    bool has_subscription_ = false;
    bool is_verified_ = false;
};

// ❌ Bad
bool loading = false;        // ambiguous
bool active = false;         // adjective without prefix
bool errors = false;         // sounds like collection
bool edit_permission = false; // noun phrase
```

---

## 19. Exceptions

Use **PascalCase** with `Exception` suffix or `Error` suffix:

```cpp
#include <stdexcept>

// ✅ Good — Exception suffix
class UserNotFoundException : public std::runtime_error
{
public:
    explicit UserNotFoundException(int user_id)
        : std::runtime_error("User with id=" + std::to_string(user_id) + " not found")
        , user_id_(user_id)
    {}

    int GetUserId() const { return user_id_; }

private:
    int user_id_;
};

class InvalidEmailException : public std::invalid_argument
{
public:
    explicit InvalidEmailException(const std::string& email)
        : std::invalid_argument("Invalid email: " + email)
    {}
};

class PaymentFailedException : public std::runtime_error
{
public:
    explicit PaymentFailedException(const std::string& reason)
        : std::runtime_error("Payment failed: " + reason)
    {}
};

// ✅ Exception hierarchy
class AppException : public std::exception
{
public:
    explicit AppException(std::string message) : message_(std::move(message)) {}
    const char* what() const noexcept override { return message_.c_str(); }

private:
    std::string message_;
};

class DatabaseException : public AppException { ... };
class ConnectionTimeoutException : public DatabaseException { ... };

// ❌ Bad
class UserException : public std::exception {};   // too vague
class bad_user : public std::exception {};        // snake_case
class USER_NOT_FOUND : public std::exception {};  // all caps
```

---

## 20. Files & Directories

### Header files

```
UserService.hpp      ← class declaration (PascalCase = class inside)
UserService.h        ← also acceptable (.h or .hpp — pick one)
http_client.hpp      ← snake_case also common (especially in LLVM/Google style)
```

### Source files

```
UserService.cpp      ← implementation (matches header name)
UserService.cc       ← also acceptable (.cpp or .cc — pick one)
http_client.cpp
```

### Common conventions by style guide

| Style | Headers | Sources |
|-------|---------|---------|
| Google | `snake_case.h` | `snake_case.cc` |
| LLVM | `PascalCase.h` | `PascalCase.cpp` |
| Microsoft | `PascalCase.h` | `PascalCase.cpp` |
| Qt | `lowercase.h` | `lowercase.cpp` |
| Most teams | `PascalCase.hpp` / `PascalCase.h` | `PascalCase.cpp` |

### File structure

```
project/
  include/
    myapp/
      UserService.hpp
      UserRepository.hpp
      models/
        User.hpp
        Order.hpp
  src/
    UserService.cpp
    UserRepository.cpp
    models/
      User.cpp
  tests/
    UserServiceTest.cpp
    UserRepositoryTest.cpp
  CMakeLists.txt
```

### Special files

```
CMakeLists.txt        ← CMake build
Makefile              ← Make build
conanfile.txt         ← Conan package manager
vcpkg.json            ← vcpkg package manager
.clang-format         ← clang-format config
.clang-tidy           ← clang-tidy config
compile_commands.json ← compile database (for IDEs)
```

---

## 21. Header Guards & `#pragma once`

### `#pragma once` (preferred — simpler)

```cpp
// ✅ pragma once — works on all modern compilers
#pragma once

#include <string>
#include <vector>

namespace MyApp
{

class UserService
{
    // ...
};

} // namespace MyApp
```

### Traditional include guards — SCREAMING_SNAKE_CASE with path

```cpp
// ✅ Traditional include guard — format: PROJECT_PATH_TO_FILE_H
#ifndef MYAPP_SERVICES_USER_SERVICE_HPP
#define MYAPP_SERVICES_USER_SERVICE_HPP

// ... content ...

#endif // MYAPP_SERVICES_USER_SERVICE_HPP
```

---

## 22. Operator Overloading

Name follows standard operator syntax — no custom naming needed. Keep semantics intuitive:

```cpp
class Vector2
{
public:
    float x, y;

    // ✅ Arithmetic operators
    Vector2 operator+(const Vector2& rhs) const
    {
        return {x + rhs.x, y + rhs.y};
    }

    Vector2 operator-(const Vector2& rhs) const
    {
        return {x - rhs.x, y - rhs.y};
    }

    Vector2 operator*(float scalar) const
    {
        return {x * scalar, y * scalar};
    }

    Vector2& operator+=(const Vector2& rhs)
    {
        x += rhs.x;
        y += rhs.y;
        return *this;
    }

    // ✅ Comparison operators
    bool operator==(const Vector2& rhs) const
    {
        return x == rhs.x && y == rhs.y;
    }

    bool operator!=(const Vector2& rhs) const
    {
        return !(*this == rhs);
    }

    bool operator<(const Vector2& rhs) const  // for sorting
    {
        return std::tie(x, y) < std::tie(rhs.x, rhs.y);
    }

    // ✅ Stream operator — free function
    friend std::ostream& operator<<(std::ostream& os, const Vector2& v)
    {
        return os << "(" << v.x << ", " << v.y << ")";
    }

    // ✅ Subscript
    float& operator[](int index)
    {
        return index == 0 ? x : y;
    }

    // ✅ Conversion
    explicit operator bool() const
    {
        return x != 0.0f || y != 0.0f;
    }
};
```

---

## 23. C-style Naming (Pure C)

When writing pure C code, all naming uses **snake_case**:

```c
/* Variables */
int user_count = 0;
char* first_name = NULL;
float order_total = 0.0f;

/* Constants */
#define MAX_BUFFER_SIZE 1024
#define PI 3.14159265f

static const int kDefaultTimeout = 30;

/* Functions — module_verb_noun pattern */
int user_create(const char* name, const char* email);
void user_destroy(User* user);
User* user_find_by_id(int id);
bool user_is_active(const User* user);

/* Structs — PascalCase or snake_case (both common in C) */
typedef struct User
{
    int id;
    char first_name[64];
    char last_name[64];
    char email[256];
    bool is_active;
} User;

typedef struct
{
    int x;
    int y;
    int width;
    int height;
} Rect;

/* Enums */
typedef enum
{
    USER_ROLE_ADMIN = 0,
    USER_ROLE_EDITOR,
    USER_ROLE_VIEWER,
} UserRole;

/* File-local functions — static + underscore prefix optional */
static void _validate_email(const char* email);
static bool _is_valid_id(int id);

/* Type suffixes — _t suffix (be careful: POSIX reserves names ending in _t) */
typedef unsigned char byte_t;
typedef int error_code_t;
typedef void (*callback_fn_t)(void* context);
```

---

## 24. Style Guide Comparison

| Construct | Google | LLVM | Microsoft | Unreal Engine | Qt |
|-----------|--------|------|-----------|---------------|-----|
| Variables | `snake_case` | `CamelCase` | `camelCase` | `CamelCase` | `camelCase` |
| Functions | `PascalCase` | `camelCase` | `PascalCase` | `PascalCase` | `camelCase` |
| Classes | `PascalCase` | `PascalCase` | `PascalCase` | `FPascalCase` | `PascalCase` |
| Constants | `kPascalCase` | `kPascalCase` | `ALL_CAPS` | `ALL_CAPS` | `PascalCase` |
| Enums | `enum class PascalCase` | `enum class PascalCase` | `PascalCase` | `EPascalCase` | `PascalCase` |
| Enum members | `kPascalCase` | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` |
| Private fields | `name_` | `Name_` or `name_` | `m_name` | `MemberName` | `m_name` |
| Namespaces | `snake_case` | `llvm` style | `PascalCase` | `N/A (UE uses modules)` | `PascalCase` |
| Macros | `ALL_CAPS` | `ALL_CAPS` | `ALL_CAPS` | `ALL_CAPS` | `ALL_CAPS` |
| Files | `snake_case.cc/.h` | `PascalCase.cpp/.h` | `PascalCase.cpp/.h` | `PascalCase.cpp/.h` | `lowercase.cpp/.h` |
| Braces | K&R / Attach | LLVM / Attach | Allman | Allman | Allman |

> **Unreal Engine** has its own type prefixes:
> `F` — structs/classes (FVector, FString), `U` — UObject subclasses, `A` — AActor subclasses, `E` — enums, `I` — interfaces, `T` — template classes, `G` — global variables.

---

## 25. Naming Anti-patterns

### ❌ Generic / meaningless names

```cpp
// Bad
auto data = GetUsers();
auto result = ProcessOrder(order);
auto temp = CalculateTotal();
auto obj = std::make_unique<UserService>();
auto info = GetUserInfo(user_id);

// Good
auto users = GetUsers();
auto processed_order = ProcessOrder(order);
auto order_total = CalculateTotal();
auto user_service = std::make_unique<UserService>();
auto user_profile = GetUserProfile(user_id);
```

### ❌ Hungarian notation

```cpp
// ❌ Bad — encodes type in name (obsolete)
int nCount = 0;
char* pszName = nullptr;
bool bIsActive = false;
DWORD dwFlags = 0;
IUserRepository* pRepo = nullptr;

// ✅ Good — type system handles it
int count = 0;
char* name = nullptr;
bool is_active = false;
unsigned int flags = 0;
IUserRepository* repo = nullptr;
```

### ❌ Misleading names

```cpp
// Implies list but holds count
int users = 42;               // should be user_count

// Name lies about return type
std::vector<User> GetUser();  // returns many, name says one
User* FindUsers(int id);      // returns one, name says many
```

### ❌ Double underscores (reserved)

```cpp
// ❌ NEVER — reserved by the C++ standard
int __value;
void __init();
class __MyClass {};

// ❌ Also reserved — leading underscore + uppercase at global scope
int _Value;    // at global scope — reserved
```

### ❌ Numeric suffixes

```cpp
// Bad
User* user1 = GetUser(id1);
User* user2 = GetUser(id2);

// Good
User* current_user = GetUser(current_user_id);
User* target_user = GetUser(target_user_id);
```

---

## 26. Quick Reference Cheatsheet

| Construct | Convention | Example |
|-----------|-----------|---------|
| Variable | `snake_case` or `camelCase` | `user_count`, `userCount` |
| Constant / constexpr | `kPascalCase` or `SCREAMING` | `kMaxRetries`, `MAX_RETRIES` |
| Standalone function | `snake_case` or `PascalCase` | `get_user_by_id()`, `GetUserById()` |
| Class | PascalCase | `UserService`, `ShoppingCart` |
| Struct | PascalCase | `Point`, `UserConfig` |
| Abstract class | PascalCase or `I`/`Base` prefix | `IUserRepository`, `BaseRepository` |
| Method | same as function convention | `get_by_id()` / `GetById()` |
| const method | mark with `const` | `int GetId() const;` |
| Private field | trailing `_` or `m_` prefix | `name_`, `m_name` |
| Static member | same + `s_` if desired | `s_instance_count` |
| Parameter | `snake_case` or `CamelCase` | `user_id`, `UserId` |
| Namespace | `snake_case` or `PascalCase` | `my_app`, `MyApp` |
| Template param | `T`, `U` / `PascalCase` | `T`, `TEntity`, `TKey` |
| Concept | PascalCase | `Comparable`, `Printable` |
| Enum (class) | PascalCase + PascalCase members | `UserRole::Admin` |
| Old enum | SCREAMING members with prefix | `USER_ROLE_ADMIN` |
| Macro | `SCREAMING_SNAKE_CASE` with prefix | `MYAPP_MAX_SIZE` |
| Type alias | PascalCase | `UserId`, `Callback` |
| Header guard | `PROJECT_PATH_FILE_HPP` | `MYAPP_SERVICES_USER_HPP` |
| Header files | `PascalCase.hpp` or `snake_case.h` | `UserService.hpp` |
| Source files | matches header | `UserService.cpp` |
| Boolean | `is_/has_/can_` prefix | `is_active_`, `has_errors_` |
| Exception | PascalCase + `Exception` | `UserNotFoundException` |
| Interface (C) | `I` prefix | `ILogger`, `IRenderer` |
| Brace style | Allman (own line) | see Section 2 |
| Pointer decl | `int* ptr` (attach to type) | `User* user_ptr` |

---

## 27. References & Further Reading

| Resource | URL |
|----------|-----|
| **ISO C++ Core Guidelines** | https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines |
| **Google C++ Style Guide** | https://google.github.io/styleguide/cppguide.html |
| **LLVM Coding Standards** | https://llvm.org/docs/CodingStandards.html |
| **Microsoft C++ Coding Conventions** | https://learn.microsoft.com/en-us/cpp/cpp/ |
| **Unreal Engine Coding Standard** | https://dev.epicgames.com/documentation/en-us/unreal-engine/coding-standard |
| **Qt Coding Conventions** | https://wiki.qt.io/Coding_Conventions |
| **C++ Best Practices (Jason Turner)** | https://github.com/cpp-best-practices/cppbestpractices |
| **clang-format** | https://clang.llvm.org/docs/ClangFormat.html |
| **clang-tidy** | https://clang.llvm.org/extra/clang-tidy/ |
| **cppreference.com** | https://en.cppreference.com |

### Recommended `.clang-format` (Allman style)

```yaml
---
BasedOnStyle: LLVM
BreakBeforeBraces: Allman          # ← Allman braces
IndentWidth: 4
TabWidth: 4
UseTab: Never
ColumnLimit: 120
AccessModifierOffset: -4
AlignConsecutiveDeclarations: true
AlignConsecutiveAssignments: true
AlignTrailingComments: true
IncludeBlocks: Regroup
SortIncludes: CaseInsensitive
PointerAlignment: Left             # int* ptr (attach to type)
ReferenceAlignment: Left           # int& ref
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
SpaceBeforeParens: ControlStatements
Cpp11BracedListStyle: true
```

### Recommended `.clang-tidy`

```yaml
Checks: >
  clang-diagnostic-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  readability-identifier-naming,
  readability-*,
  performance-*,
  bugprone-*

CheckOptions:
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.FunctionCase
    value: camelCase                 # or CamelCase — your choice
  - key: readability-identifier-naming.VariableCase
    value: lower_case
  - key: readability-identifier-naming.ConstantCase
    value: CamelCase
  - key: readability-identifier-naming.ConstantPrefix
    value: k
  - key: readability-identifier-naming.PrivateMemberSuffix
    value: _
  - key: readability-identifier-naming.EnumCase
    value: CamelCase
  - key: readability-identifier-naming.EnumConstantCase
    value: CamelCase
```

---

*Last updated: 2026 — Based on C++23, ISO C++ Core Guidelines, clang-format 17+*
