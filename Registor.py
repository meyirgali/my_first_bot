import asyncio
import logging 
import sys 
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message
from states import Registor
from states import save_info

TOKEN = ""
bot = Bot(TOKEN)

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    full_name = message.from_user.full_name
    text = f"Salom {full_name}, Wikipediya botga xush kelibsiz"
    await message.answer(text)

@dp.message(Command("reg"))
async def register(message: Message, state:FSMContext):
    await message.answer("Ro'yxatdan o'tish uchun ma'lumotlarni kiriting ! \nIsmingizni kiriting ")
    await state.set_state(Registor.ism)

@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    ism = message.text
    await state.update_data(ism=ism)
    await state.set_state(Registor.familiya)
    await message.answer("Familiya kiriting ")

@dp.message(F.text, Registor.familiya)
async def register_familiya(message: Message, state:FSMContext):
    familiya = message.text
    await state.update_data(familiya = familiya)
    await state.set_state(Registor.yosh)
    await message.answer("Yoshingizni kiriting ")

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text
    await state.update_data(yosh = yosh)
    await state.set_state(Registor.manzil)
    await message.answer("Manzilingizni kiririntg ")

@dp.message(F.text, Registor.manzil)
async def register_manzil(message:Message, state:FSMContext):
    manzil = message.text
    await state.update_data(manzil=manzil)
    await state.set_state(Registor.tel_raqam)
    await message.answer("Telefon raqamingizni kiriting ")

@dp.message(F.text, Registor.tel_raqam)
async def register_traqam(message:Message, state:FSMContext):
    tel_raqam = message.text
    await state.update_data(tel_raqam=tel_raqam)
    await state.set_state(Registor.kurs)
    await message.answer("Kursni kiriting ")

@dp.message(F.text, Registor.kurs)
async def register_kurs(message:Message, state:FSMContext):
    kurs = message.text
    await state.update_data(kurs=kurs)
    await state.set_state(Registor.email)
    await message.answer("Emailni kiriting ")
    
@dp.message(F.text, Registor.email)
async def register_email(message:Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await state.set_state(Registor.jinsi)
    await message.answer("Jinsingizni kiriting ")

@dp.message(F.text, Registor.jinsi)
async def register_jinsi(message:Message, state:FSMContext):
    jinsi = message.text
    await state.update_data(jinsi=jinsi)
    await state.set_state(Registor.tugilgan_sana)
    await message.answer("Tug'ilgan sanangizni kiriting ")

@dp.message(F.text, StateFilter(Registor.tugilgan_sana))
async def register_tugilgan_sana(message:Message, state:FSMContext):
    tugilgan_sana = message.text
    await state.update_data(tugilgan_sana=tugilgan_sana)
    await state.set_state(Registor.hobbi)
    await message.answer("Hobbiyingizni kiriting ")

@dp.message(F.text, StateFilter(Registor.hobbi))
async def register_hobbi(message:Message, state:FSMContext):
    hobbi = message.text
    await state.update_data(hobbi=hobbi)
    await state.set_state(Registor.tasdiq)
    await message.answer("Ma'lumotlarni tasdiqlaysizmi? (ha/yo'q)")

@dp.message(StateFilter(Registor.tasdiq))
async def register_tasdiq(message: Message, state: FSMContext):
    tasdiq = message.text.lower()

    if tasdiq == "ha":
        data = await state.get_data()
        ism = data.get("ism")
        familiya = data.get("familiya")
        yosh = data.get("yosh")
        manzil = data.get("manzil")
        tel_raqam = data.get("tel_raqam")
        kurs = data.get("kurs")
        email = data.get("email")
        jinsi = data.get("jinsi")
        tugilgan_sana = data.get("tugilgan_sana")
        hobbi = data.get("hobbi")
        text = (
            f"✅ Ro'yxatdan o'tdingiz!\n\n"
            f"Ism: {ism}\nFamiliya: {familiya}\nYosh: {yosh}\n"
            f"Manzil: {manzil}\nTel: {tel_raqam}\nKurs: {kurs}\n"
            f"Email: {email}\nJinsi: {jinsi}\nTug'ilgan sana: {tugilgan_sana}\n"
            f"Hobbi: {hobbi}"
        )
        await message.answer(text)
        save_info(text)
    else:
        await message.answer("❌ Ma'lumotlar bekor qilindi!")
    await state.clear()   

@dp.message(Command("clear"))
async def clear_message(message: Message):
    chat_id = message.chat.id
    for i in range(message.message_id, message.message_id-50, -1): 
        try:
            await bot.delete_message(chat_id, i)
        except:
            pass

async def main():
    global Bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())