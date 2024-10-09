import typer
from positron_cli.run import run
from positron_cli.login import login
from positron_cli.set_env import set_env
from positron_cli.configure import configure
from rich import print
import pyfiglet
  
ascii_banner = pyfiglet.figlet_format("Robbie")
print(ascii_banner)
app = typer.Typer(help="A CLI tool to help you run your code in the Robbie")

app.command()(run)
app.command()(login)
app.command()(set_env)
app.command()(configure)

if __name__ == "__main__":
    app()
