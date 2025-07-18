from aiogram.dispatcher.filters.state import State, StatesGroup

class OrderState(StatesGroup):
    ChoosingCategory = State()
    ChoosingService = State()
    EnteringLink = State()
    EnteringQuantity = State()
