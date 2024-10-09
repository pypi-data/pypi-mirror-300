import typer
import os
from typing_extensions import Annotated
from typing import Optional
from positron_common.deploy import positron_deploy
from positron_common.config import parse_job_config, PositronJobConfig, PositronJob
from positron_common.cli_args import args
from positron_common.cli.console import console
from positron_cli.interactive import prompt_and_build_PositronJobConfig, build_synthetic_PositronJobConfig

JOB_CONF_YAML_PATH = "./job_config.yaml"

def run(
  commands: Annotated[Optional[str], typer.Argument(help='String of shell commands')] = None,
  config: Annotated[str, typer.Option("--f", help='The path to the job configuration file')] = None,
  debug: Annotated[bool, typer.Option("--debug", help='Enable debug logging')] = False,
  tail: Annotated[bool, typer.Option("--tail", help='Tail the job\'s stdout back to your CLI')] = False,
  status: Annotated[bool, typer.Option("--s", help='Monitor job status in your CLI')] = False,
  skip_prompts: Annotated[bool, typer.Option("--y", help='Bypass the prompts and run the job immediately')] = False,
  interactive: Annotated[bool, typer.Option("--i", help="Interactively choose your job configuration.")] = False,
  create_only: Annotated[bool, typer.Option("--create-only", help="Only create the job, do not run it.")] = False,
) -> None:
    """
    Run a command line job in Robbie

    You can optionally specify [COMMANDS] to run. 
    If no commands are specified in the command line, the command will be taken from the job_config.yaml file.
    """
    # we can either stream or monitor status but not both at the same time
    if tail and status:
        console.print('[bold red]Error: Choose either the -logs and -s option.')
        return
    
    if commands and config:
        console.print('[bold red]Error: Specify run commands directly in the CLI or in the job_config.yaml.')
        return

    # initialize the argument singleton
    args.init(
        debug=debug,
        stream_stdout=tail,
        skip_prompts=skip_prompts,
        monitor_status=status,
        commands_to_run=commands,
        interactive=interactive,
        create_only=create_only,
    )

    if commands:
        # create synthetic config for now until defaults are supported in the backend
        cfg = build_synthetic_PositronJobConfig(commands)
        # write it so it gets transfered to the remote machine
        if cfg == None:
            return
        cfg.write_to_file()
        
    elif interactive:
        # lets prompt the user 
        print("Please follow the prompts to the paramters to run your job")
        print("Values in brackets [] are default, use the <tab> key to see a menu of options.\n")
        cfg = prompt_and_build_PositronJobConfig()
        print("interactive cfg: ", cfg)
        if cfg == None:
            return
        cfg.write_to_file(filename=JOB_CONF_YAML_PATH)
            
    # this is the same for use case, even interactive and command.
    # in those case, we just read the previously generated files.
    if not config:
        config = JOB_CONF_YAML_PATH
    print(f'Using job configuration file: {config}')
    if not os.path.exists(config):
        console.print(f'[bold red]Error {config} file not found')
        return
      
    job_config = parse_job_config(config)
    if not job_config:
        console.print('[bold red]Error parsing job_config.yaml file. See the documentation for more information.')
        return
        
    positron_deploy(job_config)



