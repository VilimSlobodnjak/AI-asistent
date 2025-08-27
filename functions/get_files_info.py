import os
from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        put = os.path.join(working_directory, directory)
        if os.path.abspath(put).startswith(os.path.abspath(working_directory)) == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(put)==False:
            return f'Error: "{directory}" is not a directory'
    
        lista_unutar_mape=os.listdir(put)
        lista_podataka=[]
        veličina_fajla=0
        to_je_dir=False
        for fajl in lista_unutar_mape:
            if os.path.isfile(os.path.join(put,fajl))==True:
                veličina_fajla=os.path.getsize(os.path.join(put,fajl))
                to_je_dir = False
            elif os.path.isdir(os.path.join(put,fajl))==True:
                veličina_fajla=os.path.getsize(os.path.join(put,fajl))
                to_je_dir=True
            else:
                veličina_fajla=0
                to_je_dir=False
            lista_podataka.append(f"- {fajl}: file_size={veličina_fajla} bytes, is_dir={to_je_dir}")
            spojena_lista_za_print="\n".join(lista_podataka)
        return spojena_lista_za_print
    except OSError as e:
        return f"Error: {e}"