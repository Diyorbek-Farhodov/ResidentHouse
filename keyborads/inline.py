from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from mock_data import REGIONS, EMPLOYEES_DISTRICT


def auth_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kod bilan", callback_data="auth_code")],
        [InlineKeyboardButton(text="Telefon raqam bilan", callback_data="auth_phone")]
    ])

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" Yangi Uy", callback_data="add_house")],
        [InlineKeyboardButton(text=" Mening tumanlarim", callback_data="my_districts")],
        [InlineKeyboardButton(text=" Yashovchi qo‘shish", callback_data="add_resident")],
        [InlineKeyboardButton(text=" Uy qidiruvi", callback_data="search_house")]
    ])


def region_keyboard():
    kb = InlineKeyboardMarkup(row_width = 2)
    for region in REGIONS.keys():
        kb.add(InlineKeyboardButton(text=region, callback_data=f"region:{region}"))
    return kb


def district_keyboard(region_name):
    kb = InlineKeyboardMarkup(row_width = 2)
    for district in REGIONS.get(region_name, []):
        kb.add(InlineKeyboardButton(text=district, callback_data=f"district:{district}"))
    return kb


def confirm_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Malumotlarni kiriting", callback_data="write_data"))
    return kb


def employee_district_kb(districts: list) -> InlineKeyboardMarkup:
    keyboard = []
    for district in districts:
        if isinstance(district, str):
            keyboard.append(
                [InlineKeyboardButton(text=district, callback_data=f"select_dist:{district}")]
            )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def search_house_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=" Tuman bo'yicha", callback_data="search_by_district"),
    )
    builder.row(
        InlineKeyboardButton(text="Uy raqami bo'yicha", callback_data="search_by_number"),
    )
    builder.row(
        InlineKeyboardButton(text=" Egasi tel. bo'yicha", callback_data="search_by_owner_phone"),
    )
    return builder.as_markup()