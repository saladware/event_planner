import asyncio
import datetime

from aiogram import Bot, Dispatcher, types
from asyncio import AbstractEventLoop

from .config import BOT_TOKEN
from .users.auth import get_user, get_db, verify_password
from .events.models import Event


bot = Bot(BOT_TOKEN)


async def get_link():
    user = await bot.me
    return f'https://t.me/{user.username}'


dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = get_user(message.from_user.username, db=next(get_db()))
    if user is None:
        await message.answer(
            'Привет, незнакомец! Мне кажется, тебя здесь быть не должно. Быть может, ты всё ещё не зарегестрирован?'
        )
    elif user.is_verified():
        await message.answer('С возвращением! Я по прежнему буду радовать тебя оповещениями о твоих событиях')
    else:
        await message.answer(
            'Добро пожаловать! Введи /verify <пароль>, чтобы я удостоверился, что это действительно'
            ' ты, и смог подтвердить твой аккаунт')


@dp.message_handler(commands=['verify'])
async def verify(message: types.Message):
    db = next(get_db())
    password = message.get_args()
    user = get_user(message.from_user.username, db=db)
    if user is None:
        await message.answer('Пользователь не найден')
    elif user.is_verified():
        await message.answer('ВЫ уже зарегестрированны')
    elif not password:
        await message.answer('Введи /verify <пароль>')
    elif verify_password(password, user.hashed_password):
        user.verify(message.from_user.id)
        db.commit()
        await message.answer('Профиль успешно зарегестрирован!')
    else:
        await message.answer(f'Пароль не верный: {password}')


async def remind_event(event: Event):
    await bot.send_message(event.author.telegram_id, f'В {event.planned_at} начало события {event.name}')


async def reminder(sleep_for: int = 60 * 60):
    while True:
        await asyncio.sleep(sleep_for)
        db = next(get_db())
        now = datetime.datetime.utcnow()
        upcoming_events = (
            db.query(Event)
            .filter(Event.remind_at <= now + datetime.timedelta(minutes=10))
            .order_by(Event.remind_at)
        )
        for event in upcoming_events:
            wait = (event.remind_at - datetime.datetime.now()).total_seconds()
            await asyncio.sleep(wait)
            await remind_event(event)


def run(loop: AbstractEventLoop):
    loop.create_task(reminder())
    loop.create_task(dp.start_polling())
