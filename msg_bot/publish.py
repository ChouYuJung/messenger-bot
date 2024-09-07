import time

from ksuid import Ksuid

from msg_bot.config import fake
from msg_bot.utils.pubsub import MQTTConnectionManager, get_topic, publish_message


def main():
    with MQTTConnectionManager() as mqtt_connection:
        for _ in range(3):
            publish_message(
                mqtt_connection,
                get_topic(
                    "msg",
                    "create",
                    org_id=f"org_{Ksuid()}",
                    conv_id=f"conv_{Ksuid()}",
                    msg_id=f"msg_{Ksuid()}",
                ),
                fake.text(),
            )
            time.sleep(1)


if __name__ == "__main__":
    main()
