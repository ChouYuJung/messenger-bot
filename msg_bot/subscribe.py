import awscrt.mqtt

from msg_bot.config import settings
from msg_bot.utils.pubsub import subscribe

topicfilter_subs_all_org_events = "{topic_base}/{topic_path_org}/+/#".format(
    topic_base=settings.TOPIC_BASE, topic_path_org=settings.TOPIC_PATH_ORG
)
topicfilter_subs_all_conv_events = (
    "{topic_base}/{topic_path_org}/+/{topic_path_conv}/+/#"
).format(
    topic_base=settings.TOPIC_BASE,
    topic_path_org=settings.TOPIC_PATH_ORG,
    topic_path_conv=settings.TOPIC_PATH_CONV,
)
topicfilter_subs_all_msg_events = (
    "{topic_base}/{topic_path_org}/+/{topic_path_conv}/+/{topic_path_msg}/+/#"
).format(
    topic_base=settings.TOPIC_BASE,
    topic_path_org=settings.TOPIC_PATH_ORG,
    topic_path_conv=settings.TOPIC_PATH_CONV,
    topic_path_msg=settings.TOPIC_PATH_MSG,
)
