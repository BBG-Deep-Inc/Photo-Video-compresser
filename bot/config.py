import aiogram
from dotenv import load_dotenv
import os
from aiogram import Bot,Dispatcher
import asyncio
from handlers import router
import sys
from config import PROJECT_ROOT