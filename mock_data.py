EMPLOYEES = {
    "EMP001":{
        "name": "Diyorbek Farhodov",
        "phone": "+998948670779",
        "code": "123"
    },
    "EMP002": {
        "name": "Sarvarbek Farhodov",
        "phone": "+998942577788",
        "code": "567"
    },
}

def check_employee_code(code: str) -> dict  | None:
    for emp_id, emp in EMPLOYEES.items():
        if emp['code'] == code:
            return {**emp, 'id':emp_id}
    return None


def check_employee_phone(phone: str) -> dict | None:
    for emp_id, emp in EMPLOYEES.items():
        if emp['phone'] == phone:
            return {**emp, "id": emp_id}
    return None



REGIONS = {
    "Navoiy": ["Xatirchi", "Nuroto", "Navoiy shahri"],
    "Toshkent": ["Olmazor", "Yunusobot"],
    "Samarqand": ["Urgut", "Narpay"]
}


EMPLOYEES_DISTRICT = {
    "123": ["Xatirchi", "Nuroto"],
    "567": ["Narpay", "Urgut"]
}

user_session = {}

def get_region_by_district(district_name: str) -> str| None:
    for region , district in REGIONS.items():
        if district_name in district:
            return region
    return None


def get_district_by_region(region: str) -> list[str]:
    return REGIONS.get(region, [])


def get_all_regions() -> list[str]:
    return list(REGIONS.keys())