import os
import tarfile
from rich.tree import Tree
from positron_common.env_config import env
from positron_common.constants import temp_path
from rich.prompt import Confirm
from ..cli.console import console

def check_workspace_dir(workspace_dir: str):
    if not os.path.exists(workspace_dir):
        question_prompt = f"Directory '{workspace_dir}' does not exist. Would you like to create it?"
        if Confirm.ask(f'{question_prompt}', default=True):
            os.makedirs(workspace_dir)
            return True
        console.print("[yellow]Either update the 'workspace_dir' config or remove it to use the default of the current workspace.[/yellow]")
        return False
    return True

def create_workspace_tar(workspace_dir: str) -> int:
    # Use the context manager to handle opening and closing the tar file
    tree = Tree("Local (workspace) files to copy to Remote Machine")
    path = f"{temp_path}/{env.COMPRESSED_WS_NAME}"
    last_files_compressed_count = 0

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    with tarfile.open(path, 'w:gz') as tar:
        for root, dirs, files in os.walk(workspace_dir):
            for exclude_dir in ['.venv', '.git', '__pycache__', temp_path]:
                try:
                    dirs.remove(exclude_dir)
                except ValueError:
                    # Ignore if the directory is not in the list
                    pass
            for file in files:
                last_files_compressed_count += 1
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=workspace_dir)
                file_size = os.path.getsize(full_path)
                tar.add(full_path, arcname=arcname)
                tree.add(f"[yellow]{arcname}, size: {file_size} bytes[/yellow]")
    if last_files_compressed_count > 0:
        console.print(tree)
    return last_files_compressed_count
