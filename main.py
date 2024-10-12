import discord
import jishaku 
import os 
import dotenv

from discord.ext       import commands

from tools.myth       import Myth

dotenv.load_dotenv()

token = "MTI4NDYxMzcyMTg4ODUyNjQxNw.GoZRST.m9ukM8Mg_KJcEYfMUxqYaP0sRYCYj40PT-QNVI"

Myth(token=token)
