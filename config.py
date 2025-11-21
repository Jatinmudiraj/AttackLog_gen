# import os
# from dotenv import load_dotenv

# # Load environment variables from .env (if present)
# load_dotenv()

# # OpenAI API key (optional – if missing, SAFE_MODE is used)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# # If no key, we don't call the real API, we generate demo logs
# SAFE_MODE = (OPENAI_API_KEY == "")

# # Base folders
# BASE_LOG_FOLDER = "system_logs"
# CONFIG_FOLDER = "configs"

# # Default GPT model (if API key is present)
# # You can change this to: "gpt-4.1", "gpt-4o", etc.
# GPT_MODEL = "gpt-4o-mini"

import os
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# OpenAI API key (optional – if missing, SAFE_MODE is used)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# If no key, we don't call the real API, we generate demo logs
SAFE_MODE = (OPENAI_API_KEY == "")

# Base folders
BASE_LOG_FOLDER = "system_logs"
CONFIG_FOLDER = "configs"

# New: folder for high-level prompt templates
PROMPT_TEMPLATE_FOLDER = "prompt_templates"

# Default GPT model (if API key is present)
# You can change this to: "gpt-4.1", "gpt-4o", etc.
GPT_MODEL = "gpt-4o-mini"
