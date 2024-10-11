import discord; from discord.ext import commands
import jishaku; import os; import dotenv
from tools.start import Superbot

dotenv.load_dotenv()

token = 'MTI4NDYxMzcyMTg4ODUyNjQxNw.GfG5HE.zVu-lVuEb69XGhUiWGai_qBWxuLqQjrwTone68'

Superbot(token=token)
