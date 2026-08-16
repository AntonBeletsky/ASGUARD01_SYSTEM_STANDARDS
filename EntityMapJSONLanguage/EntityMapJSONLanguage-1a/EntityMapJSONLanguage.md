# EntityMap JSON Language — Specification v1.0

> **Purpose:** A universal, single-file JSON format for describing the structure of any data model —
> SQL databases, OOP class hierarchies (C++, C#, Python, Java, JS), UML diagrams, APIs — in one
> portable, tool-agnostic schema that an AI or code generator can read and deploy anywhere.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Root Object](#2-root-object)
3. [Meta Block](#3-meta-block)
4. [Entity Object](#4-entity-object)
   - 4.1 [Entity Kinds](#41-entity-kinds)
   - 4.2 [Field Object](#42-field-object)
   - 4.3 [Field Types](#43-field-types)
   - 4.4 [Field Constraints](#44-field-constraints)
   - 4.5 [Method Object (optional)](#45-method-object-optional)
5. [Relation Object](#5-relation-object)
   - 5.1 [Relation Kinds](#51-relation-kinds)
   - 5.2 [Multiplicity](#52-multiplicity)
6. [Comments & Annotations](#6-comments--annotations)
7. [Reserved Keys Summary](#7-reserved-keys-summary)
8. [Full Example](#8-full-example)
9. [AI Generation Guide](#9-ai-generation-guide)

---

## 1. Motivation

Modern systems mix SQL tables, OOP classes, interfaces, enums, and UML artifacts. Each tool
has its own export format. EntityMap JSON is a **lowest-common-denominator interchange layer**:

- One `.json` file describes an entire model.
- No proprietary extensions, no XML, no binary blobs.
- An AI can generate, transform, and deploy it to any target language or DB engine.
- Round-trips cleanly: DB → EntityMap → Python classes → EntityMap → SQL DDL.

---

## 2. Root Object

Every EntityMap document is a single JSON object with the following top-level keys:

```jsonc
{
  "$entitymap": "1.0",              // Required. Format version string.
  "$comment": "Human note here",   // Optional. Free-text comment on the whole map.
  "meta":     { ... },             // Optional. Authorship, project info.
  "entities": [ ... ],             // Required. Array of Entity objects.
  "relations": [ ... ]             // Required (may be empty). Array of Relation objects.
}
```

| Key | Type | Required | Description |
|---|---|---|---|
| `$entitymap` | string | ✅ | Spec version. Always `"1.0"` for this revision. |
| `$comment` | string | ❌ | Top-level human comment, ignored by tooling. |
| `meta` | object | ❌ | Project metadata (see §3). |
| `entities` | array | ✅ | All entity definitions. |
| `relations` | array | ✅ | All inter-entity relations. Empty array `[]` is valid. |

> **Rule:** Every object and array inside the document may carry an optional `"$comment"` key.
> Tooling must silently ignore any key prefixed with `$` except `$entitymap`.

---

## 3. Meta Block

Optional metadata about the model, not about entities.

```jsonc
"meta": {
  "title":       "E-Commerce Domain Model",
  "version":     "2.3.1",
  "author":      "Team Backend",
  "created":     "2025-04-28",
  "modified":    "2025-04-28",
  "description": "Core data model for the shop platform.",
  "tags":        ["ecommerce", "shop", "backend"],
  "$comment":    "Any free text note."
}
```

| Key | Type | Description |
|---|---|---|
| `title` | string | Human-readable model name. |
| `version` | string | SemVer or any version string of the model itself. |
| `author` | string | Author or team. |
| `created` | string | ISO 8601 date. |
| `modified` | string | ISO 8601 date of last change. |
| `description` | string | Longer description. |
| `tags` | string[] | Free labels for search/filter. |

---

## 4. Entity Object

An **entity** is any named container of fields: a DB table, a class, an interface, an enum,
a struct, an abstract class, or a value object.

```jsonc
{
  "id":        "user",                // Required. Unique machine ID (snake_case).
  "name":      "User",               // Required. Display name.
  "kind":      "class",              // Required. Entity kind (see §4.1).
  "comment":   "Registered user.",   // Optional. Human description.
  "namespace": "auth",               // Optional. Package / schema / module name.
  "abstract":  false,                // Optional. true = abstract class/table.
  "fields":    [ ... ],              // Optional. Array of Field objects.
  "methods":   [ ... ],              // Optional. Array of Method objects (OOP only).
  "$comment":  "Internal note."      // Optional. Ignored by tooling.
}
```

### 4.1 Entity Kinds

| `kind` | Maps to (DB) | Maps to (OOP) | Maps to (UML) |
|---|---|---|---|
| `"class"` | Table | Class | Class |
| `"table"` | Table | — | — |
| `"interface"` | View / Protocol | Interface | Interface |
| `"abstract"` | — | Abstract Class | Abstract Class |
| `"struct"` | — | Struct / Record | — |
| `"enum"` | ENUM type | Enum | Enumeration |
| `"value_object"` | Embedded / JSON col | Value Object | — |
| `"mixin"` | — | Mixin / Trait | — |

> When in doubt, use `"class"` for OOP and `"table"` for pure DB models.
> `"enum"` entities carry their values in `fields` as literals without types (see §4.2).

---

### 4.2 Field Object

A **field** belongs to exactly one entity and never exists standalone.

```jsonc
{
  "name":        "email",            // Required. Field name (snake_case or camelCase).
  "type":        "string",           // Required. Data type (see §4.3).
  "length":      255,                // Optional. Max length for string/varchar.
  "precision":   10,                 // Optional. Total digits for decimal.
  "scale":       2,                  // Optional. Digits after decimal point.
  "nullable":    false,              // Optional. Default: false.
  "default":     null,               // Optional. Default value (JSON literal).
  "constraints": ["unique", "index"],// Optional. Array of constraint tags (see §4.4).
  "visibility":  "public",           // Optional. OOP visibility (public/protected/private).
  "static":      false,              // Optional. OOP static flag.
  "readonly":    false,              // Optional. OOP readonly / DB generated.
  "comment":     "User email address, unique per account.",
  "$comment":    "Internal note."
}
```

**Enum literal field** — for `kind: "enum"` entities, omit `type` and use only `name` + `comment`:

```jsonc
{
  "name":    "ACTIVE",
  "comment": "Account is in good standing."
}
```

---

### 4.3 Field Types

#### Primitive Types (always supported everywhere)

| Type token | SQL equivalent | C / C++ | C# | Python | Java | JS/TS |
|---|---|---|---|---|---|---|
| `"bool"` | BOOLEAN | bool | bool | bool | boolean | boolean |
| `"int"` | INTEGER | int | int | int | int | number |
| `"int8"` | TINYINT | int8_t | sbyte | int | byte | number |
| `"int16"` | SMALLINT | int16_t | short | int | short | number |
| `"int32"` | INT | int32_t | int | int | int | number |
| `"int64"` | BIGINT | int64_t | long | int | long | bigint |
| `"uint"` | UNSIGNED INT | unsigned int | uint | int | — | number |
| `"float"` | FLOAT | float | float | float | float | number |
| `"double"` | DOUBLE | double | double | float | double | number |
| `"decimal"` | DECIMAL(p,s) | — | decimal | Decimal | BigDecimal | — |
| `"string"` | VARCHAR(n) | char* | string | str | String | string |
| `"text"` | TEXT / CLOB | — | string | str | String | string |
| `"char"` | CHAR(1) | char | char | str | char | string |
| `"bytes"` | BLOB / BYTEA | uint8_t* | byte[] | bytes | byte[] | Uint8Array |

#### Date & Time Types

| Type token | SQL equivalent | Notes |
|---|---|---|
| `"date"` | DATE | Calendar date only (YYYY-MM-DD). |
| `"time"` | TIME | Time of day only. |
| `"datetime"` | DATETIME | Date + time, no timezone. |
| `"timestamp"` | TIMESTAMP | Date + time with UTC offset. |
| `"duration"` | INTERVAL | ISO 8601 duration. |

#### Identity & Reference Types

| Type token | SQL equivalent | Notes |
|---|---|---|
| `"uuid"` | UUID / CHAR(36) | RFC 4122 UUID. |
| `"id"` | BIGINT AUTO_INCREMENT / SERIAL | Surrogate PK. Alias for uint64. |
| `"ref"` | FOREIGN KEY (bigint) | Logical foreign-key reference. |

#### Structured & Special Types

| Type token | SQL equivalent | Notes |
|---|---|---|
| `"json"` | JSON / JSONB | Arbitrary JSON value. |
| `"array"` | ARRAY / JSON array | Homogeneous list. Specify `"items_type"`. |
| `"map"` | JSONB / HSTORE | Key-value pairs. |
| `"enum"` | ENUM | Reference to an enum entity via `"ref_id"`. |
| `"any"` | VARIANT / TEXT | Dynamic / unknown type. |

**`"array"` field example:**

```jsonc
{
  "name":       "tags",
  "type":       "array",
  "items_type": "string",
  "comment":    "List of string tags."
}
```

**`"enum"` field example:**

```jsonc
{
  "name":    "status",
  "type":    "enum",
  "ref_id":  "account_status",
  "comment": "Current account lifecycle state."
}
```

---

### 4.4 Field Constraints

The `constraints` array holds zero or more of these string tokens:

| Token | Meaning |
|---|---|
| `"pk"` | Primary key. |
| `"fk"` | Foreign key (pair with a `Relation` of kind `"foreign_key"`). |
| `"unique"` | Unique constraint. |
| `"index"` | Regular (non-unique) index. |
| `"not_null"` | Explicit NOT NULL (same as `nullable: false` but more visible). |
| `"auto"` | Auto-increment / auto-generated (sequences, UUIDs, timestamps). |
| `"check"` | Has a check expression (put the expression in `comment`). |
| `"default"` | Has a default value (mirror of the `default` key). |
| `"virtual"` | Computed / virtual column, not stored. |
| `"immutable"` | Value set once at creation, never updated. |
| `"encrypted"` | Field is stored encrypted at rest. |
| `"deprecated"` | Field is kept for backwards compat but should not be used. |

---

### 4.5 Method Object (optional)

Methods are meaningful only for OOP entity kinds (`class`, `abstract`, `interface`, `mixin`).
DB-only models may omit `methods` entirely.

```jsonc
{
  "name":        "calculateTotal",
  "visibility":  "public",           // public | protected | private | internal
  "static":      false,
  "abstract":    false,
  "async":       false,
  "returns":     "decimal",          // Any field type token, or "void", or "self".
  "params": [
    { "name": "discount", "type": "float", "default": 0.0 }
  ],
  "comment":     "Returns the order total after applying a discount."
}
```

---

## 5. Relation Object

A **relation** is a directed link from one entity (`from`) to another (`to`).
It may reference specific fields that carry the foreign key or ownership marker.

```jsonc
{
  "id":           "order_user_fk",       // Required. Unique relation ID.
  "name":         "Order → User",        // Optional. Human label.
  "kind":         "foreign_key",         // Required. Relation kind (see §5.1).
  "from":         "order",               // Required. Source entity id.
  "to":           "user",                // Required. Target entity id.
  "from_field":   "user_id",             // Optional. Field on source carrying the key.
  "to_field":     "id",                  // Optional. Field on target being referenced.
  "multiplicity": "many_to_one",         // Optional. Cardinality (see §5.2).
  "cascade":      "delete",             // Optional. delete | update | restrict | set_null
  "navigable":    "both",               // Optional. from | to | both | none
  "comment":      "Each order belongs to one user.",
  "$comment":     "Internal note."
}
```

| Key | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✅ | Unique identifier for this relation. |
| `name` | string | ❌ | Human-readable label. |
| `kind` | string | ✅ | Relation kind (see §5.1). |
| `from` | string | ✅ | `id` of the source entity. |
| `to` | string | ✅ | `id` of the target entity. |
| `from_field` | string | ❌ | Field on `from` entity (FK holder, owner). |
| `to_field` | string | ❌ | Field on `to` entity (PK being referenced). |
| `multiplicity` | string | ❌ | Cardinality token (see §5.2). |
| `cascade` | string | ❌ | DB cascade rule: `delete`, `update`, `restrict`, `set_null`. |
| `navigable` | string | ❌ | Which direction can navigate: `from`, `to`, `both`, `none`. |
| `comment` | string | ❌ | Human description. |

---

### 5.1 Relation Kinds

Covers all six UML class-diagram relationship types plus DB-specific ones:

| `kind` | Origin | Meaning |
|---|---|---|
| `"association"` | UML | General link. One class uses or knows about another. |
| `"directed_association"` | UML | One-directional association (has-a, one way). |
| `"aggregation"` | UML | Weak whole/part. Part can exist without whole. (hollow diamond) |
| `"composition"` | UML | Strong whole/part. Part cannot exist without whole. (solid diamond) |
| `"inheritance"` | UML / OOP | Is-a / Generalization. Subclass extends superclass. |
| `"realization"` | UML / OOP | Class implements an interface or protocol. |
| `"dependency"` | UML | Weak usage. Source uses target transiently. |
| `"foreign_key"` | DB | SQL foreign-key constraint from `from_field` to `to_field`. |
| `"many_to_many"` | DB | Junction / bridge table relationship. |
| `"self"` | DB / OOP | Recursive / self-referential (entity references itself). |
| `"mixin"` | OOP | Source mixes in (uses / includes) target trait/mixin. |

**UML Cheat-Sheet:**

```
inheritance      ──────▷   is-a (extends)
realization      - - - ▷   implements interface
composition      ◆──────   part dies with whole
aggregation      ◇──────   part survives whole
association      ───────   general has-a/uses
dependency       - - - →   weak usage / import
```

---

### 5.2 Multiplicity

The `multiplicity` field describes cardinality on both ends.
Uses standard UML notation encoded as a token:

| Token | UML | Meaning |
|---|---|---|
| `"one_to_one"` | 1 — 1 | Exactly one on each side. |
| `"one_to_zero_one"` | 1 — 0..1 | One source, zero or one target. |
| `"one_to_many"` | 1 — 1..* | One source, one or more targets. |
| `"one_to_zero_many"` | 1 — 0..* | One source, zero or more targets. |
| `"many_to_one"` | \*..*1 — 1 | Many sources, one target (typical FK). |
| `"many_to_many"` | \* — \* | Many on both sides (junction table). |
| `"zero_one_to_many"` | 0..1 — \* | Optional source, many targets. |

You may also use a **raw UML string** when none of the tokens fit:

```jsonc
"multiplicity_raw": "2..5"
```

---

## 6. Comments & Annotations

EntityMap has two comment mechanisms:

### 6.1 `$comment` — Tooling-ignored notes

Any object may contain `"$comment": "..."`. It is purely for human readers; all generators
must skip it silently. Use it for:
- Implementation notes
- TODO / FIXME
- Reasons behind a design decision

```jsonc
{
  "name": "deleted_at",
  "type": "timestamp",
  "nullable": true,
  "$comment": "Soft-delete sentinel. NULL = active record."
}
```

### 6.2 `comment` — Semantic description

`comment` (without `$`) is a **semantic annotation** that generators should preserve:
- As SQL column comment (`COMMENT ON COLUMN ...`)
- As JSDoc / docstring on a class field
- As Swagger/OpenAPI description in API schemas
- As tooltip in visual editors

Both keys may coexist on the same object.

---

## 7. Reserved Keys Summary

| Key | Scope | Role |
|---|---|---|
| `$entitymap` | Root | Spec version. |
| `$comment` | Any object | Human-only note, ignored by tooling. |
| `meta` | Root | Project metadata block. |
| `entities` | Root | Array of all entities. |
| `relations` | Root | Array of all relations. |
| `id` | Entity, Relation | Unique machine identifier. |
| `name` | Entity, Field, Relation, Method, Param | Display name. |
| `kind` | Entity, Relation | Categorical type token. |
| `comment` | Entity, Field, Relation, Method | Semantic description for generators. |
| `fields` | Entity | Array of Field objects. |
| `methods` | Entity | Array of Method objects. |
| `type` | Field, Param | Data type token. |
| `constraints` | Field | Array of constraint tokens. |
| `multiplicity` | Relation | Cardinality token. |
| `from` / `to` | Relation | Source and target entity `id`. |
| `from_field` / `to_field` | Relation | Fields carrying the link. |

---

## 8. Full Example

```jsonc
{
  "$entitymap": "1.0",
  "$comment": "Sample e-commerce model demonstrating all major features.",

  "meta": {
    "title":   "Shop Domain Model",
    "version": "1.0.0",
    "author":  "Backend Team"
  },

  "entities": [

    // ── Enum ────────────────────────────────────────────────────────────────
    {
      "id":      "order_status",
      "name":    "OrderStatus",
      "kind":    "enum",
      "comment": "Lifecycle states of a customer order.",
      "fields": [
        { "name": "PENDING",   "comment": "Awaiting payment." },
        { "name": "PAID",      "comment": "Payment confirmed." },
        { "name": "SHIPPED",   "comment": "Dispatched to carrier." },
        { "name": "DELIVERED", "comment": "Received by customer." },
        { "name": "CANCELLED", "comment": "Cancelled before shipment." }
      ]
    },

    // ── Interface ────────────────────────────────────────────────────────────
    {
      "id":      "auditable",
      "name":    "Auditable",
      "kind":    "interface",
      "comment": "Any entity that tracks creation and modification times.",
      "fields": [
        { "name": "created_at", "type": "timestamp", "comment": "Creation timestamp." },
        { "name": "updated_at", "type": "timestamp", "comment": "Last update timestamp." }
      ]
    },

    // ── Class / Table ────────────────────────────────────────────────────────
    {
      "id":        "user",
      "name":      "User",
      "kind":      "class",
      "namespace": "auth",
      "comment":   "Registered platform user.",
      "fields": [
        {
          "name": "id",
          "type": "uuid",
          "constraints": ["pk", "auto"],
          "comment": "Surrogate primary key."
        },
        {
          "name": "email",
          "type": "string",
          "length": 254,
          "nullable": false,
          "constraints": ["unique", "index"],
          "comment": "RFC 5321 email address. Must be unique."
        },
        {
          "name": "password_hash",
          "type": "string",
          "length": 128,
          "nullable": false,
          "constraints": ["encrypted"],
          "comment": "Bcrypt hash of the user password.",
          "$comment": "Never log or expose this field."
        },
        {
          "name": "full_name",
          "type": "string",
          "length": 200,
          "nullable": true,
          "default": null,
          "comment": "Display name. Optional."
        },
        {
          "name": "is_active",
          "type": "bool",
          "default": true,
          "comment": "False = soft-banned account."
        },
        {
          "name": "created_at",
          "type": "timestamp",
          "constraints": ["auto", "immutable"],
          "comment": "Account creation time (UTC)."
        }
      ],
      "methods": [
        {
          "name":       "fullName",
          "visibility": "public",
          "returns":    "string",
          "comment":    "Returns formatted display name."
        },
        {
          "name":       "changePassword",
          "visibility": "public",
          "params": [
            { "name": "raw_password", "type": "string" }
          ],
          "returns": "void",
          "comment": "Hashes and stores the new password."
        }
      ]
    },

    {
      "id":      "product",
      "name":    "Product",
      "kind":    "class",
      "comment": "Sellable item in the catalogue.",
      "fields": [
        { "name": "id",          "type": "id",      "constraints": ["pk", "auto"] },
        { "name": "sku",         "type": "string",  "length": 64,  "constraints": ["unique"], "comment": "Stock-keeping unit code." },
        { "name": "title",       "type": "string",  "length": 255, "nullable": false },
        { "name": "description", "type": "text",    "nullable": true },
        { "name": "price",       "type": "decimal", "precision": 12, "scale": 2, "comment": "Retail price in base currency." },
        { "name": "stock",       "type": "int32",   "default": 0,  "comment": "Available units in warehouse." },
        { "name": "tags",        "type": "array",   "items_type": "string", "comment": "Search tags." },
        { "name": "is_active",   "type": "bool",    "default": true }
      ]
    },

    {
      "id":      "order",
      "name":    "Order",
      "kind":    "class",
      "comment": "A purchase made by a user.",
      "fields": [
        { "name": "id",         "type": "id",        "constraints": ["pk", "auto"] },
        { "name": "user_id",    "type": "uuid",      "constraints": ["fk", "index"],   "comment": "FK → User.id" },
        { "name": "status",     "type": "enum",      "ref_id": "order_status",          "comment": "Current order status." },
        { "name": "total",      "type": "decimal",   "precision": 14, "scale": 2,       "comment": "Computed grand total." },
        { "name": "created_at", "type": "timestamp", "constraints": ["auto", "immutable"] },
        { "name": "notes",      "type": "text",      "nullable": true,                  "comment": "Optional customer notes." }
      ]
    },

    {
      "id":      "order_item",
      "name":    "OrderItem",
      "kind":    "class",
      "comment": "A single line inside an order.",
      "fields": [
        { "name": "id",         "type": "id",      "constraints": ["pk", "auto"] },
        { "name": "order_id",   "type": "id",      "constraints": ["fk", "index"] },
        { "name": "product_id", "type": "id",      "constraints": ["fk", "index"] },
        { "name": "quantity",   "type": "int32",   "default": 1 },
        { "name": "unit_price", "type": "decimal", "precision": 12, "scale": 2 }
      ]
    }

  ],

  "relations": [

    {
      "id":           "order_belongs_to_user",
      "name":         "Order → User",
      "kind":         "foreign_key",
      "from":         "order",
      "to":           "user",
      "from_field":   "user_id",
      "to_field":     "id",
      "multiplicity": "many_to_one",
      "cascade":      "restrict",
      "comment":      "Many orders belong to one user. Deletion of user is restricted while orders exist."
    },

    {
      "id":           "order_item_belongs_to_order",
      "name":         "OrderItem → Order",
      "kind":         "composition",
      "from":         "order_item",
      "to":           "order",
      "from_field":   "order_id",
      "to_field":     "id",
      "multiplicity": "many_to_one",
      "cascade":      "delete",
      "comment":      "Items cannot exist without their parent order (composition)."
    },

    {
      "id":           "order_item_references_product",
      "name":         "OrderItem → Product",
      "kind":         "foreign_key",
      "from":         "order_item",
      "to":           "product",
      "from_field":   "product_id",
      "to_field":     "id",
      "multiplicity": "many_to_one",
      "cascade":      "restrict"
    },

    {
      "id":      "user_implements_auditable",
      "name":    "User implements Auditable",
      "kind":    "realization",
      "from":    "user",
      "to":      "auditable",
      "comment": "User satisfies the Auditable interface contract."
    },

    {
      "id":      "order_implements_auditable",
      "name":    "Order implements Auditable",
      "kind":    "realization",
      "from":    "order",
      "to":      "auditable"
    }

  ]
}
```

---

## 9. AI Generation Guide

This section tells an AI model exactly how to read and produce EntityMap JSON.

### 9.1 Reading / Understanding a Map

1. Load the root object and confirm `"$entitymap": "1.0"`.
2. Index all entities by `id` into a lookup map.
3. Index all relations by `id`.
4. When resolving a `"type": "enum"` field, look up `"ref_id"` in the entity index.
5. Treat `$comment` keys as invisible; only `comment` keys carry semantic meaning.
6. A field with `"constraints": ["pk"]` is the primary key of its entity.
7. A field with `"constraints": ["fk"]` has a corresponding `Relation` object; find it by
   matching `from` == entity.id and `from_field` == field.name.

### 9.2 Generating a Map

- **Always** assign unique `id` values in `snake_case`.
- **Always** include `"$entitymap": "1.0"` as the first key.
- **Always** include `"entities": []` and `"relations": []` even if empty.
- Encode every foreign-key field (`constraints: ["fk"]`) as **both**:
  a) a field with `"constraints": ["fk"]` inside the entity, and
  b) a `Relation` object in `relations` with `kind: "foreign_key"`.
- Use `"kind": "composition"` when the child entity cannot exist without the parent.
- Use `"kind": "aggregation"` when the child can survive without the parent.
- Use `"kind": "inheritance"` for class extension (extends / : Base).
- Use `"kind": "realization"` for interface implementation (implements / : IFoo).
- Prefer precise types (`"int32"`, `"decimal"`) over generic ones (`"int"`, `"float"`)
  when the target DB or language requires precision.
- Add `"comment"` to every entity and every field. Generators use these as docstrings.

### 9.3 Deploying a Map

| Target | Action |
|---|---|
| SQL (PostgreSQL) | `class`/`table` entities → `CREATE TABLE`. `foreign_key` relations → `ALTER TABLE … ADD CONSTRAINT`. `enum` entities → `CREATE TYPE … AS ENUM`. |
| SQL (MySQL) | Same as above; map `uuid` → `CHAR(36)`, `bool` → `TINYINT(1)`. |
| Python (dataclass) | Each entity → `@dataclass`. Fields → typed attributes. `inheritance` → base class. `realization` → ABC. |
| C# | Each entity → `class` or `interface`. Fields → properties. `inheritance` → `: Base`. `realization` → `: IFoo`. |
| TypeScript | Each entity → `interface` or `class`. Enums → `enum`. |
| Java | Each entity → class/interface. Use `@Column`, `@OneToMany`, etc. for JPA. |
| OpenAPI | Each entity → schema component in `components/schemas`. |

### 9.4 Validation Rules (for linters / CI)

- Every `id` must be unique across all entities.
- Every `id` must be unique across all relations.
- Every `from` and `to` in a relation must reference an existing entity `id`.
- Every `from_field` must name a field that actually exists in the `from` entity.
- Every `to_field` must name a field that actually exists in the `to` entity.
- Fields with `"type": "enum"` must have a `ref_id` pointing to a `kind: "enum"` entity.
- Fields with `"type": "array"` must have an `items_type` key.
- An entity of `kind: "enum"` must not have fields with a `type` key (enum values are literal).
- `nullable: true` and `constraints: ["not_null"]` on the same field is a conflict → error.

---

*End of EntityMapJSONLanguage v1.0 Specification.*
