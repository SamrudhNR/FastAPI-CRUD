from dotenv import load_dotenv
load_dotenv()


import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")



DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

