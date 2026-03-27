import os, argparse
from dotenv import load_dotenv
from google import genai

parser = argparse.ArgumentParser(description="Google Gemini")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

load_dotenv()
apiKey = os.environ.get("GEMINI_API_KEY")
if apiKey == None:
    raise Exception("no api key")

client = genai.Client(api_key=apiKey)

model = "gemini-2.5-flash"
content = args.user_prompt

response = client.models.generate_content(model=model, contents=content)
if response.usage_metadata == None:
    raise RuntimeError("api request failed")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
