from sqlalchemy import select
from models import metadata_obj,main_table
from typing import Optional,List 
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
#from chats_models import metadata_obj,chats_table
import asyncio
from datetime import datetime,timedelta



load_dotenv()


async_engine = create_async_engine(
   f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/photo_video_main", 
    pool_size=20,           # Размер пула соединений
    max_overflow=50,        # Максимальное количество соединений
    pool_recycle=3600,      # Пересоздавать соединения каждый час
    pool_pre_ping=True,     # Проверять соединение перед использованием
    echo=False
)

AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)


async def get_all_data():
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table)
            res = await conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            raise Exception(f"Error : {e}")  

async def is_user_exists(username:str) -> bool:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table.c.username).where(main_table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            return data is not None
        except Exception as e:
            raise Exception(f"Error : {e}")        
 
async def create_default_data(username:str):
    if not await is_user_exists(username):
        return
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = main_table.insert().values(
                    username = username,
                    sub = False,
                    date = None
                )
                await conn.execute(stmt)
            except Exception as e:
                raise Exception(f"Error : {e}")
            
async def subscribe(username:str):
    if not await is_user_exists(username):
        return 
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                date_sub = datetime.now().date() + timedelta(days = 30)
                stmt = main_table.update().where(main_table.c.username == username).values(
                    sub = True,
                    date = date_sub
                )
                await conn.execute(stmt)
            except Exception as e:
                raise Exception(f"Error : {e}")

async def is_user_subbed(username:str) -> bool:
    if not await is_user_exists(username):
        return
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table.c.sub).where(main_table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            return data if data is not None else False                
        except Exception as e:
            raise Exception(f"Error : {e}")
                
