import discord; from discord.ext import commands
import jishaku; import os; import dotenv
from tools.myth import Myth

dotenv.load_dotenv()

token = "MTI4NDYxMzcyMTg4ODUyNjQxNw.GoZRST.m9ukM8Mg_KJcEYfMUxqYaP0sRYCYj40PT-QNVI"

Myth(token=token)
