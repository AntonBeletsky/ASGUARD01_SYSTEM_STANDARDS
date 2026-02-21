# Краткий отчёт: W3C валидаторы + ESLint

---

## 1. Nu Html Checker (HTML валидатор)

**Официальный HTML5 валидатор от W3C**

- **Сайт:** https://validator.w3.org/nu/
- **GitHub:** https://github.com/validator/validator
- **Лицензия:** MIT

### Установка (локально через Docker)
```bash
docker run -it --rm -p 8888:8888 ghcr.io/validator/validator:latest
```

### Использование

**Через браузер:** http://localhost:8888

**Через API (JSON):**
```bash
curl -H "Content-Type: text/html; charset=utf-8" \
     --data-binary @myfile.html \
     "http://localhost:8888/?out=json"
```

**Или публичный API:**
```bash
curl "https://validator.w3.org/nu/?doc=https://example.com&out=json"
```

---

## 2. W3C CSS Validator

**Официальный CSS валидатор от W3C**

- **Сайт:** https://jigsaw.w3.org/css-validator/
- **GitHub:** https://github.com/w3c/css-validator
- **Лицензия:** W3C Software License

### Установка (локально через Java)
```bash
# Требуется Java 8+
git clone https://github.com/w3c/css-validator
cd css-validator
ant jar
java -jar css-validator.jar https://example.com
```

### Использование

**Через публичный API:**
```bash
curl "https://jigsaw.w3.org/css-validator/validator?uri=https://example.com&output=json"
```

**Прямая отправка CSS:**
```bash
curl -X POST "https://jigsaw.w3.org/css-validator/validator" \
     -F "text=body { color: red }" \
     -F "output=json"
```

---

## 3. ESLint (JavaScript линтер)

**Стандарт де-факто для линтинга JS/TS кода**

- **Сайт:** https://eslint.org/
- **GitHub:** https://github.com/eslint/eslint
- **Лицензия:** MIT

### Установка
```bash
npm install eslint --save-dev
```

### Инициализация (генерирует конфиг)
```bash
npx eslint --init
```

### Использование
```bash
# Проверить папку
npx eslint ./src

# Проверить конкретный файл
npx eslint app.js

# Автоматически исправить что можно
npx eslint ./src --fix

# Вывод в JSON
npx eslint ./src --format json
```

### Минимальный конфиг (eslint.config.js)
```javascript
export default [
  {
    rules: {
      "no-unused-vars": "warn",
      "no-console": "warn",
      "semi": ["error", "always"]
    }
  }
];
```

---

## Сравнительная таблица

| Инструмент      | Что проверяет | Язык  | Локально | Онлайн API |
|----------------|--------------|-------|----------|------------|
| Nu Html Checker | HTML         | Java  | Docker   | ✅          |
| CSS Validator   | CSS          | Java  | Сложнее  | ✅          |
| ESLint          | JS / TS      | Node  | ✅ npm    | ❌          |
