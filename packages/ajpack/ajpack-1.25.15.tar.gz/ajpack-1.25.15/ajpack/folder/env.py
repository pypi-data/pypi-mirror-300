import os

def create_env(paths: list[str]) -> None:
    """
    Creates the paths provided. (list)
    
    :param paths: The paths to create.
    """
    for path in list(paths):
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            raise Exception(f"There was an exception while creating the path '{path}'! --> {e}")

def create_standard_env() -> None:
    """
    Creates the standard paths for the project.
    (env, env/logs, env/data, env/images, env/func)
    """
    paths = [
        "env",
        "env/logs",
        "env/data",
        "env/images",
        "env/func",
    ]

    for path in paths:
        os.makedirs(path, exist_ok=True)