import os


def get_file_path_in_curr_working_dir(file_name):
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, file_name)
