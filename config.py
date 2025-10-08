import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")  # or gpt-3.5-turbo for faster/cheaper responses

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TITLE = "Smart Match API"
API_DESCRIPTION = "Intelligent product matching API for parsing queries into structured search facets"
API_VERSION = "1.0.0"

# Facets Configuration
FACETS_CONFIG_PATH = "facets_config.json"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
