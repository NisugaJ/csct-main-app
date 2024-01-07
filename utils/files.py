import os

def get_files_in_dir(relative_dir, file_ext):
    all_files = []

    for filename in os.listdir(relative_dir):
        file = f"{relative_dir}/{filename}"
        _, file_extension = os.path.splitext(file)
        if file_extension == file_ext:
            all_files.append(file)

    return all_files