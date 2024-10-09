import time
import signal
import json
from .exceptions import RobbieKnownException 
from .env_config import env
from .config import PositronJob
from .cli_args import args as cli_args
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
from rich.prompt import Confirm
from .print import print_robbie_configuration_banner, print_job_details_banner, print_job_complete_banner
from .cli.console import console, ROBBIE_GREEN, SPINNER
from .constants import temp_path
from .deployment.compression import create_workspace_tar, check_workspace_dir
from .cli.logging_config import logger
from .job_api import start_stdout_stream, get_job, start_job, terminate_job, create_job
from .utils import get_default_workspace_dir
from positron_common.aws.s3_presigned_handler import S3PresignedHandler

# number of seconds to poll when monitoring job status
POLLING_SEC=1

# for the the deep link
PORTAL_BASE = env.API_BASE.rstrip('/api')
    
# Cloud deployment definition
def positron_deploy(job_config: PositronJob):
    signal.signal(signal.SIGINT, handle_sigint)
    logger.debug(env)
    
    try:
        logger.debug(f'Job Config: {job_config}')
        job_config.validate_values()

        # TODO: We should not be creating a job before we let the user run it, we need defaults in the DBs that we can query
        logger.debug(job_config.create_runtime_env())
        job = create_job(job_config=job_config)
        logger.debug(json.dumps(job, indent=4))
        
        # print the configuration banner
        print_robbie_configuration_banner(job, job_config)
    
        # prompt the user if they don't pass the -y option
        if not cli_args.skip_prompts:
            user_input = input("Run job with these settings? (Y/n)")
            if not user_input.lower() in ["", "yes", "y", "Yes", "Y"]:
                terminate_job(job["id"], "User declined to run job from CLI")
                console.print("[yellow]See you soon![/yellow]")
                return

        # tell people we are on the local machine
        console.print("[bold]Local Machine: [/bold]", style=ROBBIE_GREEN)    

        workspace_dir = (job_config.workspace_dir if job_config.workspace_dir else get_default_workspace_dir())
        logger.debug(f'Workspace directory: {workspace_dir}')
        
        if not check_workspace_dir(workspace_dir):
            console.print("[yellow]See you soon![/yellow]")
            terminate_job(job["id"], "User declined to run job from CLI")
            exit(0)
            return

        # show the spinner as we compress the workspace
        with Live(Spinner(SPINNER, text=Text("Compressing workspace...(1 of 3)", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
            file_count = create_workspace_tar(workspace_dir=workspace_dir)
            console.print("[green]✔[/green] Workspace compression complete (1 of 3)")

        if file_count == 0:
            Confirm.ask("No files were found in the workspace directory. Would you like to continue anyway?", default=False)
    
        # show the spinner as we upload
        with Live(Spinner(SPINNER, text=Text("Uploading compressed workspace to Robbie...(2 of 3)", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
            S3PresignedHandler.upload_file_to_job_folder(f"{temp_path}/{env.COMPRESSED_WS_NAME}", job['id'], env.COMPRESSED_WS_NAME)
            console.print("[green]✔[/green] Workspace uploaded to Robbie (2 of 3)")
        
        if cli_args.create_only:
            console.print(f"[green]✔[/green] Job created successfully. (3 of 3)")
            console.print(f"JOB_ID: {job.get('id')}")
            return

        # spin while submitting job
        with Live(Spinner(SPINNER, text=Text("Submitting job to Robbie...(3 of 3)", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
            start_job(job_id=job['id'], data=job_config.create_runtime_env())
            console.print(f"[green]✔[/green] Successfully submitted job to Robbie. (3 of 3)")

        start = time.perf_counter()
        print_job_details_banner(job)
        

        # Are we streaming stdout or just showing the status changes.
        if cli_args.stream_stdout:
            # tell people we are on the remote machine
            console.print("[bold]Remote Machine Status: [/bold]", style=ROBBIE_GREEN)  
            start_stdout_stream(job['id'])
            # job is down now, diplay final results.    
            final_get_job = get_job(job['id'])
            print_job_complete_banner(final_get_job, start)
        else:
            if cli_args.monitor_status:
                # lets track and display the status updates
                console.print(f"You can also monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/dashboard/jobs?jobId={job['id']}\n", style=ROBBIE_GREEN) 
                
                # tell people we are on the remote machine
                console.print("[bold]Remote Machine Status: [/bold]", style=ROBBIE_GREEN)  
                last_status_change = "Starting..."
                final_get_job = None
        
                with Live(Spinner(SPINNER, text=Text("Processing...", style=ROBBIE_GREEN)),refresh_per_second=20, console=console):    
                    while True:
                        job_result = get_job(job['id'])
                        # are we in a final state?
                        if(jobIsDone(job_result)):
                            break
                        if(job_result['status'] != last_status_change):
                            # there has been a status change
                            time1 = time.strftime("%H:%M:%S")
                            console.print(f"\t{time1}: {job_result['status']}")
                            last_status_change = job_result['status']
                        time.sleep(POLLING_SEC)
                # job is down now, diplay final results.    
                final_get_job = get_job(job['id'])
                print_job_complete_banner(final_get_job, start)
            else:
                console.print(f"You can monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/dashboard/jobs?jobId={job['id']}", style=ROBBIE_GREEN) 

    except RobbieKnownException as e:
            """For known errors we dont print exceptions, we just print the user friendly message"""
            console.print(f"[red]An error has ocurred: {e.user_friendly_message}[/red]")
            console.print(f"[yellow]{e.additional_help}[/yellow]")
            exit(0)
    except Exception:
        # TODO: maybe some additional logging, but we want the process to exit with a non-zero code.
        raise

def jobIsDone(job) -> bool:
    return job['status'] == "terminated" or job['status'] == "complete" or job['status'] == "failed" or job['status'] == "execution_error"


def handle_sigint(signum, frame):
    console.print('Terminating gracefully...')
    # TODO: we should actually close open connections
    exit(0)
