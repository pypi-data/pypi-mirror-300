
import os
from positron_common.job_api.funding_envs_images import list_environments, list_funding_sources, list_images
from rich import print
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from positron_common.config import PositronJob
from positron_common.config import PositronJobConfig


# Prompts the user for FGs, environmetns, etc.
# Queries the backend for the FundingSources and Environments.
def prompt_and_build_PositronJobConfig(
) -> PositronJobConfig:

    pj = PositronJob()

    # fetch the names and ids
    fs = FundingSources.load()
    fs_choice = prompt('Select how to bill your job [Personal tokens] ', completer=WordCompleter(fs.menu_items()))

    if len(fs_choice):
        fs_id = fs.id_from_menu_item(fs_choice)
    else:
        fs_id = fs.default_funding_source_id()
        
    pj.funding_group_id = fs_id
    # fetch the envionments available to this Funding Source
    envs = Environments.load(pj.funding_group_id)

    # are there any environments in this funding source?
    if envs:
        env_choice = prompt(f'Select your preferred hardware [{fs.default_env_name_from_fs_id(fs_id)}]: ', completer=WordCompleter(envs.menu_items()))
    else:
        # no environments for the user oh well
        print(f"[bold red]Error your funding sources: {fs_choice} has no approved hardware, please contact 'support@robbie.run'")
        return None

    if len(env_choice):
        pj.environment_id = envs.id_from_menu_item(env_choice)
    else:
        # choose the default, if available
        if fs.default_env_id_from_fs_id(fs_id) == None:
             print(f"[bold red] Error funding source: {fs_choice} has no default hardware and you didn't specify any.")
             return None
        else:
            pj.environment_id = fs.default_env_id_from_fs_id(fs_id)

    # show the images
    images = Images.load(pj.funding_group_id, pj.environment_id)
    image_choice = prompt(f'Select your preferred image[{fs.default_image_name(fs_id)}]: ', completer=WordCompleter(images.menu_items()))

    if len(image_choice):
        pj.image = images.name_from_menu_item(image_choice)
    else:
        # choose the default, if available
        if fs.default_image_name(fs_id) == None:
             print(f"[bold red] Error funding source: {fs_choice} has no default hardware and you didn't specify any.")
             return None
        else:
            pj.image = fs.default_image_name(fs_id)

    text = prompt('Max tokens [none]:')
    if len(text):
        pj.max_tokens = text
    
    text = prompt('Max time in HH:MM format [none]:')
    if len(text):
        pj.max_tokens = text

    text = prompt(f'Specify the directory contents to send to the remote machine [{os.getcwd()}]:')
    if len(text):
        pj.workspace_dir = text
    else:
        pj.workspace_dir = os.getcwd()

    # environment variables are part of a nested dict
    pj.env = {}
    while True:
        var_name = prompt('Environment variable name <return to exit>:')
        if not var_name:
            break
        var_value = prompt(f'Value for {var_name} (hint=hit <return> to use local machine value):')
        pj.env[var_name] = var_value

    # loop through and create a big string of commands
    pj.commands = []
    while True:
        cmd = prompt('Enter command to run <return to exit>:')
        if not cmd:
            break
        pj.commands.append(cmd)

    return PositronJobConfig(version="1.0", python_job=pj)
    

def build_synthetic_PositronJobConfig(commands: str
) -> PositronJobConfig:
    pj = PositronJob()
    pj.commands = []
    pj.commands.append(commands)

    return PositronJobConfig(version="1.0", python_job=pj)




# Naming
FS_ID="id"
FS_NAME="name"
FS_TOKENS="userTokens"
FS_MENU="menu"
FS_TYPE="type"
FS_DEFAULT_IMAGE_NAME="defaultImageName"
FS_DEFAULT_IMAGE_ID="defaultImageId"
FS_DEF_ENV_NAME="defaultEnvironmentName"
FS_DEF_ENV_ID="defaultEnvironmentId"
FS_PERSONAL_NAME="Personal"
FS_PERSONAL_TYPE="PERSONAL"


# singleton builds a list of tuples from the DB results
class FundingSources: 
    is_init: bool = False
    my_fs: dict

    def __init__(self, fs_arg: dict):
        if self.is_init:
            raise ValueError('FundingSources.load() already initialized')
        else:
            self.init = True
            self.my_fs= fs_arg

    @staticmethod
    def load():
        fs = list_funding_sources()
        if len(fs) == 0:
            return None
        # Loop through and add a customer "menu" item to each dict 
        for key, val in fs.items(): 
                val[FS_MENU] = f'{val[FS_NAME]} ({val[FS_TOKENS]} tokens available)'
        return FundingSources(fs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for key, val in self.my_fs.items():
            # just show names
            ret_list.append(val[FS_MENU])
        return ret_list

    # Return 'funding_group_id' using the val returned from session.prompt() 
    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val[FS_ID]
        return None

    def default_env_id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val[FS_DEF_ENV_ID]
        return None
    
    def default_env_name_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val[FS_DEF_ENV_NAME]
        return None
    
    def default_env_name_from_fs_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    if FS_DEF_ENV_NAME in val:
                        return val[FS_DEF_ENV_NAME]
        return None
    
    def default_env_id_from_fs_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    if FS_DEF_ENV_ID in val:
                        return val[FS_DEF_ENV_ID]
        return None
    
    def default_env_id(self) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                if FS_DEF_ENV_NAME in val:
                    return val[FS_DEF_ENV_ID]
        return None
    
    def default_funding_source_id(self) -> str: 
        for key, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val[FS_ID]
        return None
    
    def default_image_name(self, id: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val[FS_DEFAULT_IMAGE_NAME]
        return None
    
    def default_image_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val[FS_DEFAULT_IMAGE_ID]
        return None
    


# offsets for the list of tuples
ENV_NAME="environmentName"
ENV_ID="id"
ENV_TPH="tokensPerHour"
ENV_MENU_ITEM="menu"

# singleton for Environments
class Environments: 
    is_init: bool = False
    my_envs: dict

    def __init__(self, env_arg):
         if self.is_init:
            raise ValueError('Environments.load() already initialized')
         else:
            self.my_envs = env_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str):
        envs = list_environments(fs_id)
        if len(envs) == 0:
            return None
        for key, val in envs.items():
            val[ENV_MENU_ITEM] = f"{val['environmentName']} ({val['tokensPerHour']} Tokens/Hour)" # shows in menu
        return Environments(envs)

    def menu_items(self) -> list: 
        menu_list = []
        for key, val in self.my_envs.items():
            menu_list.append(val[ENV_MENU_ITEM])
        return menu_list

    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_MENU_ITEM] == menu_item):
                return val[ENV_ID]
        return None

    def tokens_per_hour(self, env_id: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_ID] == env_id):
                return val[ENV_TPH]
        return None
        


# offsets for the list of tuples
IMAGE_NAME="imageName"
IMAGE_ID="id"
IMAGE_MENU_ITEM="menu"

# singleton for Environments
class Images: 
    is_init: bool = False
    my_images: dict

    def __init__(self, image_arg):
         if self.is_init:
            raise ValueError('Images.load() already initialized')
         else:
            self.my_images = image_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str, env_id: str):
        images = list_images(fs_id, env_id)
        if len(images) == 0:
            return None
        for key, val in images.items():
            val[IMAGE_MENU_ITEM] = f"{val[IMAGE_NAME]}" # shows in menu
        return Images(images)

    def menu_items(self) -> list: 
        menu_list = []
        for key, val in self.my_images.items():
            menu_list.append(val[IMAGE_MENU_ITEM])
        return menu_list

    def name_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_images.items():
            if (val[IMAGE_MENU_ITEM] == menu_item):
                return val[IMAGE_NAME]
        return None
        
