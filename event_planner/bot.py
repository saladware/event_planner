import asyncio
import datetime

from aiogram import Bot, Dispatcher, types
from asyncio import AbstractEventLoop

from sqlalchemy import func

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
    if user is None:await message.answer(
            "Hello, stranger! I don't think you should be here. Maybe you're still not registered?"
        )
    elif user.is_verified():
        await message.answer("Welcome back! I will continue to delight you with notifications about your events")
    else:
        await message.answer(
            "Welcome! Enter /verify <password> so that "
            " can make sure it's really you and be able to verify your account"
        )


@dp.message_handler(commands=['verify'])
async def verify(message: types.Message):
    db = next(get_db())
    password = message.get_args()
    user = get_user(message.from_user.username, db=db)
    if user is None:
        await message.answer('User not found')
    elif user.is_verified():
        await message.answer('You are already registered')
    elif not password:
        await message.answer('Enter /verify <password>')
    elif verify_password(password, user.hashed_password):
        user.verify(message.from_user.id)
        db.commit()
        await message.answer('Your account has been successfully registered!')
    else:
        await message.answer(f'The password is incorrect: {password}')


async def remind_event(event: Event):
    await bot.send_message(
        event.author.telegram_id,
        f'At {event.planned_at} the beginning of the event "{event.name}". {event.description}'
    )


async def reminder(sleep_for: int = 60 * 5):
    while True:
        db = next(get_db())
        upcoming_events = (
            db.query(Event)
            .filter(
                Event.remind_at <= func.now() + datetime.timedelta(minutes=10),
                Event.is_happened.is_(False)
            )
            .order_by(Event.remind_at)
        )
        for event in upcoming_events:
            wait = (event.remind_at - datetime.datetime.now(tz=event.remind_at.tzinfo)).total_seconds()
            if wait > 0:
                await asyncio.sleep(wait)
            await remind_event(event)
            event.is_happened = True
            db.commit()
            db.refresh(event)
        await asyncio.sleep(sleep_for)


def run(loop: AbstractEventLoop):
    loop.create_task(reminder())
    loop.create_task(dp.start_polling())
