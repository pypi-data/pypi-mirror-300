import os
import signal
import subprocess
import requests
import tarfile
import time
from typing import List, Optional
from threading import Thread
from datetime import datetime, timezone
from positron_common.config import parse_job_config, PositronJob
from positron_common.exceptions import RobbieException
from .runner_env import runner_env
from .cloud_storage import cloud_storage
from .cloud_logger import logger
from .remote_function import RemoteFunction

'''_______________________________________________________________________________________
    
    INITIALIZING CONFIGURATION AND CONSTANTS
    ______________________________________________________________________________________
'''

# Define API endpoints
API_BASE = runner_env.API_ENDPOINT
API_GET_JOB = f'{API_BASE}/get-job'
API_UPDATE_JOB = f'{API_BASE}/update-job'
API_JOB_LIFECYCLE = f'{API_BASE}/check-lifecycle'

# Define cross component enums
job_statuses = dict(
    pending="pending",
    uploading="uploading",
    in_queue="in_queue",
    launching="launching_pod",
    pulling_image="pulling_image",
    pulled_image="pulled_image",
    starting_container="starting_container",
    started_container="started_container",
    initializing="initializing",
    computing="computing",
    storing="storing",
    complete="complete",
    failed="failed",
    execution_error="execution_error",
    terminate="terminate_job",
    terminated="terminated"
)

# Job management
running_job = None
kill_threads = False
job = {}
final_status = job_statuses['complete']
return_code = 0

# Request header
headers = {}

# Constants for S3
S3_BASE_PATH = f"{runner_env.JOB_OWNER_EMAIL}/{runner_env.JOB_ID}"
S3_RESULT_PATH = f"{S3_BASE_PATH}/result"

# Unpack workspace ----------------------------------------------------
def unpack_workspace_from_s3():
    s3_key = f"{S3_BASE_PATH}/workspace.tar.gz"
    try:
        local_tar_path = os.path.join(runner_env.RUNNER_CWD, 'workspace.tar.gz')
        cloud_storage.download_file(s3_key, local_tar_path)

        logger.info('Unpacking workspace')
        with tarfile.open(local_tar_path) as tar:
            tar.extractall(runner_env.JOB_CWD)
        logger.info('Workspace unpacked successfully')

    except Exception as e:
        logger.error(f"Failed to unpack workspace from S3: {e}")

# Upload results ----------------------------------------------------
def upload_results_to_s3():
    try:
        logger.info('Copying results')

        results_dir = f"{runner_env.JOB_CWD}"
        os.makedirs(results_dir, exist_ok=True)

        # Create a tar.gz of the result directory
        tar_file_name = f"{results_dir}/result.tar.gz"
        with tarfile.open(tar_file_name, "w:gz") as tar:
            tar.add(runner_env.JOB_CWD, arcname=os.path.basename(results_dir))

        # Upload all files in JOB_CWD recursively to S3
        for root, dirs, files in os.walk(runner_env.JOB_CWD):
            if 'venv' in dirs:
                dirs.remove('venv')
            
            if 'persistent-disk' in dirs:
                dirs.remove('persistent-disk')

            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, runner_env.JOB_CWD)
                s3_key = f"{S3_RESULT_PATH}/{rel_path}"
                cloud_storage.upload_file(file_path, s3_key)

        logger.info('Results uploaded to S3 successfully')

    except Exception as e:
        logger.error(f"Failed to upload results to S3: {e}")

'''_______________________________________________________________________________________
    
    SUB MODULES
    ______________________________________________________________________________________
'''
# Get Job -----------------------------------------------------------
def get_job():
    logger.info('Fetching job details')
    resp = try_request(requests.get, API_GET_JOB, headers=headers)
    global job
    job = resp.json()

# Run Job -----------------------------------------------------------
def run_job():
    logger.info('Starting job')
    update_job(status=job_statuses["computing"])
    
    config_file = os.path.join(runner_env.JOB_CWD, "job_config.yaml")
    job_config = parse_job_config(config_file)

    if job_config and job_config.commands:
        run_commands(job_config)
    else:
        run_decorator_job(job_config=job_config)


def run_commands(job_config: Optional[PositronJob]):
    commands: List[str] = job_config.commands
    logger.info(f'Found commands to execute:\n{commands}')

    # build command and execute as separate process
    commands_string = ';\n'.join(commands)
    start_and_monitor_job(commands_string, job_config)


def run_decorator_job(job_config: Optional[PositronJob]):
    # Determine which cli to install
    robbie_local_cli_cmd = f"[ -d \"{runner_env.ROBBIE_CLI_PATH}\" ] && echo 'Installing local robbie cli...' && pip install {runner_env.ROBBIE_CLI_PATH}"
    robbie_env_cli_cmd = "echo 'Installing positron-networks' && pip install positron-networks"
    if (runner_env.POSITRON_CLI_ENV == "development"):
        robbie_env_cli_cmd = "echo 'Installing positron-networks:dev' && pip install --force-reinstall --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --pre positron-networks"
    if (runner_env.POSITRON_CLI_ENV == "test"):
        robbie_env_cli_cmd = "echo 'Installing positron-networks:test' && pip install --force-reinstall --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ positron-networks"
    install_robbie_cmd = f"{robbie_local_cli_cmd} || {robbie_env_cli_cmd}"

    enter_env = "python -m venv venv && . venv/bin/activate"
    install_requirements = "[ -f requirements.txt ] && pip install -r requirements.txt || echo 'No requirements to install'"

    # Construct the command
    # By putting the install_robbie_cmd at the end, we ensure the latest version of robbie is installed,
    # overriding any version in the requirements.txt
    command_base = " && ".join([
        enter_env,
        install_requirements,
        install_robbie_cmd,
    ])
    entry_point = job['entryPoint']

    # TODO: Need to add a type to job or something, not this.
    if entry_point == 'REMOTE_FUNCTION_CALL':
        # Download the additional resources required.
        logger.info('Downloading function and arguments')
        rm = RemoteFunction()
        rm.setup()
        entry_point = rm.entry_point

    if entry_point is None:
        logger.error('Entry point is required for decorator jobs!')
        global final_status; final_status = job_statuses["execution_error"]
        return

    meta = job.get('meta', {})
    job_arguments = meta.get('jobArguments', [])

    # Join job arguments with spaces
    arguments_string = ' '.join(job_arguments)

    # Construct the execution command
    execution_command = f"python {entry_point} {arguments_string}"

    # Log the execution command
    logger.info(f"Installing Dependencies and running: {execution_command}")

    # Combine the base command with the execution command
    full_command = f"{command_base} && {execution_command}"
    logger.debug(f"Full command: {full_command}")
    start_and_monitor_job(full_command, job_config)


def start_and_monitor_job(command: str, job_config: Optional[PositronJob]):
    sub_env = runner_env.env_without_runner_env()
    if job_config:
        job_config_env = job_config.parse_runtime_env()
        sub_env.update(job_config_env)

    # collect current environment variables from env
    job_runner_env = {}
    for key in sub_env.keys():
        job_runner_env[key] = os.getenv(key, None)
    logger.debug(f'Job runner environment vars: {job_runner_env}')
    logger.debug(f'Running client job with job environment: {sub_env}')
    # Start job
    global running_job
    if (runner_env.JOB_USER == 'positron'):
        logger.debug('Running job as current user')
        running_job = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            shell=True,
            cwd=runner_env.JOB_CWD,
            env=sub_env,
        )
    else:
        logger.debug('Running job as protected user')
        running_job = subprocess.Popen(
            ["su", "-c", command, "-s", "/bin/bash", runner_env.JOB_USER],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            text=True,
            # shell=True,
            cwd=runner_env.JOB_CWD,
            env=sub_env,
            preexec_fn=os.setsid,
        )

    logger.debug(f"Job started with PID: {running_job.pid}")

    # Start parallel threads
    termination_thread = start_termination_thread()
    charge_thread = start_charging_thread()
    stdout_thread = Thread(target=logging_thread, args=(running_job.stdout, "stdout")); stdout_thread.start()
    stderr_thread = Thread(target=logging_thread, args=(running_job.stderr, "stderr")); stderr_thread.start()
    logger.debug(f"Started stdout logging thread with ID: {stdout_thread.ident}")
    logger.debug(f"Started stderr logging thread with ID: {stderr_thread.ident}")

    # Wait for the process to finish
    running_job.wait()

    # user job has finished
    global return_code
    return_code = running_job.returncode
    logger.debug(f"User job exited with return code: {return_code}")


    # Terminate threads
    global kill_threads; kill_threads = True
    stdout_thread.join()
    stderr_thread.join()
    charge_thread.join()
    termination_thread.join()

    logger.debug("Threads have completed.")

    global final_status
    if final_status != job_statuses['terminated'] and return_code > 0: final_status = job_statuses["execution_error"]

def decode_if_bytes(line):
    return line.decode('utf-8') if isinstance(line, bytes) else line

# Finish Job --------------------------------------------------------
def finish_job():
    logger.info("Finishing job")
    out_str = '\n'.join(decode_if_bytes(line) for line in logger.stdout)
    err_str = '\n'.join(decode_if_bytes(line) for line in logger.stderr)

    tokens_used = job['tokensUsed']

    if tokens_used:
        tokens_used_msg = f'Total tokens used for processing job: {tokens_used}'
        logger.info(tokens_used_msg)
        out_str += f'\n{tokens_used_msg}'

    logger.debug(f"Updating job with logs: output log size: {len(out_str)}, error log size: {len(err_str)}")

    update_job(status=final_status, end_date=datetime.now(timezone.utc), output_log=out_str, error_log=err_str)
    
    # Shared backend checks for this signal to terminate socket connection
    logger.info("Job successfully completed.")
    logger.end_of_logs_signal()


'''_______________________________________________________________________________________
    
    UTILS
    ______________________________________________________________________________________
'''
# Check for termination ---------------------------------------------
def is_job_active():
    if (runner_env.rerun):
        return True

    resp = try_request(requests.get, API_GET_JOB, headers=headers)
    db_job = resp.json()
    inactive_statuses = [
        job_statuses["complete"],
        job_statuses["failed"],
        job_statuses["execution_error"],
        job_statuses["terminate"],
        job_statuses["terminated"],
    ]

    if db_job['status'] not in inactive_statuses:
        return True

    global final_status
    if db_job['status'] == job_statuses["terminate"]:
        final_status = job_statuses["terminated"]
        logger.info("The job has been terminated by the user.")
    else:
        final_status = db_job['status']
        logger.info(f"The job is not active anymore (status: {db_job['status']})")

    return False


# Update Job --------------------------------------------------------
def update_job(status, start_date=None, end_date=None, output_log=None, error_log=None):
    logger.info(f'Updating status: {status}')
    body={
        "status": status,
        "startDate": start_date.isoformat() if start_date is not None else None,
        "endDate": end_date.isoformat() if end_date is not None else None,
        "outputLog": output_log,
        "errorLog": error_log
    }
    # filter out the items where the value is None
    body = {key:value for key, value in body.items() if value is not None}
    try_request(requests.post, API_UPDATE_JOB, headers=headers, json_data=body)

# Charging thread ---------------------------------------------------
def start_charging_thread():
    logger.debug('Start charging thread')
    def charge_thread():
        while not kill_threads:
            res = try_request(requests.post, API_JOB_LIFECYCLE, headers=headers)
            if res is None:
                # stop looping, job is forced to terminate by try_request
                break
            j = res.json()
            if not j['succeeded']:
                # unable to validate job lifecycle due to known reason (e.g. insufficient funds, time/token limit exceeded)
                logger.error('Job lifecycle error!')
                logger.error(j['message'])

            # @Todo: discuss if job should be charged for every computational minute that is started, i.e. if termination occurs
            # between two charge calls, should we charge for the minute that was started but not completed?
            time.sleep(runner_env.POSITRON_CHARGE_INTERVAL) # @Todo: if these intervals are too long, termination of the job can take long
    ct = Thread(target=charge_thread)
    ct.start()
    return ct


# Termination thread ------------------------------------------------
def start_termination_thread():
    logger.debug('Starting termination thread')
    def termination_thread():
        while not kill_threads:
            res = try_request(requests.get, API_GET_JOB, headers=headers)
            if res is None:
                # stop looping, job is forced to terminate by try_request
                break
            j = res.json()
            if j['status'] == job_statuses['terminate']:
                logger.info('Terminating job')
                terminate_running_job()
                global final_status; final_status = job_statuses["terminated"]
                break
            time.sleep(runner_env.POSITRON_CHECK_TERMINATION_INTERVAL)

    tt = Thread(target=termination_thread)
    tt.start()
    return tt


# Logging thread ----------------------------------------------------
def logging_thread(pipe, stream_name: str):
    try:
        with pipe:
            for line in iter(pipe.readline, ''):
                if line.strip():
                    if stream_name == "stdout":
                        logger.info("job stdout: " + line.rstrip())
                    else:
                        logger.error("job stderr: " + line.rstrip())
    except Exception as e:
        logger.error(f'logging pipe for stream: {stream_name} closed with exception: {e}')


# Terminate running job ---------------------------------------------
def terminate_running_job():
    global running_job
    # Signal termination
    if (running_job is not None) and (running_job.poll() is None):
        logger.debug("Terminating job process")
        os.killpg(os.getpgid(running_job.pid), signal.SIGTERM)
        logger.debug("running_job.kill(): completed")
        running_job.stdout.close()
        logger.debug("running_job.stdout.close(): completed")
        running_job.stderr.close()
        logger.debug("running_job.stderr.close(): completed")
        running_job.wait()  # Wait for job to terminate completely
        logger.debug("Job process terminated")


# Retry API requests ------------------------------------------------
def try_request(request_func, url, retries=2, headers=None, json_data=None):
    for attempt in range(retries):
        try:
            response = request_func(url, headers=headers, json=json_data)
            response.raise_for_status()  # Raise an error for 4xx and 5xx status codes
            return response
        except requests.RequestException as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                logger.debug("Retrying...")
                time.sleep(2)  # Adding a delay before retrying
            else:
                logger.debug("Max retries reached, terminating job.")
                terminate_running_job()
                raise RobbieException(f"Failed to make request to {url} after {retries} attempts.")


'''_______________________________________________________________________________________
    
    RUN!
    ______________________________________________________________________________________
'''
def run():
    global headers

    headers = {
        "PositronJobId": runner_env.JOB_ID,
        "SystemAuthenticationKey": runner_env.SYSTEM_AUTHENTICATION_KEY,
    }

    try:
        # 1. Get the job details
        get_job()

        if is_job_active():
            # 2. Update status to initializing
            update_job(status=job_statuses["initializing"], start_date=datetime.now(timezone.utc))

            # 3. Unpack workspace tar
            if is_job_active():
                unpack_workspace_from_s3()

                # 4. Run the job (including dependency install)
                if is_job_active():
                    run_job()

                    # 5. Update status to Storing
                    update_job(status=job_statuses['storing'])

                    # 6. Upload results
                    upload_results_to_s3()

        # 7. Get the completed job details
        get_job()
        # 8. Update status to success or error
        finish_job()

    except Exception as e:
        logger.error(f'Job stopped. An exception occurred: {str(e)}.')
        logger.end_of_logs_signal()
        raise e

        
