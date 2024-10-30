from dotenv           import load_dotenv
from tools.myth       import Myth
from os               import environ

load_dotenv()
Myth(token=environ['TOKEN'])
