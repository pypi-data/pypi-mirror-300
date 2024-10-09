import time
from .config import PositronJob
from .cli.console import console, ROBBIE_ORANGE, ROBBIE_GREEN, ROBBIE_GREY
from rich.text import Text
from rich.panel import Panel
from rich import box

def print_robbie_configuration_banner(job: dict, job_config: PositronJob):
    text = Text()
    text.append("Funding Source: ", style=ROBBIE_GREEN)
    text.append(f"{job['fundingGroupName']} ({job['fundingGroupId']})\n", style=ROBBIE_GREY)
        
    text.append("Hardware: ", style=ROBBIE_GREEN)
    text.append(f"{job['environmentName']} ({job['environmentId']})\n", style=ROBBIE_GREY)
        
    text.append("Image: ", style=ROBBIE_GREEN)
    text.append(f"{job['imageName']}\n", style=ROBBIE_GREY)
        
    text.append("Workspace Directory: ", style=ROBBIE_GREEN)
    text.append(f"{job_config.workspace_dir}\n", style=ROBBIE_GREY) 
    text.append("Max Token Consumption: ", style=ROBBIE_GREEN)
    if not job["maxUsableTokens"]:
        text.append("Not specified\n", style=ROBBIE_GREY)
    else:
        text.append(f"{job['maxUsableTokens']}\n", style=ROBBIE_GREY)

    text.append("Max Execution Time (minutes): ", style=ROBBIE_GREEN)

    if not job["maxExecutionMinutes"]:
        text.append("Not specified\n", style=ROBBIE_GREY)
    else:
        text.append(f"{job['maxExecutionMinutes']}\n", style=ROBBIE_GREY)
    
    text.append("Environment Variables: ", style=ROBBIE_GREEN)

    if not job_config.env:
         text.append("None specified\n", style=ROBBIE_GREY)
    else:
        text.append(f"{job_config.env}\n", style=ROBBIE_GREY)


    if job_config.commands:
        text.append("Shell Commands:  \n", style=ROBBIE_GREEN)
        for cmd in job_config.commands:
            text.append(f'{cmd}\n', style=ROBBIE_GREY)
    
    if job_config.entry_point:
        text.append("Entry Point: ", style=ROBBIE_GREY)
        text.append(f"{job_config.entry_point}\n", style=ROBBIE_GREY)

    console.print(Panel(
        text,
        box=box.ROUNDED,
        # padding=(1, 2),
        title = Text(f"Robbie Job Configuration ({job['tokenRatePerHour']} tokens/hour)", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))

def print_job_details_banner(job: dict):
    ## print job details
    text = Text()
    text.append("Job Name: ", style=ROBBIE_GREEN)
    text.append(f"{job['name']}\n")
            
    text.append("Job ID: ", style=ROBBIE_GREEN)
    text.append(f"{job['id']}\n")
        
    text.append("Start Time: ", style=ROBBIE_GREEN)
    text.append(f"{time.asctime()}")

    console.print(Panel(
        text,
        box=box.ROUNDED,
        title=Text("Job Details", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))
    
# prints a rich job completion banner
def print_job_complete_banner(job: dict, start):
    ## print job details
    text = Text()
    text.append("Job Name: ", style=ROBBIE_GREEN)
    text.append(f"{job['name']}\n")
            
    text.append("Total time: ", style=ROBBIE_GREEN)
    text.append(f"{time.perf_counter() - start:.2f} seconds.\n")
        
    text.append("Tokens consumed: ", style=ROBBIE_GREEN)
    text.append(f"{job['tokensUsed']}\n")
        
    text.append("RESULT: ")
    if(job['status'] == "complete"):
        text.append(f"Success", style="green")
    else:
        text.append(f"{job['status']}", style="red")
                
    console.print(Panel(
        text,
        box=box.ROUNDED,
        # padding=(1, 2),
        title=Text("Job Complete", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))