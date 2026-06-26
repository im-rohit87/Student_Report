from dotenv import load_dotenv
import os

load_dotenv()

# Email Configuration
EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Project Root
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Folder Configuration
QUIZ_FOLDER = os.path.join(
    BASE_DIR,
    "quizzes"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "outputs"
)

# Quiz Settings
QUIZ_MAX_MARKS = 15

# Email Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587