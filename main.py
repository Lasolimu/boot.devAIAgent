import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
apiKey = os.environ.get("GEMINI_API_KEY")
if apiKey == None:
    raise Exception("no api key")

client = genai.Client(api_key=apiKey)

model = "gemini-2.5-flash"
content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

response = client.models.generate_content(model=model, contents=content)
if response.usage_metadata == None:
    raise RuntimeError("api request failed")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
