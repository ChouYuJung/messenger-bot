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


@msgbot.command()
def subs():

    from msg_bot.events import on_message_create
    from msg_bot.subscribe import topicfilter_subs_all_msg_events
    from msg_bot.utils.pubsub import SubscriptionManager

    with SubscriptionManager() as subs:
        subs.add_subscription(topicfilter_subs_all_msg_events, on_message_create)
        subs.wait_for_all_events()
