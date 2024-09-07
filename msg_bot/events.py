from typing import Text

from rich.style import Style
from rich.text import Text as RichText

from msg_bot.config import console


def on_message_create(topic: Text, payload: bytes, **kwargs):
    console.print(
        RichText("Received message from topic '")
        + RichText(topic, style=Style(color="cyan"))
        + RichText("': ")
        + RichText(str(payload), style=Style(color="magenta"))
    )
