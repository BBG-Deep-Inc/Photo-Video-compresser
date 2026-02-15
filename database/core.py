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