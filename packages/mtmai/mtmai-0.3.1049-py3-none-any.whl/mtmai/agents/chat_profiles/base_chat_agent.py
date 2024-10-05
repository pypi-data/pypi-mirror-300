from abc import ABC


class ChatAgentBase(ABC):
    """
    聊天机器人基础类
    """
    def __init__(
        self,
        name: str,
    ):
        self.name = name
