# Booking Room Demo

**Booking Room Demo** — это API - сервер для управления бронированиями переговорных комнат с использованием JSON-файлов для хранения данных. Проект включает функционал работы с пользователями, комнатами, участниками и автоматическое уведомление о бронированиях.

## 📄 Warning

Проект распространяется свободно с лицензией "как-есть". Это только демо, простейшая реализация. Я могу сделать Ваш проект полностью под ключ.

FeelMusic (Neiruha)


## 🛠 Стек технологий

- **Python** (3.10+)
- **FastAPI** — для API
- **Pytest** — для тестов
- **JSON** — для хранения данных
- **Git** — для контроля версий

---

## 📂 Структура проекта

```plaintext
.
├── app/
│   ├── __init__.py          # Пустой файл для обозначения модуля
│   ├── database.py          # Основная логика работы с бронированиями и пользователями
│   └── main.py              # Точка входа для FastAPI
│
├── data/                    # Папка для хранения данных (JSON-файлы)
│   ├── users.json           # База данных пользователей
│   └── YYYY-MM-DD.json      # Файлы с бронированиями по дням
│
├── tests/                   # Папка для тестов
│   ├── __init__.py          # Пустой файл для обозначения модуля
│   └── test_database.py     # Тесты для database.py
│
├── generate_test_bookings.py # Скрипт для генерации тестовых бронирований
├── requirements.txt         # Зависимости проекта
├── .gitignore               # Исключения для Git
├── pytest.ini               # Конфигурация для pytest
└── README.md                # Описание проекта

```

## ⚙️ Установка и настройка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/username/booking-system.git
cd booking-system
```
	
2. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

## 🚀 Запуск проекта


1. **Запуск приложения (FastAPI):**

```bash
python app/main.py
```
Приложение будет доступно по адресу: http://127.0.0.1:8000


2. **Генерация тестовых данных: Для создания тестовых бронирований используйте:**

```bash
python generate_test_bookings.py
```

## 🧪 Тестирование

1. **Запуск всех тестов:**

```bash
Редактировать
pytest tests/
```

2. **Проверка конкретного теста:**

```bash
pytest tests/test_database.py
```

## 📚 Пример использования API

### Добавление бронирования

**Запрос:**  
`POST /bookings/`

```json

{
    "id": "501202501170900",
    "room_id": "501",
    "date": "2025-01-17",
    "start_time": "09:00",
    "end_time": "10:00",
    "booked_by": 101,
    "participants": [103, 104],
    "status": "confirmed",
    "comment": "Important meeting"
}

```

**Ответ:**

```json
{
    "id": "501202501170900",
    "room_id": "501",
    "date": "2025-01-17",
    "start_time": "09:00",
    "end_time": "10:00",
    "booked_by": 101,
    "participants": [
        { "id": 103, "name": "Марина" },
        { "id": 104, "name": "Ольга" }
    ],
    "status": "confirmed",
    "comment": "Important meeting",
    "guests": []
}

```

---

## 🗃 Формат данных

### `users.json`

```json
{
    "101": {
        "name": "Петр",
        "nickname": "Петя"
    },
    "102": {
        "name": "Вася",
        "nickname": "Васька"
    }
}

```

### Бронирование в `YYYY-MM-DD.json`

```json
[
    {
        "id": "501202501170900",
        "room_id": "501",
        "date": "2025-01-17",
        "start_time": "09:00",
        "end_time": "10:00",
        "booked_by": 101,
        "participants": [
            { "id": 103, "name": "Марина" },
            { "id": 104, "name": "Ольга" }
        ],
        "status": "confirmed",
        "comment": "Important meeting",
        "guests": []
    }
]

```

---

