import os

import click

# clear = lambda: os.system('clear')
# clear()


from . import cli

@click.group()
def cmd():
  pass


cmd.add_command(cli.askpdf)
cmd.add_command(cli.welcome)


if __name__ == "__main__":
  cmd()
