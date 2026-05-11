import os
from dotenv import load_dotenv

# Load environment variables from a .env file if you prefer
load_dotenv()

# Supabase Credentials
# Replace these with your actual Project URL and API Key from the Supabase Dashboard
SUPABASE_URL = "https://xuqvcxejqwmphzmngewj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh1cXZjeGVqcXdtcGh6bW5nZXdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4ODgzNzUsImV4cCI6MjA5MTQ2NDM3NX0.UFRmP79BbRHW8B5K2yTZac-_tdp9PpVBdFSd5HNmraU"

# Security Configuration
# This MUST be a valid 32-byte base64-encoded key for Fernet encryption
SECRET_KEY = "ihiqdXbe_DhYyVqtHdYfaqiyVxfzYPxx5DxlYK_1I2M="

# Flask Configuration
DEBUG = True