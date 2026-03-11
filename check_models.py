from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

print("🔍 Checking available models for your API Key...")
try:
    models = client.models.list()
    for m in models:
        print(f" - {m.name}")
except Exception as e:
    print(f"Error: {e}")