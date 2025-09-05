import os
import subprocess


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
