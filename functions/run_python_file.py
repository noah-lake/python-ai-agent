import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    subprocess_args = ["python3", target_file]
    subprocess_args.extend(args)

    try:
        completed_process = subprocess.run(
            args=subprocess_args,
            capture_output=True,
            timeout=30,
            cwd=abs_working_directory,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        return f"Error: executing python file: {e}"

    if completed_process:
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"
    return "No output produced"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, returning the stdout and sterr. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="The optional arguments to pass into the specified python file.",
                ),
                description="The optional arguments to pass into the specified python file.",
            ),
        },
        required=["file_path"],
    ),
)
