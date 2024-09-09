import click


@click.group()
def msgbot():
    """Command line interface for msg-bot."""
    pass


@msgbot.command()
def subs():

    from msg_bot.events import on_message_create
    from msg_bot.subscribe import topicfilter_subs_all_msg_events
    from msg_bot.utils.pubsub import SubscriptionManager

    with SubscriptionManager() as subs:
        subs.add_subscription(topicfilter_subs_all_msg_events, on_message_create)
        subs.wait_for_all_events()


@msgbot.command()
def chat():
    """Send a message to chat."""

    from msg_bot.publish import publish_message
    from msg_bot.schemas.messages import Message, MessageType
    from msg_bot.utils.common import gen_id
    from msg_bot.utils.pubsub import MQTTConnectionManager, get_topic

    msg_create_topic = get_topic(
        "msg",
        "create",
        org_id=gen_id("org"),
        conv_id=gen_id("conv"),
        msg_id=gen_id("msg"),
    )

    with MQTTConnectionManager() as mqtt_connection:
        while True:
            try:
                msg_text = click.prompt("Press Enter to send a message")
                msg_text = msg_text.strip()
                if not msg_text:
                    continue

                msg_model = Message.model_validate(
                    {
                        "content": msg_text,
                        "sender_id": gen_id("usr"),
                        "conversation_id": gen_id("conv"),
                        "message_type": MessageType.TEXT,
                    }
                )
                publish_message(mqtt_connection, msg_create_topic, msg_model)

            except click.exceptions.Abort:
                click.echo("Aborted!")
                return
