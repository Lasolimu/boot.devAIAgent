import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser(description="Google Gemini")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
apiKey = os.environ.get("GEMINI_API_KEY")
if apiKey == None:
    raise Exception("no api key")

client = genai.Client(api_key=apiKey)

model = "gemini-2.5-flash"
content = args.user_prompt
messages = [types.Content(role="user", parts=[types.Part(text=content)])]

response = client.models.generate_content(model=model, contents=messages)
if response.usage_metadata == None:
    raise RuntimeError("api request failed")
if args.verbose:
    print(f"User prompt: {content}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
