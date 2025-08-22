import os


def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_directory):
        return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'

    try:
        display_strings = []
        for file in os.listdir(target_dir):
            filepath = os.path.join(target_dir, file)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            display_strings.append(
                f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(display_strings)
    except Exception as e:
        return f"Error listing files: {e}"
