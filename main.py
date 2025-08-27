import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info

def main():
    load_dotenv()

    args = sys.argv[1:]
    
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = False
    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True
    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(client, messages, verbose, user_prompt)
model_name= "gemini-1.5-flash"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories. Name directory when user says root to '.' and pkg to 'pkg'.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. If not provided, lists files in the working directory itself.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt))
    if verbose == True:
        print("User prompt:", user_prompt )
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    if len(response.function_calls) > 0:
        for function_call_part in response.function_calls:
            print (f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()