import os
from dotenv import load_dotenv

load_dotenv()


def get_project_id():
    return os.getenv("COMMONBASE_PROJECT_ID")
