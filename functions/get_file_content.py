import os
MAX_CHARS = 10000
from google.genai import types
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to file.",
            ),
        },
    ),
)
def get_file_content(working_directory, file_path):
    try:
        put = os.path.join(working_directory, file_path)
        if os.path.abspath(put).startswith(os.path.abspath(working_directory)) == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(put)==False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        file_size = os.path.getsize(put)
        with open(put, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if file_size > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"