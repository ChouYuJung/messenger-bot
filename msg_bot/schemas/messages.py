import time
from typing import Dict, List, Optional, Text

from pydantic import BaseModel, Field

from msg_bot.utils.common import gen_id


class Message(BaseModel):
    id: Text = Field(default_factory=lambda: gen_id("msg"))
    content: Text
    sender_id: Text
    conversation_id: Text
    message_type: Text
    reply_to: Optional[Text] = Field(default=None)
    is_edited: bool = Field(default=False)
    metadata: Optional[Dict] = Field(default=None)
    reactions: Optional[List[Dict]] = Field(default=None)
    created_at: int = Field(default_factory=lambda: int(time.time()))
    updated_at: Optional[int] = Field(default=None)
