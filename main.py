import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file
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
model_name= "gemini-2.5-flash"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories. Name directory when user says root to '.' and pkg to 'pkg'.
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. If not provided, lists files in the working directory itself.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt))
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    if len(response.function_calls) > 0:
        for function_call_part in response.function_calls:
            povratna_informacija = call_function(function_call_part, verbose)
            messages.append(povratna_informacija)

            if not (len(povratna_informacija.parts) > 0 and \
                    hasattr(povratna_informacija.parts[0], 'function_response') and \
                    hasattr(povratna_informacija.parts[0].function_response, 'response')):
                raise Exception("Neispravan format povratne informacije iz funkcije!")

            function_response_result = povratna_informacija.parts[0].function_response.response

            if function_response_result == None:
                raise Exception("Function response je None!")

            if verbose:
                print(f"-> {function_response_result}")
    else:
        print("Response:")
        print(response.text)

        
popis_funkcija={"get_files_info": get_files_info,
                "get_file_content": get_file_content,
                "write_file": write_file,
                "run_python": run_python_file}      
def call_function(function_call_part, verbose=False):
    ispravan_poziv_funkcije = function_call_part.name in popis_funkcija
    if ispravan_poziv_funkcije == False:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    pozvana_funkcija = popis_funkcija[function_call_part.name]
    function_call_part.args["working_directory"] = "./calculator"
    function_result = pozvana_funkcija(**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

if __name__ == "__main__":
    main()