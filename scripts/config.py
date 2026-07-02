import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")

PUSHGATEWAY = os.getenv(
    "PUSHGATEWAY",
    "http://localhost:9091"
)