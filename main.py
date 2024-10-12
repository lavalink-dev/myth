import discord; from discord.ext import commands
import jishaku; import os; import dotenv
from tools.myth import Superbot

dotenv.load_dotenv()

token = "MTI4NDYxMzcyMTg4ODUyNjQxNw.GoZRST.m9ukM8Mg_KJcEYfMUxqYaP0sRYCYj40PT-QNVI"

Superbot(token=token)
