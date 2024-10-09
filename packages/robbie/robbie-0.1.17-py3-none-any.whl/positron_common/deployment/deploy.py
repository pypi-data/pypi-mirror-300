import signal
import json
import time
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from rich.prompt import Confirm
from positron_common.aws.s3_presigned_handler import S3PresignedHandler
from positron_common.deployment.stored_function import StoredFunction
from positron_common.utils import get_default_workspace_dir
from positron_common.exceptions import RemoteFunctionException, RobbieKnownException
from positron_common.config import PositronJob
from positron_common.enums import finished_job_statuses
from ..job_api import start_stdout_stream, get_job_status, start_job, terminate_job, create_job
from positron_common.cli_args import args as cli_args
from positron_common.deployment.compression import create_workspace_tar, check_workspace_dir
from positron_common.env_config import env
from positron_common.user_config import user_config
from positron_common.constants import temp_path
from ..cli.console import console, ROBBIE_GREEN, SPINNER
from ..cli.logging_config import logger
from ..job_api.terminate_job import terminate_job
from ..print import print_robbie_configuration_banner, print_job_details_banner

# TODO: update env var to just be base url
PORTAL_BASE = env.API_BASE.rstrip('/api')

class Deploy:
    @staticmethod
    def remote_function_deploy(func, args, kwargs, job_config: PositronJob):
        signal.signal(signal.SIGINT, handle_sigint)
        try:
            # TODO: lots of this code is the same as the other `deploy` file, need to consolidate
            logger.debug(f'Job Config: {job_config}')
            job_config.validate_values()
            logger.debug(f'Runtime Environment: {job_config.create_runtime_env()}')

            job = create_job(job_config)
            print_robbie_configuration_banner(job, job_config)
            logger.debug(f"Created Job Details: {json.dumps(job, indent=2)}")

            # prompt the user if they don't pass the -y option
            if not cli_args.skip_prompts:
                user_input = input("Run job with these settings? (Y/n)")
                if not user_input.lower() in ["", "yes", "y", "Yes", "Y"]:
                    terminate_job(job["id"], "User declined to run job from CLI")
                    console.print("[yellow]See you soon![/yellow]")
                    return

            console.print("[bold]Local Machine: [/bold]", style=ROBBIE_GREEN)    
            workspace_dir = (job_config.workspace_dir if job_config.workspace_dir else get_default_workspace_dir())
            logger.debug(f"Workspace Directory: {workspace_dir}")

            if not check_workspace_dir(workspace_dir):
                console.print("[yellow]See you soon![/yellow]")
                terminate_job(job["id"], "User declined to run job from CLI")
                exit(0)
                return

            with Live(Spinner(SPINNER, text=Text("Packaging up workspace artifacts...(1 of 3)", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
                # Create stored function from func and arguments
                stored_function = StoredFunction(func, args, kwargs)
                stored_function.set_job_id(job['id'])
                stored_function.serialize_function()
                stored_function.create_function_metadata(hmac_key=user_config.user_auth_token)
                file_count = create_workspace_tar(workspace_dir=workspace_dir)
                console.print("[green]✔[/green] Workspace artifacts packaged. (1 of 3)")

            if file_count == 0:
                Confirm.ask("No files were found in the workspace directory. Would you like to continue anyway?", default=False)

            with Live(Spinner(SPINNER, text=Text("Uploading workspace to Robbie...(2 of 3)", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
                stored_function.upload_to_s3()
                S3PresignedHandler.upload_file_to_job_folder(f"{temp_path}/{env.COMPRESSED_WS_NAME}", job['id'], env.COMPRESSED_WS_NAME)
                console.print("[green]✔[/green] Workspace uploaded to Robbie. (2 of 3)")

            if cli_args.create_only:
                console.print(f"[green]✔[/green] Job created successfully. (3 of 3)")
                console.print(f"JOB_ID: {job.get('id')}")
                exit(0)
                return

            # start job
            with Live(Spinner(SPINNER, text=Text("Submitting job to Robbie...(3 of 3)", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
                runtime_env = job_config.create_runtime_env()
                logger.debug(f"Runtime Environment: {runtime_env}")
                start_job(job_id=job['id'], data=runtime_env)
                console.print(f"[green]✔[/green] Successfully submitted job to Robbie. (3 of 3)")
                print_job_details_banner(job)
                console.print(f"You can also monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/dashboard/jobs?jobId={job['id']}\n", style=ROBBIE_GREEN)

            # Start standard output stream if option selected
            with Live(Spinner(SPINNER, text=Text("Waiting for remote job to finish...", style=ROBBIE_GREEN)),refresh_per_second=20, console=console, transient=True):
                if cli_args.stream_stdout:
                    start_stdout_stream(job['id'])

                #  Wait for the remote function run to finnish
                while True:
                    job = get_job_status(job['id'])
                    if job['status'] in finished_job_statuses:
                        console.print(f"[green]✔[/green] Done! Now processing results...")
                        result, exception = stored_function.load_and_validate_results(hmac_key=user_config.user_auth_token)
                        console.print("Passing back result.")
                        if exception is not None:
                            raise RemoteFunctionException(exception)
                        else:
                            return  result
                    else:
                        time.sleep(10)
            
        except RobbieKnownException as e:
            """For known errors we dont print exceptions, we just print the user friendly message"""
            console.print(f"[red]An error has ocurred: {e.user_friendly_message}[/red]")
            console.print(f"[yellow]{e.additional_help}[/yellow]")
            exit(0)
        except RemoteFunctionException as e:
            """
                When the result of a remote function call is an Exception being raised
                this is how we let the deserialized exception bubble up back to the client side
            """
            raise e.rf_exception
        except Exception:
            console.print_exception()


def handle_sigint(signum, frame):
    console.print('Terminating gracefully...')
    # TODO: we should actually close open connections
    exit(0)
