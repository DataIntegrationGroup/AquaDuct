from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env file

def get(key):
  return os.getenv(key)