from aiogram import Dispatcher


from app.bot.handlers import router

from app.bot.factory import create_bot

bot = create_bot()


dp = Dispatcher()

dp.include_router(router)