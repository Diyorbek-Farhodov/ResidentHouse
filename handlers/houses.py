
from json_handler import add_user_data, search_by_owner_phone
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from mock_data import user_session
from states import HouseInfoState

router = Router()




@router.callback_query(F.data.startswith("select_dist:"))
async def district_selected(callback: CallbackQuery, state: FSMContext):
    district = callback.data.split(":")[1]
    await state.update_data(district=district)
    await callback.message.answer("Mahallani kiriting:")
    await state.set_state(HouseInfoState.waiting_for_mahalla)



@router.message(HouseInfoState.waiting_for_mahalla)
async def process_mahalla(message: Message, state: FSMContext):
    await state.update_data(mahalla=message.text)
    await message.answer("Ko'chani kiriting:")
    await state.set_state(HouseInfoState.waiting_for_street)


@router.message(HouseInfoState.waiting_for_street)
async def process_street(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("Qishloqni kiriting (agar yo‘q bo‘lsa, 'yo‘q' deb yozing):")
    await state.set_state(HouseInfoState.waiting_for_qishloq)



@router.message(HouseInfoState.waiting_for_qishloq)
async def process_qishloq(message: Message, state: FSMContext):
    await state.update_data(qishloq=message.text)
    await message.answer("Uy raqamini kiriting:")
    await state.set_state(HouseInfoState.waiting_for_home_number)



@router.message(HouseInfoState.waiting_for_home_number)
async def process_home_number(message: Message, state: FSMContext):
    await state.update_data(home_number=message.text)
    await message.answer("Uy egasining ismini kiriting:")
    await state.set_state(HouseInfoState.waiting_for_owner_name)



@router.message(HouseInfoState.waiting_for_owner_name)
async def process_owner_name(message: Message, state: FSMContext):
    await state.update_data(owner_name=message.text)
    await message.answer("Uy egasining telefon raqamini kiriting:")
    await state.set_state(HouseInfoState.waiting_for_owner_phone)


@router.message(HouseInfoState.waiting_for_owner_phone)
async def process_owner_phone(message: Message, state: FSMContext):
    await state.update_data(owner_phone=message.text)
    data = await state.get_data()

    user = user_session.get(message.from_user.id)
    if not user:
        await message.answer("Xatolik: Sessiya ma'lumotlari topilmadi. Qaytadan kirishingiz kerak.")
        await state.clear()
        return

    employee_code = user.get("code")
    employee_name = user.get("name")
    employee_phone = user.get("phone")

    house_data = {
        "district": data.get("district"),
        "mahalla": data.get("mahalla"),
        "street": data.get("street"),
        "qishloq": data.get("qishloq"),
        "home_number": data.get("home_number"),
        "owner_name": data.get("owner_name"),
        "owner_phone": data.get("owner_phone")
    }

    add_user_data(
        employee_code=employee_code,
        employee_name=employee_name,
        employee_phone=employee_phone,
        new_data=house_data
    )

    summary = (
        f"<b>Yangi ma'lumotlar:</b>\n"
        f"Xodim: {employee_name} ({employee_code})\n"
        f"Tuman: {house_data.get('district')}\n"
        f"Mahalla: {house_data.get('mahalla')}\n"
        f"Ko'cha: {house_data.get('street')}\n"
        f"Qishloq: {house_data.get('qishloq')}\n"
        f"Uy raqami: {house_data.get('home_number')}\n"
        f"Uy egasi: {house_data.get('owner_name')}\n"
        f"Telefon: {house_data.get('owner_phone')}"
    )

    await message.answer(summary)
    await message.answer("✅ Ma'lumotlaringiz saqlandi.")
    await state.clear()

# _________________________________________________________________________________________________________________
# Uy qidiruvi uchun


@router.callback_query(F.data == 'search_house')
async def start_phone_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        " Uy egasining telefon raqamini kiriting (+998XXXXXXXXX formatida):"
    )
    await state.set_state(HouseInfoState.waiting_for_search_owner_phone)


@router.message(HouseInfoState.waiting_for_search_owner_phone)
async def process_phone_search(message: Message, state: FSMContext):
    phone = message.text.strip()

    if not (phone.startswith('+998') and len(phone) == 13 and phone[1:].isdigit()):
        await message.answer("❌ Noto'g'ri format. Iltimos, +998XXXXXXXXX ko'rinishida kiriting")
        return

    results = search_by_owner_phone(phone)
    await show_search_results(message, results, state)


async def show_search_results(message: Message, results: list[dict], state: FSMContext):
    if not results:
        await message.answer("❌ Hech qanday natija topilmadi")
    else:
        for result in results:
            employee_name = result.get("employee_name", "Nomaʼlum xodim")
            house_data = result.get("house_data", {})

            response = (
                "🔍 <b>Qidiruv natijasi:</b>\n\n"
                f" <b>Xodim:</b> {employee_name}\n"
                f" <b>Tuman:</b> {house_data.get('district', 'Nomaʼlum')}\n"
                f" <b>Mahalla:</b> {house_data.get('mahalla', 'Nomaʼlum')}\n"
                f" <b>Ko'cha:</b> {house_data.get('street', 'Nomaʼlum')}\n"
                f" <b>Qishloq:</b> {house_data.get('qishloq', 'Nomaʼlum')}\n"
                f" <b>Uy raqami:</b> {house_data.get('home_number', 'Nomaʼlum')}\n"
                f" <b>Uy egasi:</b> {house_data.get('owner_name', 'Nomaʼlum')}\n"
                f"ire"
                f" <b>Telefon:</b> {house_data.get('owner_phone', 'Nomaʼlum')}"
            )

            await message.answer(response, parse_mode="HTML")

    await state.clear()