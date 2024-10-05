import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def msk():
    """
    Shoot the portal gun
    """
    typer.echo("hidekimsk")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading")
