import os
from config import TRUNCATE_LIMIT


def get_file_content(working_directory, file_path="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot get contents of "{target_file}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{target_file}" is not a file'

    try:
        with open(target_file) as f:
            file_contents = f.read()
            if len(file_contents) > TRUNCATE_LIMIT:
                file_contents = file_contents[:TRUNCATE_LIMIT]
                file_contents += (
                    f'[...File "{target_file}" truncated at 10000 characters]'
                )
            return file_contents
    except Exception as e:
        return f"Error reading files: {e}"
