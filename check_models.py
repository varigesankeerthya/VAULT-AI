from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("\nALL AVAILABLE MODELS:\n")

for model in client.models.list():
    print("Model:", model.name)
    print("Supported actions:", getattr(model, "supported_actions", "Not available"))
    print("-------------------------")