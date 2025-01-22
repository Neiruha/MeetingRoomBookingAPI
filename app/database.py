import json
import os
from datetime import date, datetime, time, timedelta
from typing import List, Dict, Optional
import logging
from threading import Lock

# --- Инициализация ---
DATA_FOLDER = "./data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
ROOMS_FILE = os.path.join(DATA_FOLDER, "rooms.json")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Блокировки для работы с файлами
file_locks = {}

def get_file_lock(file_path: str) -> Lock:
    """Получить блокировку для файла."""
    if file_path not in file_locks:
        file_locks[file_path] = Lock()
    return file_locks[file_path]

# --- Установка папки данных ---
def set_data_folder(folder_path: str):
    """Установить путь для папки данных."""
    global DATA_FOLDER, USERS_FILE, ROOMS_FILE
    DATA_FOLDER = os.path.abspath(folder_path)
    USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
    ROOMS_FILE = os.path.join(DATA_FOLDER, "rooms.json")
    os.makedirs(DATA_FOLDER, exist_ok=True)
    logger.info(f"Data folder set to: {DATA_FOLDER}")


def read_json(file_path: str) -> any:
    lock = get_file_lock(file_path)
    logger.debug(f"Попытка чтения файла {file_path}")
    with lock:
        logger.debug(f"Файл {file_path} успешно открыт для чтения")
        if not os.path.exists(file_path):
            return [] if file_path.endswith(".json") else {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON {file_path}: {e}")
            return [] if file_path.endswith(".json") else {}


def write_json(file_path: str, data: List[Dict]):
    lock = get_file_lock(file_path)
    logger.debug(f"Попытка записи в файл {file_path}")
    with lock:
        logger.debug(f"Файл {file_path} успешно открыт для записи")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Ошибка записи файла {file_path}: {e}")


# --- Работа с комнатами ---
def load_rooms() -> List[Dict]:
    """Загрузить список переговорных."""
    return read_json(ROOMS_FILE)


def save_rooms(rooms: List[Dict]):
    """Сохранить список переговорных."""
    room_ids = [room['id'] for room in rooms]
    if len(room_ids) != len(set(room_ids)):
        raise ValueError("Duplicate room IDs found in the rooms list.")
    write_json(ROOMS_FILE, rooms)


# --- Работа с пользователями ---
def load_users() -> Dict[str, Dict[str, str]]:
    """Загрузить базу пользователей. Возвращает словарь."""
    users = read_json(USERS_FILE)
    if not isinstance(users, dict):  # Если файл пустой или формат неверный
        users = {}
    return users

def save_users(users: Dict[str, Dict[str, str]]):
    # Добавляем вывод перед записью
    print(f"Saving users: {users}")  
    """Сохранить базу пользователей."""
    write_json(USERS_FILE, users)


def add_user(user_id: int, name: str, nickname: str = ""):
    """
    Добавить пользователя в базу.
    """
    users = load_users()
    user_id_str = str(user_id)
    if user_id_str in users:
        logger.info(f"User with ID {user_id} already exists.")
    else:
        users[user_id_str] = {"name": name, "nickname": nickname}
        logger.info(f"Adding user: {users[user_id_str]}")
        save_users(users)
        logger.info(f"User {name} added to the database. Current users: {users}")


# --- Работа с бронированиями ---
def get_file_path(target_date: date) -> str:
    """Получить путь к файлу бронирований для даты."""
    return os.path.join(DATA_FOLDER, f"{target_date.strftime('%Y-%m-%d')}.json")


def read_bookings(target_date: date) -> List[Dict]:
    """Прочитать бронирования из JSON-файла. Если файл пуст, вернуть пустой список."""
    bookings = read_json(get_file_path(target_date))
    if not isinstance(bookings, list):  # Если файл содержит что-то кроме списка
        bookings = []

    # Преобразование booked_by в объект Participant
    users = load_users()
    for booking in bookings:
        if isinstance(booking["booked_by"], str):  # Если booked_by — строка (ID пользователя)
            user_info = users.get(booking["booked_by"])
            if user_info:
                booking["booked_by"] = {
                    "id": booking["booked_by"],
                    "name": user_info["name"]
                }

    return bookings


def write_bookings(target_date: date, bookings: List[Dict]):
    """Записать бронирования в JSON-файл."""
    write_json(get_file_path(target_date), bookings)

def process_participants(participants: List, users: Dict) -> (List, List):
    """Обработать участников, разделив их на известных и гостей."""
    known = []
    guests = []
    for participant in participants:
        if isinstance(participant, int):  # Указан ID
            user_info = users.get(str(participant))  # Приведение ID к строке
            if user_info:
                known.append({"id": participant, "name": user_info["name"]})
            else:
                guests.append(f"Unknown ID: {participant}")
        else:
            guests.append(participant)
    logger.debug(f"Processed participants: {len(known)} known, {len(guests)} guests.")
    return known, guests


def create_booking(booking: Dict) -> Dict:
    """Создать новое бронирование."""
    target_date = date.fromisoformat(booking["date"])
    users = load_users()

    # Проверка уникальности ID
    bookings = read_bookings(target_date)
    if not isinstance(bookings, list):
        raise TypeError(f"Expected bookings to be a list, got {type(bookings)}")
    if any(b["id"] == booking["id"] for b in bookings):
        logger.error(f"Booking with ID {booking['id']} already exists.")
        raise ValueError(f"Booking with ID {booking['id']} already exists.")

    # Преобразуем `booked_by` в объект
    if isinstance(booking["booked_by"], str):  # Если это ID пользователя
        user_info = users.get(booking["booked_by"])
        if not user_info:
            raise ValueError(f"User with ID {booking['booked_by']} not found in the database.")
        booking["booked_by"] = {"id": booking["booked_by"], "name": user_info["name"]}

    # Обработка участников
    participants, guests = process_participants(booking["participants"], users)

    # Проверка наличия участников
    if not participants and not guests:
        logger.error("No participants provided for the booking.")
        raise ValueError("No participants provided for the booking.")

    # Сохраняем бронирование
    booking["participants"] = participants
    booking["guests"] = guests
    bookings.append(booking)
    write_bookings(target_date, bookings)

    logger.info(f"Booking {booking['id']} created successfully.")
    return booking


def validate_time(value):
    """Убедиться, что значение — объект time."""
    if not isinstance(value, time):
        raise ValueError(f"Expected time object, got {type(value)}")


def check_room_availability(target_date: date, room_id: str, start_time: time, end_time: time) -> bool:
    validate_time(start_time)
    validate_time(end_time)

    bookings = read_bookings(target_date)
    logger.info(f"Checking room {room_id} availability on {target_date} from {start_time} to {end_time}")

    for booking in bookings:
        if booking["room_id"] == room_id:
            existing_start = datetime.strptime(booking["start_time"], "%H:%M").time()
            existing_end = datetime.strptime(booking["end_time"], "%H:%M").time()

            if start_time < existing_end and end_time > existing_start:
                logger.info(
                    f"Room {room_id} is not available: existing booking from {existing_start} to {existing_end}, ID: {booking['id']}"
                )
                return False
    logger.info(f"Room {room_id} is available.")
    return True


def delete_booking(target_date: date, booking_id: str) -> bool:
    """Удалить бронирование по ID."""
    bookings = read_bookings(target_date)
    updated_bookings = [b for b in bookings if b["id"] != booking_id]
    if len(bookings) == len(updated_bookings):
        return False  # Ничего не удалили
    write_bookings(target_date, updated_bookings)
    return True


def get_booking(target_date: date, booking_id: str) -> Optional[Dict]:
    """Получить бронирование по ID."""
    bookings = read_bookings(target_date)
    for booking in bookings:
        if booking["id"] == booking_id:
            return booking
    return None


def get_user_bookings(user_id: str, start_date: date, end_date: date) -> List[Dict]:
    """Получить все бронирования для пользователя за указанный период."""
    result = []
    current_date = start_date
    while current_date <= end_date:
        bookings = read_bookings(current_date)
        user_bookings = [b for b in bookings if b.get("booked_by") == user_id]
        result.extend(user_bookings)
        current_date += timedelta(days=1)
    return result


def get_bookings_in_range(
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    rooms: Optional[List[str]] = None
) -> List[Dict]:
    """
    Получить все бронирования из всех файлов в папке `data`,
    с фильтрацией по дате и комнатам.
    """
    result = []
    for file_name in os.listdir(DATA_FOLDER):
        # Пропускаем служебные файлы
        if file_name in ["rooms.json", "users.json"]:
            continue
        
        # Проверяем формат файла (YYYY-MM-DD.json)
        try:
            file_date = date.fromisoformat(file_name.replace(".json", ""))
        except ValueError:
            logger.warning(f"Пропущен файл с некорректным форматом: {file_name}")
            continue

        # Фильтруем по дате
        if start_date and file_date < start_date:
            continue
        if end_date and file_date > end_date:
            continue

        # Читаем бронирования из файла
        bookings = read_json(os.path.join(DATA_FOLDER, file_name))
        if not isinstance(bookings, list):
            logger.warning(f"Файл {file_name} не содержит списка бронирований, пропущен")
            continue

        # Фильтруем по комнатам
        if rooms:
            bookings = [b for b in bookings if b["room_id"] in rooms]

        result.extend(bookings)

    return result
