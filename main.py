import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import (available_functions, call_function)

def generateContent(client, model, messages):
    return client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        )
    )

def processCalls(response):
    if response.function_calls != None:
        functionResults = []
        for call in response.function_calls:
            result = call_function(call, call.args)

            if result.parts == None or len(result.parts) == 0:
                raise Exception("result has no parts")
            
            functionResponse = result.parts[0].function_response
            if functionResponse == None:
                raise Exception("no function response")
            
            responseString = functionResponse.response
            if functionResponse.response == None:
                raise Exception("no string from function")
            
            functionResults.append(result.parts[0])
            
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
        return functionResults
    else:
        print(response.text)
        return []


parser = argparse.ArgumentParser(description="Google Gemini")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
apiKey = os.environ.get("GEMINI_API_KEY")
if apiKey == None:
    raise Exception("no api key")

client = genai.Client(api_key=apiKey)

# model = "gemini-2.5-flash"
model = "gemini-2.5-flash-lite"
content = args.user_prompt
messages = [types.Content(role="user", parts=[types.Part(text=content)])]

finalResponse = False
for _ in range(13):
    response = generateContent(client, model, messages)
    if response.usage_metadata == None:
        raise RuntimeError("api request failed")
    if args.verbose:
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates != None and len(response.candidates) > 0:
        for candidate in response.candidates:
            messages.append(candidate.content)

    functionResults = processCalls(response)
    if len(functionResults) > 0:
        messages.append(types.Content(role="user", parts = functionResults))
    else:
        finalResponse = True
        break

if not finalResponse:
    print("Error: did not find final response")
    sys.exit(1)