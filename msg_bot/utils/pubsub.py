import json
from contextlib import AbstractContextManager
from typing import Callable, Literal, ParamSpec, Text, TypeVar

import awscrt.mqtt
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from rich import print
from rich.style import Style
from rich.text import Text as RichText

from msg_bot.config import settings

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


def get_topic(
    topic_type: Literal["root", "org", "conv", "msg"],
    operation: Literal[
        "create", "update", "delete", "bulk_create", "bulk_update", "bulk_delete"
    ],
    field: Text | None = None,
    *,
    org_id: Text | None = None,
    conv_id: Text | None = None,
    msg_id: Text | None = None,
    topic_base: Text = settings.TOPIC_BASE,
    topic_path_org: Text = settings.TOPIC_PATH_ORG,
    topic_path_conv: Text = settings.TOPIC_PATH_CONV,
    topic_path_msg: Text = settings.TOPIC_PATH_MSG,
) -> Text:
    _topic: Text
    if topic_type == "root":
        _topic = topic_base

    elif topic_type == "org":
        if org_id is None:
            raise ValueError("org_id is required for org topic")
        _topic = f"{topic_base}/{topic_path_org}/{org_id}"

    elif topic_type == "conv":
        if org_id is None or conv_id is None:
            raise ValueError("org_id and conv_id are required for conv topic")
        _topic = f"{topic_base}/{topic_path_org}/{org_id}/{topic_path_conv}/{conv_id}"

    elif topic_type == "msg":
        if org_id is None or conv_id is None or msg_id is None:
            raise ValueError("org_id, conv_id, and msg_id are required for msg topic")
        _topic = f"{topic_base}/{topic_path_org}/{org_id}/{topic_path_conv}/{conv_id}/{topic_path_msg}/{msg_id}"

    else:
        raise ValueError(f"Invalid topic type: {topic_type}")

    if operation is not None:
        _topic = f"{_topic}/{operation}"

    if field is not None:
        _topic = f"{_topic}/{field}"

    return _topic


# Callback when connection is accidentally lost.
def on_connection_interrupted(
    connection: "awscrt.mqtt.Connection", error: Exception, **kwargs
):
    print(f"Connection interrupted. error: {error}")


# Callback when an interrupted connection is re-established.
def on_connection_resumed(
    connection: "awscrt.mqtt.Connection",
    return_code: int,
    session_present: bool,
    **kwargs,
):
    print(
        f"Connection resumed. return_code: {return_code} session_present: {session_present}"
    )


def get_mqtt_connection(
    endpoint: Text = settings.AWS_IOT_CORE_ENDPOINT,
    *,
    cert_filepath: Text = settings.AWS_IOT_CORE_CERTS_FILEPATH,
    pri_key_filepath: Text = settings.AWS_IOT_CORE_SECRET_KEY_FILEPATH,
    ca_filepath: Text = settings.AWS_IOT_CORE_CA_FILEPATH,
    client_id: Text = settings.AWS_IOT_CORE_CLIENT_ID,
) -> "awscrt.mqtt.Connection":
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=cert_filepath,
        pri_key_filepath=pri_key_filepath,
        client_bootstrap=client_bootstrap,
        ca_filepath=ca_filepath,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=6,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
    )

    print(f"Connecting to '{endpoint}' with client ID '{client_id}' ...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected!")

    return mqtt_connection


def publish_message(
    mqtt_connection: "awscrt.mqtt.Connection", topic: Text, message: Text
):
    # Publish message to server desired number of times.
    rich_text = (
        RichText("Publishing message to topic '")
        + RichText(topic, style=Style(color="cyan"))
        + RichText("': ")
        + RichText(message, style=Style(color="green"))
    )
    print(rich_text)
    mqtt_connection.publish(
        topic=topic,
        payload=json.dumps({"message": message}),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )


def disconnect(mqtt_connection: "awscrt.mqtt.Connection"):
    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")


class MQTTConnectionManager(AbstractContextManager):
    def __init__(
        self,
        connection_builder: Callable[
            ..., "awscrt.mqtt.Connection"
        ] = get_mqtt_connection,
    ):
        self._connection = connection_builder()

    def __enter__(self):
        return self._connection

    def __exit__(self, exc_type, exc_value, traceback):
        # Disconnect the MQTT connection when exiting the context
        disconnect(self._connection)
