import asyncio

from app.bot.dispatcher import bot, dp


async def main():
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())