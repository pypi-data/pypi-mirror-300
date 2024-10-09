from pydantic import BaseModel
from typing import List, Optional

class PositronCLIArgs(BaseModel):
    """
    Positron CLI command line arguments.
    """
    is_init: bool = False
    local: bool = False
    deploy: bool = False
    stream_stdout: bool = False
    debug: bool = False
    job_args: Optional[List[str]] = None
    skip_prompts: bool = False
    monitor_status: bool = False
    commands_to_run: str | None = None
    interactive: bool = False
    create_only: bool = False
    results_from_job_id: str = ""

    def init(self,
        local: bool = False,
        deploy: bool = False,
        stream_stdout: bool = False,
        debug: bool = False,
        job_args: Optional[List[str]] = None,
        skip_prompts: bool = False,
        monitor_status: bool = False,
        commands_to_run: str | None = None,
        interactive: bool = False,
        create_only: bool = False,
        results_from_job_id: str = "",
    ):
        if self.is_init:
            raise ValueError('CLI Args already initialized')
        
        self.local = local
        self.deploy = deploy
        self.stream_stdout = stream_stdout
        self.debug = debug
        self.job_args = job_args
        self.is_init = True
        self.skip_prompts=skip_prompts
        self.monitor_status=monitor_status
        self.commands_to_run = commands_to_run
        self.interactive = interactive
        self.create_only = create_only
        self.results_from_job_id = results_from_job_id


#
# Export global (singleton)
#
args = PositronCLIArgs()
"""
Global CLI arguments singleton, make sure you call init() before using it.
"""
