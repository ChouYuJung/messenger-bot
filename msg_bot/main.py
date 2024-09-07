import click


@click.group()
def msgbot():
    """Command line interface for msg-bot."""
    pass


@msgbot.command()
@click.argument("message")
def chat(message):
    """Send a message to chat."""
    click.echo(f"Sending message: {message}")
