import os
from google.genai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write in file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to file."),
            "content": types.Schema(
            type=types.Type.STRING,
            description="Content to write in file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        put = os.path.join(working_directory, file_path)
        if os.path.abspath(put).startswith(os.path.abspath(working_directory)) == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        directory = os.path.dirname(put)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(put, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"