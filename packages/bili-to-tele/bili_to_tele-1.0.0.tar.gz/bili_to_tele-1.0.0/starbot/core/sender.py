import asyncio
import time
from asyncio import AbstractEventLoop
from typing import Optional, List, Any, Tuple

from loguru import logger
from pydantic import BaseModel, PrivateAttr
import httpx  # 用于发送 Telegram 请求

from bili_to_tele.core.model import LiveOn, LiveOff, DynamicUpdate, Message, PushType, PushTarget
from bili_to_tele.core.room import Up
from bili_to_tele.exception import NoPermissionException
from bili_to_tele.exception.AtAllLimitedException import AtAllLimitedException
from bili_to_tele.painter.LiveReportGenerator import LiveReportGenerator
from bili_to_tele.utils import config, redis


class Bot(BaseModel):
    """
    Bot 类，支持 Telegram 推送
    """

    ups: List[Any]
    """UP 主列表"""

    bot_token: Optional[str] = None
    """Telegram 机器人的 Token"""

    chat_id: Optional[str] = None
    """Telegram 目标聊天 ID"""

    __at_all_limited: Optional[int] = PrivateAttr()
    __banned: Optional[bool] = PrivateAttr()
    __queue: Optional[List[Tuple[int, Message, int]]] = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__at_all_limited = time.localtime(time.time() - 86400).tm_yday
        self.__banned = False
        self.__queue = []

        # 注入 Bot 实例引用
        for up in self.ups:
            up.inject_bot(self)

    def clear_resend_queue(self):
        """
        清空补发队列
        """
        self.__queue.clear()

    async def send_message(self, msg: Message):
        """
        发送消息到 Telegram

        Args:
            msg: Message 实例
        """
        if not self.bot_token or not self.chat_id:
            logger.error("Telegram Bot token 或 chat ID 未配置")
            return

        send_title = "【项目通知】"  # 自定义推送标题，替换为适合您项目的内容
        push_message = msg.get_message_chains()

        # 将消息链转换为文本
        message_text = ""
        for chain in push_message:
            for element in chain:
                if isinstance(element, Plain):
                    message_text += element.text
                elif isinstance(element, At):
                    message_text += f"@{element.target}"
                elif isinstance(element, AtAll):
                    message_text += "@All"
                elif isinstance(element, Image):
                    # Telegram 不支持直接发送图片链接，需要上传图片或使用已有图片链接
                    # 这里简单地添加图片链接到消息中
                    if element.url:
                        message_text += f"[图片]({element.url})"
                    elif element.path:
                        message_text += f"[图片]({element.path})"
                    elif element.base64:
                        message_text += "[图片]"
                else:
                    # 其他元素类型
                    pass
            message_text += "\n"  # 分隔不同的消息链

        try:
            response = await httpx.post(
                url=f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                data={
                    "chat_id": self.chat_id,
                    "text": f"{send_title}\n{message_text}",
                    "parse_mode": "Markdown"  # 支持 Markdown 格式
                }
            )
            response.raise_for_status()
            logger.info(f"成功发送消息到 Telegram: {send_title}\n{message_text}")
        except httpx.HTTPError as e:
            logger.error(f"发送 Telegram 消息失败: {e}")

    def __eq__(self, other):
        # Bot 不再与 QQ 号关联，故不进行相等比较
        return False

    def __hash__(self):
        return hash(self.chat_id)