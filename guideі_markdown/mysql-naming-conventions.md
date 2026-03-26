# MySQL Naming Conventions — The Complete Guide

> Covers ISO SQL standards, MySQL best practices, popular ORM conventions (Laravel Eloquent, Django ORM, SQLAlchemy, Hibernate), and modern database design principles.

---

## Table of Contents

1. [General Principles](#1-general-principles)
2. [Databases & Schemas](#2-databases--schemas)
3. [Tables](#3-tables)
4. [Columns](#4-columns)
5. [Primary Keys](#5-primary-keys)
6. [Foreign Keys](#6-foreign-keys)
7. [Indexes](#7-indexes)
8. [Constraints](#8-constraints)
9. [Views](#9-views)
10. [Stored Procedures](#10-stored-procedures)
11. [Functions](#11-functions)
12. [Triggers](#12-triggers)
13. [Events](#13-events)
14. [Temporary Tables](#14-temporary-tables)
15. [Junction / Pivot Tables](#15-junction--pivot-tables)
16. [Audit & Log Tables](#16-audit--log-tables)
17. [Partitioned Tables](#17-partitioned-tables)
18. [Data Types & Column Patterns](#18-data-types--column-patterns)
19. [Boolean Columns](#19-boolean-columns)
20. [Date & Time Columns](#20-date--time-columns)
21. [Status & State Columns](#21-status--state-columns)
22. [JSON Columns](#22-json-columns)
23. [ORM Conventions](#23-orm-conventions)
24. [Migrations](#24-migrations)
25. [Naming Anti-patterns](#25-naming-anti-patterns)
26. [Quick Reference Cheatsheet](#26-quick-reference-cheatsheet)
27. [References & Further Reading](#27-references--further-reading)

---

## 1. General Principles

- **Use `snake_case` everywhere** — MySQL identifiers are case-insensitive on most systems, but snake_case is the universal SQL convention.
- **Be descriptive.** `user_account_status` beats `uas` or `stat`.
- **Be consistent.** The worst convention is an inconsistent one.
- **Avoid reserved words** — never name a table or column after a SQL keyword (`order`, `select`, `group`, `key`, `value`, `date`, `status`, `type`). If unavoidable, prefix it: `order_status`, `record_type`.
- **Use singular or plural consistently** — singular is ISO standard, plural is ORM-friendly (Laravel, Django). Pick one and never mix.
- **No spaces, no hyphens** — use underscores only.
- **No prefixes like `tbl_`, `col_`, `fk_` on tables/columns** — these are noise. Exceptions: indexes and constraints benefit from prefixes.
- **Keep names under 64 characters** — MySQL's identifier length limit.
- **Use lowercase** — even though MySQL is case-insensitive, lowercase prevents cross-platform issues (Linux file system is case-sensitive).

---

## 2. Databases & Schemas

Use **snake_case**, short but descriptive:

```sql
-- ✅ Good
CREATE DATABASE ecommerce;
CREATE DATABASE user_management;
CREATE DATABASE analytics_platform;
CREATE DATABASE crm_system;
CREATE DATABASE blog_app;

-- ✅ With environment suffix (useful in dev environments)
CREATE DATABASE ecommerce_production;
CREATE DATABASE ecommerce_staging;
CREATE DATABASE ecommerce_test;

-- ❌ Bad
CREATE DATABASE Ecommerce;          -- mixed case
CREATE DATABASE eCommerceDB;        -- camelCase + noise suffix
CREATE DATABASE tbl_ecommerce;      -- tbl prefix on database
CREATE DATABASE my-database;        -- hyphens not allowed
CREATE DATABASE `My Database`;      -- spaces — backticks required, messy
```

---

## 3. Tables

Use **snake_case**. The singular vs plural debate:

### Option A — Plural (ORM-friendly, most popular today)

Used by: Laravel, Django, Rails, most modern frameworks.

```sql
-- ✅ Plural table names
CREATE TABLE users (...);
CREATE TABLE orders (...);
CREATE TABLE products (...);
CREATE TABLE blog_posts (...);
CREATE TABLE order_items (...);
CREATE TABLE payment_methods (...);
CREATE TABLE user_addresses (...);
CREATE TABLE product_categories (...);
CREATE TABLE email_templates (...);
CREATE TABLE audit_logs (...);
```

### Option B — Singular (ISO SQL standard, some enterprise shops)

```sql
-- ✅ Singular table names
CREATE TABLE user (...);
CREATE TABLE order (...);        -- ⚠️ 'order' is a reserved word! Avoid
CREATE TABLE product (...);
CREATE TABLE blog_post (...);
CREATE TABLE order_item (...);
```

> **Recommendation:** Use **plural**. It reads naturally (`SELECT * FROM users`), matches most ORM defaults, and avoids collisions with reserved words like `user` and `order`.

### Table naming patterns

```sql
-- ✅ Entity tables — plural noun
CREATE TABLE users (...);
CREATE TABLE products (...);
CREATE TABLE categories (...);
CREATE TABLE invoices (...);

-- ✅ Multi-word tables — snake_case plural
CREATE TABLE blog_posts (...);
CREATE TABLE order_items (...);
CREATE TABLE user_profiles (...);
CREATE TABLE product_variants (...);
CREATE TABLE shipping_addresses (...);
CREATE TABLE payment_transactions (...);

-- ✅ Junction / pivot tables — both entities, alphabetical order
CREATE TABLE category_product (...);  -- singular pair
CREATE TABLE role_user (...);
CREATE TABLE permission_role (...);
CREATE TABLE product_tag (...);

-- ✅ Log / history tables — suffix with _log, _history, _archive
CREATE TABLE audit_logs (...);
CREATE TABLE order_history (...);
CREATE TABLE price_history (...);
CREATE TABLE users_archive (...);

-- ❌ Bad
CREATE TABLE tbl_users (...);        -- tbl_ prefix — noise
CREATE TABLE USERS (...);            -- all caps
CREATE TABLE usersTable (...);       -- camelCase + noise suffix
CREATE TABLE t_users (...);          -- single letter prefix
CREATE TABLE `user data` (...);      -- spaces
```

---

## 4. Columns

Use **snake_case**. Be specific about what the column stores:

```sql
CREATE TABLE users
(
    -- ✅ Good column names
    id                  INT             NOT NULL AUTO_INCREMENT,
    first_name          VARCHAR(100)    NOT NULL,
    last_name           VARCHAR(100)    NOT NULL,
    email               VARCHAR(255)    NOT NULL,
    phone_number        VARCHAR(20),
    date_of_birth       DATE,
    password_hash       VARCHAR(255)    NOT NULL,
    profile_picture_url VARCHAR(500),
    bio                 TEXT,
    website_url         VARCHAR(500),
    is_active           TINYINT(1)      NOT NULL DEFAULT 1,
    is_verified         TINYINT(1)      NOT NULL DEFAULT 0,
    email_verified_at   DATETIME,
    last_login_at       DATETIME,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at          DATETIME,

    PRIMARY KEY (id)
);
```

### Column naming rules

```sql
-- ✅ Specific, descriptive
first_name          -- not just 'name' (ambiguous)
phone_number        -- not 'phone' (what kind?)
password_hash       -- not 'password' (implies plain text — dangerous!)
profile_picture_url -- not 'image' or 'pic'
total_amount        -- not 'total' (amount of what?)
unit_price          -- not 'price' (per unit? total?)
tax_rate            -- not 'tax' (rate? amount?)
shipping_address_id -- not 'address_id' (which address?)

-- ❌ Bad
nm                  -- cryptic abbreviation
usr_fn              -- abbreviated nonsense
profilePicture      -- camelCase
ProfilePicture      -- PascalCase
FIRST_NAME          -- all caps
col_first_name      -- col_ prefix (noise)
first_name_col      -- _col suffix (noise)
```

---

## 5. Primary Keys

Use **`id`** as the primary key name (simple, universal):

```sql
-- ✅ Most common — simple 'id'
CREATE TABLE users
(
    id      INT             UNSIGNED NOT NULL AUTO_INCREMENT,
    -- ...
    PRIMARY KEY (id)
);

-- ✅ Alternative — table_name + _id (explicit, preferred by some)
CREATE TABLE users
(
    user_id INT             UNSIGNED NOT NULL AUTO_INCREMENT,
    -- ...
    PRIMARY KEY (user_id)
);

-- ✅ UUID primary key
CREATE TABLE users
(
    id      CHAR(36)        NOT NULL DEFAULT (UUID()),
    -- or
    id      BINARY(16)      NOT NULL,
    -- ...
    PRIMARY KEY (id)
);

-- ✅ Composite primary key — for junction tables
CREATE TABLE role_user
(
    role_id INT UNSIGNED NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (role_id, user_id)
);
```

> **`id` vs `table_id`:**
> - `id` — simpler, widely used (Django, Laravel, Rails default)
> - `user_id` in the `users` table — more explicit, avoids ambiguity in complex joins

---

## 6. Foreign Keys

Name foreign key **columns** as `referenced_table_singular + _id`:

```sql
CREATE TABLE orders
(
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id         INT UNSIGNED NOT NULL,    -- references users.id
    billing_address_id   INT UNSIGNED,        -- references addresses.id
    shipping_address_id  INT UNSIGNED,        -- references addresses.id
    coupon_id       INT UNSIGNED,             -- references coupons.id
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),

    CONSTRAINT fk_orders_user_id
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_orders_billing_address_id
        FOREIGN KEY (billing_address_id) REFERENCES addresses (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_orders_shipping_address_id
        FOREIGN KEY (shipping_address_id) REFERENCES addresses (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

### FK column naming patterns

```sql
-- ✅ Standard — singular_table_id
user_id             -- references users.id
order_id            -- references orders.id
product_id          -- references products.id
category_id         -- references categories.id
parent_id           -- self-referential (same table)

-- ✅ When same table is referenced multiple times — add context
billing_address_id      -- references addresses (for billing)
shipping_address_id     -- references addresses (for shipping)
created_by_user_id      -- references users (who created)
approved_by_user_id     -- references users (who approved)
manager_id              -- references employees.id (self-ref)
parent_category_id      -- references categories.id (self-ref)

-- ❌ Bad
address                 -- no _id suffix — unclear it's FK
addressId               -- camelCase
fk_user                 -- fk_ prefix on column (noise)
users_id                -- plural
```

### FK constraint naming — `fk_table_column`

```sql
-- ✅ Pattern: fk_{table}_{column}
CONSTRAINT fk_orders_user_id
    FOREIGN KEY (user_id) REFERENCES users (id)

CONSTRAINT fk_order_items_order_id
    FOREIGN KEY (order_id) REFERENCES orders (id)

CONSTRAINT fk_order_items_product_id
    FOREIGN KEY (product_id) REFERENCES products (id)

-- ✅ When ambiguous: fk_{table}_{referenced_table}_{column}
CONSTRAINT fk_orders_users_billing_address_id
    FOREIGN KEY (billing_address_id) REFERENCES addresses (id)
```

---

## 7. Indexes

Always name indexes explicitly. Use prefixes to signal type:

### Index naming patterns

| Type | Prefix | Pattern | Example |
|------|--------|---------|---------|
| Regular index | `idx_` | `idx_{table}_{column(s)}` | `idx_users_email` |
| Unique index | `uniq_` or `uk_` | `uniq_{table}_{column(s)}` | `uniq_users_email` |
| Full-text index | `ft_` | `ft_{table}_{column(s)}` | `ft_posts_content` |
| Composite index | `idx_` | `idx_{table}_{col1}_{col2}` | `idx_orders_user_id_status` |
| Prefix index | `idx_` | `idx_{table}_{column}_prefix` | `idx_users_email_prefix` |

```sql
CREATE TABLE users
(
    id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    first_name      VARCHAR(100)    NOT NULL,
    last_name       VARCHAR(100)    NOT NULL,
    email           VARCHAR(255)    NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'active',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),

    -- ✅ Unique index
    UNIQUE INDEX uniq_users_email (email),

    -- ✅ Regular indexes
    INDEX idx_users_status (status),
    INDEX idx_users_created_at (created_at),
    INDEX idx_users_last_name (last_name),

    -- ✅ Composite index — column order matters (most selective first)
    INDEX idx_users_status_created_at (status, created_at),
    INDEX idx_users_last_name_first_name (last_name, first_name)
);

-- ✅ Adding indexes separately
CREATE INDEX idx_orders_user_id
    ON orders (user_id);

CREATE INDEX idx_orders_status_created_at
    ON orders (status, created_at);

CREATE UNIQUE INDEX uniq_products_sku
    ON products (sku);

-- ✅ Full-text index
CREATE FULLTEXT INDEX ft_articles_title_body
    ON articles (title, body);

-- ❌ Bad
CREATE INDEX i1 ON users (email);              -- meaningless name
CREATE INDEX email_index ON users (email);     -- vague, no table reference
CREATE INDEX users_email ON users (email);     -- no type prefix
CREATE INDEX idx ON users (email);             -- incomplete
```

---

## 8. Constraints

### CHECK constraints — `chk_{table}_{column}`

```sql
CREATE TABLE products
(
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    name        VARCHAR(255)    NOT NULL,
    price       DECIMAL(10, 2)  NOT NULL,
    stock       INT             NOT NULL DEFAULT 0,
    rating      DECIMAL(2, 1),
    weight_kg   DECIMAL(8, 3),
    PRIMARY KEY (id),

    -- ✅ CHECK constraint naming
    CONSTRAINT chk_products_price_positive
        CHECK (price >= 0),

    CONSTRAINT chk_products_stock_non_negative
        CHECK (stock >= 0),

    CONSTRAINT chk_products_rating_range
        CHECK (rating BETWEEN 0.0 AND 5.0),

    CONSTRAINT chk_products_weight_positive
        CHECK (weight_kg > 0)
);
```

### UNIQUE constraints — `uniq_{table}_{column(s)}`

```sql
CREATE TABLE users
(
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    email           VARCHAR(255) NOT NULL,
    username        VARCHAR(50)  NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT uniq_users_email    UNIQUE (email),
    CONSTRAINT uniq_users_username UNIQUE (username)
);

-- Composite unique
CREATE TABLE subscriptions
(
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     INT UNSIGNED NOT NULL,
    plan_id     INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT uniq_subscriptions_user_plan UNIQUE (user_id, plan_id)
);
```

### NOT NULL and DEFAULT — inline, no naming needed

```sql
email   VARCHAR(255) NOT NULL,
status  VARCHAR(20)  NOT NULL DEFAULT 'active',
score   INT          NOT NULL DEFAULT 0,
```

---

## 9. Views

Prefix with `v_` or `vw_` to distinguish from tables:

```sql
-- ✅ Pattern: v_{descriptive_name} or vw_{descriptive_name}
CREATE VIEW v_active_users AS
    SELECT id, first_name, last_name, email, created_at
    FROM users
    WHERE is_active = 1 AND deleted_at IS NULL;


CREATE VIEW v_order_summary AS
    SELECT
        o.id            AS order_id,
        u.first_name,
        u.last_name,
        u.email,
        COUNT(oi.id)    AS item_count,
        SUM(oi.unit_price * oi.quantity) AS total_amount,
        o.status,
        o.created_at
    FROM orders o
    JOIN users u ON u.id = o.user_id
    JOIN order_items oi ON oi.order_id = o.id
    GROUP BY o.id, u.id;


CREATE VIEW v_product_inventory AS
    SELECT
        p.id,
        p.name,
        p.sku,
        p.price,
        p.stock_quantity,
        c.name AS category_name
    FROM products p
    JOIN categories c ON c.id = p.category_id;


-- ✅ Report views — prefix with v_report_
CREATE VIEW v_report_monthly_sales AS
    SELECT
        YEAR(created_at)  AS sale_year,
        MONTH(created_at) AS sale_month,
        COUNT(*)          AS order_count,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY sale_year, sale_month;


-- ❌ Bad
CREATE VIEW users_active AS ...;    -- no v_ prefix
CREATE VIEW ActiveUsers AS ...;     -- PascalCase
CREATE VIEW view_users AS ...;      -- 'view' prefix redundant
```

---

## 10. Stored Procedures

Prefix with `sp_` or `usp_` (user stored procedure):

```sql
-- ✅ Pattern: sp_{verb}_{noun} or usp_{verb}_{noun}

DELIMITER $$

CREATE PROCEDURE sp_get_user_by_id(
    IN  p_user_id   INT UNSIGNED,
    OUT p_found     TINYINT
)
BEGIN
    SELECT * FROM users WHERE id = p_user_id AND deleted_at IS NULL;
    SET p_found = ROW_COUNT() > 0;
END$$


CREATE PROCEDURE sp_create_order(
    IN  p_user_id           INT UNSIGNED,
    IN  p_shipping_address  VARCHAR(500),
    OUT p_order_id          INT UNSIGNED
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO orders (user_id, shipping_address, status, created_at)
    VALUES (p_user_id, p_shipping_address, 'pending', NOW());

    SET p_order_id = LAST_INSERT_ID();

    COMMIT;
END$$


CREATE PROCEDURE sp_update_user_status(
    IN p_user_id    INT UNSIGNED,
    IN p_is_active  TINYINT(1)
)
BEGIN
    UPDATE users
    SET is_active = p_is_active,
        updated_at = NOW()
    WHERE id = p_user_id;
END$$


CREATE PROCEDURE sp_delete_user_soft(
    IN p_user_id INT UNSIGNED
)
BEGIN
    UPDATE users
    SET deleted_at = NOW(),
        is_active  = 0
    WHERE id = p_user_id
      AND deleted_at IS NULL;
END$$

DELIMITER ;


-- ✅ Procedure parameter naming — p_ prefix
-- IN  p_user_id, p_email, p_status
-- OUT p_result, p_order_id, p_error_message
-- INOUT p_counter, p_balance

-- ❌ Bad
CREATE PROCEDURE getUser() ...;       -- no prefix
CREATE PROCEDURE GetUserById() ...;   -- PascalCase
CREATE PROCEDURE proc_user() ...;     -- vague
CREATE PROCEDURE sp_1() ...;          -- meaningless
```

---

## 11. Functions

Prefix with `fn_` or `func_`:

```sql
DELIMITER $$

-- ✅ Scalar function
CREATE FUNCTION fn_get_full_name(
    p_first_name VARCHAR(100),
    p_last_name  VARCHAR(100)
)
RETURNS VARCHAR(201)
DETERMINISTIC
BEGIN
    RETURN CONCAT(p_first_name, ' ', p_last_name);
END$$


CREATE FUNCTION fn_calculate_age(
    p_date_of_birth DATE
)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, p_date_of_birth, CURDATE());
END$$


CREATE FUNCTION fn_is_valid_email(
    p_email VARCHAR(255)
)
RETURNS TINYINT(1)
DETERMINISTIC
BEGIN
    RETURN p_email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
END$$


CREATE FUNCTION fn_format_currency(
    p_amount        DECIMAL(15, 2),
    p_currency_code CHAR(3)
)
RETURNS VARCHAR(30)
DETERMINISTIC
BEGIN
    RETURN CONCAT(p_currency_code, ' ', FORMAT(p_amount, 2));
END$$

DELIMITER ;


-- ❌ Bad
CREATE FUNCTION getFullName() ...;    -- no prefix, camelCase
CREATE FUNCTION FullName() ...;       -- PascalCase
CREATE FUNCTION f1() ...;             -- meaningless
```

---

## 12. Triggers

Pattern: `{timing}_{table}_{event}` or `trg_{table}_{timing}_{event}`:

```sql
DELIMITER $$

-- ✅ Pattern: trg_{table}_{timing}_{event}
-- timing: before / after
-- event:  insert / update / delete

CREATE TRIGGER trg_users_before_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SET NEW.created_at = IFNULL(NEW.created_at, NOW());
    SET NEW.updated_at = NOW();
END$$


CREATE TRIGGER trg_users_before_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END$$


CREATE TRIGGER trg_orders_after_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (table_name, record_id, action, created_at)
    VALUES ('orders', NEW.id, 'INSERT', NOW());
END$$


CREATE TRIGGER trg_products_after_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    IF OLD.price <> NEW.price THEN
        INSERT INTO price_history (product_id, old_price, new_price, changed_at)
        VALUES (NEW.id, OLD.price, NEW.price, NOW());
    END IF;
END$$


CREATE TRIGGER trg_order_items_after_delete
AFTER DELETE ON order_items
FOR EACH ROW
BEGIN
    -- Restore stock
    UPDATE products
    SET stock_quantity = stock_quantity + OLD.quantity
    WHERE id = OLD.product_id;
END$$

DELIMITER ;


-- ❌ Bad
CREATE TRIGGER t1 ...;                    -- meaningless
CREATE TRIGGER users_insert ...;          -- no timing, no trg prefix
CREATE TRIGGER InsertUserTrigger ...;     -- PascalCase
```

---

## 13. Events

Prefix with `evt_` or `event_`:

```sql
DELIMITER $$

-- ✅ Pattern: evt_{action}_{subject}

CREATE EVENT evt_cleanup_expired_sessions
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
    DELETE FROM sessions
    WHERE expires_at < NOW();
END$$


CREATE EVENT evt_archive_old_orders
ON SCHEDULE EVERY 1 DAY
STARTS (CURRENT_TIMESTAMP + INTERVAL 1 DAY)
DO
BEGIN
    INSERT INTO orders_archive
    SELECT * FROM orders
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR)
      AND status IN ('completed', 'cancelled');

    DELETE FROM orders
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR)
      AND status IN ('completed', 'cancelled');
END$$


CREATE EVENT evt_send_daily_report
ON SCHEDULE EVERY 1 DAY
STARTS '2025-01-01 08:00:00'
DO
BEGIN
    CALL sp_generate_daily_report();
END$$

DELIMITER ;
```

---

## 14. Temporary Tables

Prefix with `tmp_` or `temp_`:

```sql
-- ✅ Session-level temporary tables
CREATE TEMPORARY TABLE tmp_active_users AS
    SELECT id, email, first_name, last_name
    FROM users
    WHERE is_active = 1 AND deleted_at IS NULL;


CREATE TEMPORARY TABLE tmp_order_totals
(
    order_id        INT UNSIGNED NOT NULL,
    subtotal        DECIMAL(10, 2) NOT NULL,
    tax_amount      DECIMAL(10, 2) NOT NULL,
    total_amount    DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id)
);


-- ✅ CTEs (preferred over temp tables in modern MySQL 8.0+)
WITH active_users AS (
    SELECT id, email, first_name, last_name
    FROM users
    WHERE is_active = 1 AND deleted_at IS NULL
),
user_order_counts AS (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
)
SELECT
    u.first_name,
    u.last_name,
    u.email,
    COALESCE(oc.order_count, 0) AS order_count
FROM active_users u
LEFT JOIN user_order_counts oc ON oc.user_id = u.id;
```

---

## 15. Junction / Pivot Tables

Use **both entity names** in alphabetical order, separated by underscore. Singular form:

```sql
-- ✅ Pattern: singular_entity1_singular_entity2 (alphabetical)
CREATE TABLE category_product
(
    category_id INT UNSIGNED NOT NULL,
    product_id  INT UNSIGNED NOT NULL,
    sort_order  INT          NOT NULL DEFAULT 0,
    PRIMARY KEY (category_id, product_id),
    INDEX idx_category_product_product_id (product_id),
    CONSTRAINT fk_category_product_category_id
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
    CONSTRAINT fk_category_product_product_id
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);


CREATE TABLE permission_role
(
    permission_id   INT UNSIGNED NOT NULL,
    role_id         INT UNSIGNED NOT NULL,
    PRIMARY KEY (permission_id, role_id),
    CONSTRAINT fk_permission_role_permission_id
        FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE,
    CONSTRAINT fk_permission_role_role_id
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
);


CREATE TABLE post_tag
(
    post_id INT UNSIGNED NOT NULL,
    tag_id  INT UNSIGNED NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    CONSTRAINT fk_post_tag_post_id FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
    CONSTRAINT fk_post_tag_tag_id  FOREIGN KEY (tag_id)  REFERENCES tags (id)  ON DELETE CASCADE
);


-- ✅ When pivot has extra data — give it a meaningful name
CREATE TABLE order_products     -- instead of order_product
(
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    order_id    INT UNSIGNED    NOT NULL,
    product_id  INT UNSIGNED    NOT NULL,
    quantity    INT             NOT NULL DEFAULT 1,
    unit_price  DECIMAL(10, 2)  NOT NULL,
    discount    DECIMAL(5, 2)   NOT NULL DEFAULT 0.00,
    PRIMARY KEY (id),
    UNIQUE INDEX uniq_order_products_order_product (order_id, product_id)
);
-- Better name here would be: order_items (domain-meaningful name)
```

---

## 16. Audit & Log Tables

```sql
-- ✅ General audit log
CREATE TABLE audit_logs
(
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    table_name      VARCHAR(100)    NOT NULL,
    record_id       BIGINT UNSIGNED NOT NULL,
    action          ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    old_values      JSON,
    new_values      JSON,
    changed_by      INT UNSIGNED,
    ip_address      VARCHAR(45),
    user_agent      VARCHAR(500),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_audit_logs_table_record (table_name, record_id),
    INDEX idx_audit_logs_created_at (created_at),
    INDEX idx_audit_logs_changed_by (changed_by)
);


-- ✅ Entity-specific history
CREATE TABLE price_history
(
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    product_id  INT UNSIGNED    NOT NULL,
    old_price   DECIMAL(10, 2)  NOT NULL,
    new_price   DECIMAL(10, 2)  NOT NULL,
    changed_by  INT UNSIGNED,
    changed_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_price_history_product_id (product_id),
    CONSTRAINT fk_price_history_product_id
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);


-- ✅ Activity / event log
CREATE TABLE user_activity_logs
(
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     INT UNSIGNED    NOT NULL,
    action      VARCHAR(100)    NOT NULL,
    entity_type VARCHAR(100),
    entity_id   BIGINT UNSIGNED,
    metadata    JSON,
    ip_address  VARCHAR(45),
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_user_activity_logs_user_id (user_id),
    INDEX idx_user_activity_logs_created_at (created_at)
);
```

---

## 17. Partitioned Tables

```sql
-- ✅ Partitioned log table — by range (year/month)
CREATE TABLE event_logs
(
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    event_type  VARCHAR(100)    NOT NULL,
    payload     JSON,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, created_at)   -- partition column must be in PK
)
PARTITION BY RANGE (YEAR(created_at))
(
    PARTITION p_2023 VALUES LESS THAN (2024),
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);


-- ✅ Partitioned by list (status-based)
CREATE TABLE orders_partitioned
(
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    status      VARCHAR(20)     NOT NULL,
    total       DECIMAL(10, 2)  NOT NULL,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, status)
)
PARTITION BY LIST COLUMNS (status)
(
    PARTITION p_pending     VALUES IN ('pending'),
    PARTITION p_processing  VALUES IN ('processing'),
    PARTITION p_completed   VALUES IN ('completed'),
    PARTITION p_cancelled   VALUES IN ('cancelled')
);
```

---

## 18. Data Types & Column Patterns

### Column name → recommended data type

```sql
-- IDs
id                  INT UNSIGNED / BIGINT UNSIGNED AUTO_INCREMENT
                    or CHAR(36) for UUID

-- Names & text
first_name          VARCHAR(100)
last_name           VARCHAR(100)
full_name           VARCHAR(201)    -- derived, rarely stored
username            VARCHAR(50)
title               VARCHAR(255)
slug                VARCHAR(255)    -- URL-safe version of title
description         TEXT
body                MEDIUMTEXT      -- longer content
notes               TEXT

-- Contact
email               VARCHAR(255)
phone_number        VARCHAR(20)     -- include country code prefix
website_url         VARCHAR(500)
avatar_url          VARCHAR(500)
profile_picture_url VARCHAR(500)

-- Money & numbers
price               DECIMAL(10, 2)  -- NOT FLOAT (floating point errors!)
total_amount        DECIMAL(15, 2)
tax_rate            DECIMAL(5, 4)   -- e.g. 0.2100 = 21%
discount_percent    DECIMAL(5, 2)   -- e.g. 15.50
quantity            INT UNSIGNED
stock_quantity      INT UNSIGNED
sort_order          INT UNSIGNED    -- for manual ordering
view_count          INT UNSIGNED
rating              DECIMAL(3, 1)   -- e.g. 4.5

-- Geography
country_code        CHAR(2)         -- ISO 3166-1 alpha-2
currency_code       CHAR(3)         -- ISO 4217
language_code       VARCHAR(10)     -- BCP 47 (e.g. 'en-US')
timezone            VARCHAR(50)     -- e.g. 'America/New_York'
latitude            DECIMAL(10, 8)  -- -90 to 90
longitude           DECIMAL(11, 8)  -- -180 to 180
ip_address          VARCHAR(45)     -- supports IPv6
postal_code         VARCHAR(20)

-- Hashes & tokens
password_hash       VARCHAR(255)    -- bcrypt output
remember_token      VARCHAR(100)
api_key             VARCHAR(64)
verification_token  VARCHAR(100)
reset_token         VARCHAR(100)
session_token       VARCHAR(255)

-- Status & type (see Section 21)
status              VARCHAR(20) / ENUM
type                VARCHAR(50) / ENUM  -- avoid 'type' — use specific name
role                VARCHAR(30) / ENUM

-- Colors
color_hex           CHAR(7)         -- '#FF5733'
background_color    CHAR(7)

-- Files
file_name           VARCHAR(255)
file_path           VARCHAR(500)
file_size_bytes     BIGINT UNSIGNED
mime_type           VARCHAR(127)
file_extension      VARCHAR(10)
```

---

## 19. Boolean Columns

Use `TINYINT(1)` (MySQL standard) or `BOOLEAN` alias. Prefix with `is_`, `has_`, `can_`:

```sql
CREATE TABLE users
(
    id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    -- ✅ Boolean columns — TINYINT(1), prefix with is_/has_/can_
    is_active       TINYINT(1)      NOT NULL DEFAULT 1,
    is_verified     TINYINT(1)      NOT NULL DEFAULT 0,
    is_admin        TINYINT(1)      NOT NULL DEFAULT 0,
    is_suspended    TINYINT(1)      NOT NULL DEFAULT 0,
    has_newsletter  TINYINT(1)      NOT NULL DEFAULT 0,
    has_2fa         TINYINT(1)      NOT NULL DEFAULT 0,
    can_login       TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (id)
);


CREATE TABLE products
(
    id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    is_active       TINYINT(1)      NOT NULL DEFAULT 1,
    is_featured     TINYINT(1)      NOT NULL DEFAULT 0,
    is_digital      TINYINT(1)      NOT NULL DEFAULT 0,
    is_in_stock     TINYINT(1)      NOT NULL DEFAULT 1,
    requires_shipping TINYINT(1)    NOT NULL DEFAULT 1,
    PRIMARY KEY (id)
);


-- ❌ Bad boolean column names
active          -- no prefix
flag            -- meaningless
enabled         -- acceptable but less clear than is_enabled
verified        -- acceptable but less clear than is_verified
newsletter      -- sounds like a table name
```

---

## 20. Date & Time Columns

Use consistent suffixes:

```sql
-- ✅ Suffix patterns
created_at          DATETIME        -- when record was created
updated_at          DATETIME        -- when record was last modified
deleted_at          DATETIME        -- soft delete timestamp (NULL = not deleted)
published_at        DATETIME        -- when content went live
activated_at        DATETIME        -- when account activated
deactivated_at      DATETIME        -- when account deactivated
verified_at         DATETIME        -- when email/phone verified
email_verified_at   DATETIME        -- specific: which thing verified
expires_at          DATETIME        -- when something expires
expired_at          DATETIME        -- when it actually expired (past)
started_at          DATETIME        -- event start
ended_at            DATETIME        -- event end
completed_at        DATETIME        -- when task completed
cancelled_at        DATETIME        -- when cancelled
shipped_at          DATETIME        -- when order shipped
delivered_at        DATETIME        -- when order delivered
last_login_at       DATETIME        -- last user login
last_seen_at        DATETIME        -- last activity
scheduled_at        DATETIME        -- when scheduled to run
processed_at        DATETIME        -- when job was processed
failed_at           DATETIME        -- when failure occurred
reset_at            DATETIME        -- when password reset
locked_at           DATETIME        -- when account locked
unlocked_at         DATETIME        -- when account unlocked

-- ✅ Date-only (no time)
date_of_birth       DATE
start_date          DATE
end_date            DATE
due_date            DATE
hire_date           DATE
termination_date    DATE

-- ✅ Duration columns
duration_seconds    INT UNSIGNED
duration_minutes    INT UNSIGNED
response_time_ms    INT UNSIGNED
timeout_seconds     INT UNSIGNED

-- ❌ Bad
create_date         -- inconsistent (_date vs _at)
ts                  -- cryptic abbreviation for timestamp
timestamp           -- reserved word, ambiguous
date                -- reserved word, ambiguous
time                -- reserved word, ambiguous
```

---

## 21. Status & State Columns

Use `ENUM` for known, fixed values. Use `VARCHAR` for extensible status:

```sql
-- ✅ ENUM — when values are fixed and known at design time
CREATE TABLE orders
(
    id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    status  ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded')
            NOT NULL DEFAULT 'pending',
    PRIMARY KEY (id),
    INDEX idx_orders_status (status)
);


-- ✅ VARCHAR — when values may grow or come from config
CREATE TABLE notifications
(
    id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    type    VARCHAR(50)  NOT NULL,   -- 'email', 'sms', 'push', 'in_app'
    status  VARCHAR(20)  NOT NULL DEFAULT 'pending',  -- 'pending', 'sent', 'failed', 'read'
    PRIMARY KEY (id)
);


-- ✅ Status column naming — be specific, not generic
order_status        VARCHAR(20)     -- better than just 'status' in a table with multiple states
payment_status      VARCHAR(20)
shipment_status     VARCHAR(20)
verification_status VARCHAR(20)
approval_status     VARCHAR(20)
subscription_status VARCHAR(20)

-- ✅ Avoid 'type' alone — be specific
product_type        VARCHAR(50)     -- 'physical', 'digital', 'subscription'
user_type           VARCHAR(30)     -- 'individual', 'business', 'enterprise'
address_type        VARCHAR(20)     -- 'billing', 'shipping', 'both'
notification_type   VARCHAR(50)
transaction_type    VARCHAR(30)     -- 'purchase', 'refund', 'chargeback'
```

---

## 22. JSON Columns

```sql
CREATE TABLE products
(
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    name        VARCHAR(255)    NOT NULL,
    -- ✅ JSON column names — use plural or descriptive noun
    attributes  JSON,               -- flexible key-value attributes
    metadata    JSON,               -- system metadata
    settings    JSON,               -- configuration settings
    tags        JSON,               -- array of tags
    images      JSON,               -- array of image objects
    dimensions  JSON,               -- {width, height, depth, weight}
    options     JSON,               -- product variants/options
    extra_data  JSON,               -- catch-all extra data
    PRIMARY KEY (id)
);


-- ✅ JSON path queries — use descriptive path aliases
SELECT
    id,
    name,
    attributes->>'$.color'         AS color,
    attributes->>'$.material'      AS material,
    metadata->>'$.source'          AS data_source,
    JSON_EXTRACT(dimensions, '$.weight_kg') AS weight
FROM products
WHERE attributes->>'$.category' = 'electronics';
```

---

## 23. ORM Conventions

### Laravel Eloquent

```sql
-- Laravel expects:
-- Table: plural snake_case              → users, blog_posts, order_items
-- Primary key: 'id'                     → id INT AUTO_INCREMENT
-- Foreign key: singular_table_name_id   → user_id, order_id
-- Timestamps: created_at, updated_at    → DATETIME
-- Soft deletes: deleted_at              → DATETIME NULL

-- ✅ Laravel-compatible schema
CREATE TABLE users
(
    id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    name            VARCHAR(255)    NOT NULL,
    email           VARCHAR(255)    NOT NULL,
    password        VARCHAR(255)    NOT NULL,
    remember_token  VARCHAR(100),
    created_at      TIMESTAMP       NULL,
    updated_at      TIMESTAMP       NULL,
    deleted_at      TIMESTAMP       NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX uniq_users_email (email)
);

CREATE TABLE posts
(
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    user_id     INT UNSIGNED    NOT NULL,     -- FK to users.id
    title       VARCHAR(255)    NOT NULL,
    slug        VARCHAR(255)    NOT NULL,
    body        LONGTEXT        NOT NULL,
    published_at TIMESTAMP      NULL,
    created_at  TIMESTAMP       NULL,
    updated_at  TIMESTAMP       NULL,
    deleted_at  TIMESTAMP       NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX uniq_posts_slug (slug),
    INDEX idx_posts_user_id (user_id),
    CONSTRAINT fk_posts_user_id FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Django ORM

```sql
-- Django expects:
-- Table: appname_modelname (lowercase) → blog_post, auth_user
-- Primary key: 'id'                    → id INT AUTO_INCREMENT (or BigAutoField)
-- Foreign key: field_name + _id        → user_id, category_id
-- Many-to-many: app_model1_model2      → blog_post_tags

-- ✅ Django-compatible schema
CREATE TABLE blog_post
(
    id              INT             NOT NULL AUTO_INCREMENT,
    title           VARCHAR(200)    NOT NULL,
    slug            VARCHAR(200)    NOT NULL,
    body            LONGTEXT        NOT NULL,
    author_id       INT             NOT NULL,    -- FK to auth_user.id
    is_published    TINYINT(1)      NOT NULL DEFAULT 0,
    created_at      DATETIME(6)     NOT NULL,
    updated_at      DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX uniq_blog_post_slug (slug),
    INDEX idx_blog_post_author_id (author_id)
);
```

### SQLAlchemy

```sql
-- SQLAlchemy: flexible, follows what you define
-- Common convention: snake_case table and column names
-- Typically: plural tables, id PKs, tablename_id FKs

-- ✅ SQLAlchemy-friendly schema
CREATE TABLE users
(
    id              INT             NOT NULL AUTO_INCREMENT,
    username        VARCHAR(50)     NOT NULL,
    email           VARCHAR(255)    NOT NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE INDEX uniq_users_username (username),
    UNIQUE INDEX uniq_users_email (email)
);
```

---

## 24. Migrations

### File naming — timestamp prefix

```
-- ✅ Migration file naming (framework-agnostic)
2024_01_15_000001_create_users_table.sql
2024_01_15_000002_create_roles_table.sql
2024_01_16_000001_add_email_verified_at_to_users.sql
2024_01_20_000001_create_orders_table.sql
2024_02_01_000001_add_index_to_orders_status.sql
2024_02_10_000001_alter_products_add_weight_column.sql
2024_03_01_000001_drop_legacy_sessions_table.sql

-- ✅ Laravel migration class names (PascalCase)
CreateUsersTable
AddEmailVerifiedAtToUsers
CreateOrdersTable
AddIndexToOrdersStatus
AlterProductsAddWeightColumn
```

### Migration SQL patterns

```sql
-- ✅ CREATE TABLE migration
CREATE TABLE IF NOT EXISTS sessions
(
    id              VARCHAR(255)    NOT NULL,
    user_id         BIGINT UNSIGNED,
    ip_address      VARCHAR(45),
    user_agent      TEXT,
    payload         LONGTEXT        NOT NULL,
    last_activity   INT             NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_sessions_user_id (user_id),
    INDEX idx_sessions_last_activity (last_activity)
);

-- ✅ ADD COLUMN migration — always specify position
ALTER TABLE users
    ADD COLUMN phone_number     VARCHAR(20)     NULL AFTER email,
    ADD COLUMN date_of_birth    DATE            NULL AFTER phone_number,
    ADD COLUMN avatar_url       VARCHAR(500)    NULL AFTER date_of_birth;

-- ✅ ADD INDEX migration
ALTER TABLE orders
    ADD INDEX idx_orders_status_created_at (status, created_at);

-- ✅ RENAME COLUMN (MySQL 8.0+)
ALTER TABLE users
    RENAME COLUMN full_name TO display_name;

-- ✅ DROP TABLE with IF EXISTS
DROP TABLE IF EXISTS legacy_sessions;

-- ✅ Rollback / down migration
ALTER TABLE users
    DROP COLUMN phone_number,
    DROP COLUMN date_of_birth,
    DROP COLUMN avatar_url;
```

---

## 25. Naming Anti-patterns

### ❌ Reserved words as table/column names

```sql
-- These require backtick escaping — error-prone, confusing
CREATE TABLE `order` (...);      -- 'order' is reserved
CREATE TABLE `select` (...);     -- obviously bad
CREATE TABLE `group` (...);      -- reserved
CREATE TABLE `user` (...);       -- reserved in some contexts

SELECT `name`, `date`, `key`, `value`, `status`, `type` FROM `order`;

-- ✅ Avoid by being specific
CREATE TABLE orders (...);
CREATE TABLE users (...);

-- Columns
order_status    -- not 'status'
record_type     -- not 'type'
record_date     -- not 'date'
api_key         -- not 'key'
setting_value   -- not 'value'
```

### ❌ Hungarian notation / type encoding

```sql
-- ❌ Bad
int_user_id
str_first_name
dt_created_at
bool_is_active
txt_description
vc_email        -- varchar
```

### ❌ Inconsistent naming

```sql
-- ❌ Mixed conventions in one schema
CREATE TABLE Users (...);         -- PascalCase
CREATE TABLE blog_posts (...);    -- snake_case
CREATE TABLE orderItems (...);    -- camelCase

-- ❌ Mixed singular/plural
CREATE TABLE user (...);
CREATE TABLE orders (...);
CREATE TABLE product (...);
CREATE TABLE invoices (...);
```

### ❌ Generic column names

```sql
-- ❌ Vague, ambiguous names
name        -- whose name? What kind?
type        -- type of what?
status      -- status of what?
value       -- value of what?
data        -- data what?
info        -- info about what?
text        -- text of what?
num         -- number of what?
flag        -- flag for what?
misc        -- miscellaneous what?

-- ✅ Always prefix with context
user_name / product_name / category_name
order_status / payment_status / user_status
product_type / notification_type / user_type
tax_rate / discount_rate / exchange_rate
```

### ❌ Abbreviations

```sql
-- ❌ Cryptic abbreviations
usr_id          -- user_id
ord_dt          -- order_date
prod_nm         -- product_name
cust_addr       -- customer_address
qty             -- quantity (acceptable in very common domains)
amt             -- amount
prc             -- price
desc            -- description (also a SQL keyword!)
```

### ❌ Using FLOAT for money

```sql
-- ❌ Never use FLOAT or DOUBLE for monetary values
price   FLOAT,          -- floating point errors!
total   DOUBLE,         -- still has precision issues!

-- ✅ Always use DECIMAL
price   DECIMAL(10, 2),
total   DECIMAL(15, 2),
rate    DECIMAL(5, 4),
```

---

## 26. Quick Reference Cheatsheet

| Object | Convention | Example |
|--------|-----------|---------|
| Database | snake_case | `ecommerce`, `user_management` |
| Table | plural snake_case | `users`, `order_items`, `blog_posts` |
| Column | snake_case | `first_name`, `created_at` |
| Primary key | `id` or `table_id` | `id`, `user_id` |
| Foreign key column | `singular_table_id` | `user_id`, `order_id` |
| FK with context | `context_singular_table_id` | `billing_address_id` |
| FK constraint | `fk_{table}_{column}` | `fk_orders_user_id` |
| Regular index | `idx_{table}_{col(s)}` | `idx_users_email` |
| Unique index | `uniq_{table}_{col(s)}` | `uniq_users_email` |
| Full-text index | `ft_{table}_{col(s)}` | `ft_posts_content` |
| CHECK constraint | `chk_{table}_{column}` | `chk_products_price_positive` |
| UNIQUE constraint | `uniq_{table}_{col(s)}` | `uniq_users_email` |
| View | `v_{name}` or `vw_{name}` | `v_active_users` |
| Stored procedure | `sp_{verb}_{noun}` | `sp_create_order` |
| Function | `fn_{verb}_{noun}` | `fn_get_full_name` |
| Trigger | `trg_{table}_{timing}_{event}` | `trg_users_before_insert` |
| Event | `evt_{action}_{subject}` | `evt_cleanup_expired_sessions` |
| Temp table | `tmp_{name}` | `tmp_active_users` |
| Junction table | `singular1_singular2` | `category_product`, `role_user` |
| Audit table | `{name}_log(s)` or `{name}_history` | `audit_logs`, `price_history` |
| SP parameter | `p_{name}` | `p_user_id`, `p_result` |
| Boolean column | `is_/has_/can_` + noun | `is_active`, `has_newsletter` |
| Timestamp column | noun + `_at` | `created_at`, `deleted_at`, `verified_at` |
| Date column | noun + `_date` | `start_date`, `due_date` |
| Money column | DECIMAL, descriptive | `total_amount`, `unit_price` |
| Status column | specific + `_status` | `order_status`, `payment_status` |
| Migration file | `YYYY_MM_DD_NNNNNN_description` | `2024_01_15_000001_create_users_table` |

---

## 27. References & Further Reading

| Resource | URL |
|----------|-----|
| **MySQL 8.0 Reference Manual** | https://dev.mysql.com/doc/refman/8.0/en/ |
| **MySQL Identifier Names** | https://dev.mysql.com/doc/refman/8.0/en/identifiers.html |
| **MySQL Reserved Words** | https://dev.mysql.com/doc/refman/8.0/en/reserved-words.html |
| **SQL Style Guide (Simon Holywell)** | https://www.sqlstyle.guide |
| **PostgreSQL Naming Conventions** | https://wiki.postgresql.org/wiki/Don't_Do_This |
| **Laravel Database Conventions** | https://laravel.com/docs/eloquent#eloquent-model-conventions |
| **Django Database Notes** | https://docs.djangoproject.com/en/stable/ref/databases/ |
| **SQLAlchemy ORM** | https://docs.sqlalchemy.org/en/20/orm/ |
| **Vertabelo Naming Blog** | https://vertabelo.com/blog/database-naming-conventions/ |
| **ISO SQL Standard** | ISO/IEC 9075 |

### Recommended linting tools

```sql
-- SQLFluff — SQL linter and formatter
-- Install: pip install sqlfluff
-- Config: .sqlfluff

[sqlfluff]
dialect = mysql
templater = raw
max_line_length = 120

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper      -- SELECT, FROM, WHERE in uppercase

[sqlfluff:rules:capitalisation.identifiers]
capitalisation_policy = lower      -- table/column names in lowercase

[sqlfluff:rules:aliasing.table]
aliasing = explicit                -- always name aliases explicitly

[sqlfluff:rules:convention.terminator]
multiline_newline = true
```

```sql
-- ✅ Formatting example — keywords UPPERCASE, identifiers lowercase
SELECT
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    COUNT(o.id)         AS order_count,
    SUM(o.total_amount) AS total_spent
FROM users AS u
LEFT JOIN orders AS o
    ON o.user_id = u.id
   AND o.status = 'completed'
WHERE u.is_active = 1
  AND u.deleted_at IS NULL
GROUP BY u.id, u.first_name, u.last_name, u.email
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC
LIMIT 100;
```

---

*Last updated: 2026 — Based on MySQL 8.0/8.4, Laravel 11, Django 5.x, SQLAlchemy 2.0*
