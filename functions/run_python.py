import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    try:
        put = os.path.join(working_directory, file_path)
        if os.path.abspath(put).startswith(os.path.abspath(working_directory)) == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(put):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        gotov_proces = subprocess.run(["python", file_path] + args, timeout=30, capture_output=True, cwd=working_directory)
        stdout_str = gotov_proces.stdout.decode('utf-8')
        stderr_str = gotov_proces.stderr.decode('utf-8')

        output_message = ""

        if stdout_str:
            output_message += f"STDOUT: {stdout_str}"
        if stderr_str:
            # Pazi na razmak ako je stdout_str postojao
            if output_message:
                output_message += "\n"
            output_message += f"STDERR: {stderr_str}"

        if gotov_proces.returncode != 0:
            # Opet, pazi na razmak
            if output_message:
                output_message += "\n"
            output_message += f"Process exited with code {gotov_proces.returncode}"

        if not output_message:
            return "No output produced."
        else:
            return output_message
    except Exception as e:
        return f"Error: executing Python file: {e}"