from typing import Text

import awscrt.mqtt
from awscrt import mqtt
from rich.style import Style
from rich.text import Text as RichText

from msg_bot.config import console
from msg_bot.schemas.messages import Message


def publish_message(
    mqtt_connection: "awscrt.mqtt.Connection", topic: Text, message: "Message"
):
    # Publish message to server desired number of times.
    rich_text = (
        RichText("Publishing message to topic '")
        + RichText(topic, style=Style(color="cyan"))
        + RichText("': ")
        + RichText(message.content, style=Style(color="green"))
    )
    console.print(rich_text)
    mqtt_connection.publish(
        topic=topic,
        payload=message.model_dump_json().encode("utf-8"),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )
