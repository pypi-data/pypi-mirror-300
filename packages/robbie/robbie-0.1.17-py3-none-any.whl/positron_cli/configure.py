from rich import print
from positron_cli.interactive import prompt_and_build_PositronJobConfig

DEFAULT_CONF_FILENAME = './job_config.yaml'

def configure() -> None:
    """
    Build a Robbie job configure file (job_config.yaml) interactively.

    """
    print("Please follow the prompts to build a 'job_config.yaml' in your current directory.")
    print("Values in brackets [] are default, use the <tab> key to see a menu of options.\n")
    
    cfg = prompt_and_build_PositronJobConfig()

    if cfg:
        cfg.write_to_file(filename=DEFAULT_CONF_FILENAME)
        print(f"[green] Successfully wrote config file {DEFAULT_CONF_FILENAME}'")
        print(f"[yellow]---------- Contents ----------")
        print(cfg)
        print(f"[yellow]---------- End ----------")




    
