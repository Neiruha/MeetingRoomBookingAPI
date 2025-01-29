# Booking Room Demo

**Booking Room Demo** is an API server for managing meeting room bookings using JSON files for storing data. The project includes functionality for working with users, rooms, participants and automatic notification of bookings.

## 📄 Warning

The project is freely distributed with an "as-is" license. This is only a demo, the simplest implementation. I can make your project completely turnkey.

FeelMusic (Neiruha)

## 🛠 Tech stack

- **Python** (3.10+)
- **FastAPI** — for API
- **Pytest** — for tests
- **JSON** — for storing data
- **Git** — for version control

---

## 📂 Project structure

```plaintext
. ├── app/
│ ├── __init__.py # Empty file to denote the module
│ ├── database.py # Main logic for working with bookings and users
│ └── main.py # Entry point for FastAPI
│
├── data/ # Folder for storing data (JSON files)
│ ├── users.json # User database
│ └── YYYY-MM-DD.json # Files with bookings by day
│
├── tests/ # Folder for tests
│ ├── __init__.py # Empty file to denote the module
│ └── test_database.py # Tests for database.py
│
├── generate_test_bookings.py # Script for generating test bookings
├── requirements.txt # Project dependencies
├── .gitignore # Exceptions for Git
├── pytest.ini # Configuration for pytest
└── README.md # Project description

```

## ⚙️ Installation and setup

1. **Clone the repository:**

```bash
git clone https://github.com/username/booking-system.git
cd booking-system
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## 🚀 Run project

1. **Running the application (FastAPI):**

```bash
python app/main.py
```
The application will be available at: http://127.0.0.1:8000

2. **Generating test data: To create test bookings, use:**

```bash
python generate_test_bookings.py
```

## 🧪 Testing

1. **Running all tests:**

```bash
Edit
pytest tests/
```

2. **Checking a specific test:**

```bash
pytest tests/test_database.py
```

## 📚 Example of API usage

### Adding a booking

**Request:**
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

**Answer:**

```json
{
 "id": "501202501170900",
 "room_id": "501",
 "date": "2025-01-17",
 "start_time": "09:00",
 "end_time": "10:00",
 "booked_by": 101,
 "participants": [
 { "id": 103, "name": "Marina" },
{ "id": 104, "name": "Olga" }
],
"status": "confirmed",
"comment": "Important meeting",
"guests": []
}
```

## 🗃 Data format

### `users.json`

```json
{
"101": {
"name": "Petr",
"nickname": "Petya"
},
"102": {
"name": "Vasya",
"nickname": "Vaska"
}
}

```

### Booking in `YYYY-MM-DD.json`

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
{ "id": 103, "name": "Marina" },
 { "id": 104, "name": "Olga" }
 ],
 "status": "confirmed",
 "comment": "Important meeting",
 "guests": []
 }
]

```
