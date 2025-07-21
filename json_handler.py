import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

DATA_FILE = Path("user_data.json")

def load_data() -> dict:
    try:
        if not DATA_FILE.exists():
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)
            return {}

        with open(DATA_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Malumotlarni yuklashda xatolik: {e}")
        return {}


def save_data(data: dict):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ma'lumotlarni saqlashda xatolik: {e}")


def add_user_data(employee_code: str, employee_name: str, employee_phone: str, new_data: dict):
    try:
        data = load_data()

        record = {
            "timestamp": datetime.now().isoformat(),
            "employee_code": employee_code,
            "employee_name": employee_name,
            "employee_phone": employee_phone,
            "house_data": new_data
        }

        if employee_code in data:
            data[employee_code].append(record)
        else:
            data[employee_code] = [record]

        save_data(data)
        return True
    except Exception as e:
        print(f"Ma'lumot qo'shishda xatolik: {e}")
        return False

def clear_data():
    try:
        with open(DATA_FILE, "w", encoding='utf-8') as f:
            json.dump({}, f)
        print("Malumotlar tozalandi")
    except Exception as e:
        print(f"Malumotlarni tozalashda xatolik {e}")



