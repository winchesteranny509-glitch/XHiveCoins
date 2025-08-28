# app.py
import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-service.onrender.com

if not BOT_TOKEN or not WEBHOOK_URL:
    raise SystemExit("Set BOT_TOKEN and WEBHOOK_URL environment variables on the host.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

GAME_URL = "https://winchesteranny509-glitch.github.io/HivePuzzleEarn/"

WELCOME_TEXT = (
    "🎉 Welcome to X Giveaway!\n\n"
    "💎 Turning your time into free tokens!\n"
    "🚀 Earn crypto while you play!\n"
    "💰 Helping you build wealth with free crypto!\n"
    "🌍 Empowering everyone to earn free crypto!\n"
    "🔑 Making crypto accessible through rewards!\n"
    "🌟 Your gateway to free crypto earnings!\n\n"
    "👇 Click below to start playing 👇"
)

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Play for Giveaway",
                                   web_app=types.WebAppInfo(url=GAME_URL))]
    ])
    await message.answer(WELCOME_TEXT, reply_markup=kb)

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    # register webhook: Telegram will POST updates to <WEBHOOK_URL>/webhook
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
