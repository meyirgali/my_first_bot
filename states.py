from aiogram.fsm.state import State, StatesGroup
class Registor(StatesGroup):
    ism = State()
    familiya = State()
    yosh = State()
    tel_raqam = State()
    manzil  = State()
    kurs = State()
    email = State()
    jinsi = State()
    tugilgan_sana =State()
    hobbi = State()
    tasdiq =State()
   

def save_info(text):
    """Ma'lumotlarni saqlovchi funksiya"""
    with open("state.txt", "w", encoding="utf=8") as f:
        f.write(text)