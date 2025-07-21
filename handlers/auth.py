from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import List, Dict

from keyborads.inline import auth_kb, main_menu_kb, employee_district_kb, region_keyboard
from mock_data import check_employee_code, check_employee_phone, EMPLOYEES_DISTRICT, user_session, EMPLOYEES
from states import AuthState

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum! Kirish usulini tanlang:",
        reply_markup=auth_kb()
    )


@router.callback_query(F.data == "auth_code")
async def auth_code(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AuthState.waiting_code)
    await callback.message.edit_text("Xodim kodingizni kiriting: ")

@router.callback_query(F.data == "auth_phone")
async def auth_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AuthState.waiting_phone)
    await callback.message.edit_text("Xodim Telefon raqamingizni kiriting: ")


@router.message(AuthState.waiting_code)
async def process_code(message: Message, state: FSMContext):
    emp = check_employee_code(message.text)
    if emp:
        user_session[message.from_user.id] = {
            "code": emp["code"],
            "name": emp["name"],
            "phone": emp["phone"]
        }
        await state.clear()
        await message.answer(
            f"Xush kelibsiz, {emp['name']}!",
            reply_markup=main_menu_kb()
        )
    else:
        await message.answer("Noto'g'ri kod. Qaytadan urinib ko'ring")


@router.message(AuthState.waiting_phone)
async def process_phone_number(message: Message, state: FSMContext):
    phone_number = message.text.strip()


    if not (phone_number.startswith('+998') and len(phone_number) == 13 and phone_number[1:].isdigit()):
        await message.answer("Iltimos, telefon raqamni to'g'ri formatda kiriting (+998XXXXXXXXX)")
        return

    emp = check_employee_phone(phone_number)
    if not emp:
        await message.answer("Ushbu raqam ro'yxatdan o'tmagan. Iltimos, admin bilan bog'laning.")
        return


    user_session[message.from_user.id] = {
        "code": emp["code"],
        "name": emp["name"],
        "phone": phone_number
    }

    await state.clear()
    await message.answer(
        f"Xush kelibsiz, {emp['name']}!",
        reply_markup=main_menu_kb()
    )



@router.callback_query(F.data == 'add_house')
async def show_districts(callback: CallbackQuery):
    user = user_session.get(callback.from_user.id)
    if not user:
        await callback.message.edit_text("Avval tizimga kiring")
        return

    employee_code = user.get("code")
    assigned_districts = EMPLOYEES_DISTRICT.get(employee_code, [])

    if not assigned_districts:
        await callback.message.edit_text("Sizga hech qanday tuman biriktirilmagan")
        return

    await callback.message.edit_text(
        "Quyidagi tumanlardan birini tanlang:",
        reply_markup=employee_district_kb(assigned_districts)
    )


async def show_search_results(message: Message, results: List[Dict], state: FSMContext):
    if not results:
        await message.answer("❌ Hech qanday natija topilmadi")
    else:
        response = ["🔍 Qidiruv natijalari:\n"]
        for result in results:
            house = result.get("house_data", {})
            response.append(
                f" Tuman: {house.get('district', 'Nomaʼlum')}\n"
                f" Ko'cha: {house.get('street', 'Nomaʼlum')}\n"
                f" Uy raqami: {house.get('home_number', 'Nomaʼlum')}\n"
                f" Egasi: {house.get('owner_name', 'Nomaʼlum')}\n"
                f" Telefon: {house.get('owner_phone', 'Nomaʼlum')}\n"
                "―――――――――――――――――――"
            )
        await message.answer("\n".join(response))

    await state.clear()


