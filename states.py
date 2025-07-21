from aiogram.fsm.state import StatesGroup, State


class AuthState(StatesGroup):
    waiting_code = State()
    waiting_phone = State()

class HouseInfoState(StatesGroup):
    waiting_for_mahalla = State()
    waiting_for_street = State()
    waiting_for_qishloq = State()
    waiting_for_home_number = State()
    waiting_for_owner_name = State()
    waiting_for_owner_phone = State()
    waiting_for_search_number = State()
    waiting_for_search_owner_phone = State()

