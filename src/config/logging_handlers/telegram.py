"""Telegram logger."""

import asyncio
import logging
import re

from aiogram import Bot


class TelegramHandler(logging.Handler):
    """Telegram logger."""

    def __init__(
        self,
        project_name,
        backend_url,
        bot_token,
        chat_id,
        container_name,
    ):
        """Init TelegramHandler."""
        super().__init__()
        self._bot_token = bot_token
        self._project_name = project_name
        self._backend_url = backend_url
        self._container_name = container_name
        self._chat_id = chat_id
        self._bot = Bot(token=self._bot_token)
        self._main_first_part = (
            f"Project: {self._project_name}\n"
            f"Container: {self._container_name}\n"
            f"URL: {self._backend_url}\n"
            f"Huston, we have a problem! 🚀\n"
            "- - - - -\n\n"
        )
        self._sub_first_part = ""
        self._code_prefix = "```python\n"
        self._code_suffix = "\n```"
        self._max_length = 4096
        self._tasks = []

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        if not record.exc_text:
            return

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.sent_message(str(record.exc_text)))
        self._tasks.append(task)

    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escape characters for Telegram's MarkdownV2."""
        return re.sub(r"[_*[\]()~>#+\-=|{}.!]", lambda x: "\\" + x.group(), text)

    def _build_message(self, part: str, msg_part: str) -> str:
        """Build the message with proper prefix, suffix, and escaped Markdown."""
        return self.escape_markdown(
            part + self._code_prefix + msg_part + self._code_suffix,
        )

    async def sent_message(self, msg: str) -> None:
        """Send a message to the telegram."""
        messages = []
        current_first_part = self._main_first_part
        while msg:
            msg_part = msg[
                : self._max_length
                - len(current_first_part)
                - len(self._code_prefix)
                - len(self._code_suffix)
            ]
            messages.append(self._build_message(current_first_part, msg_part))

            msg = msg[len(msg_part) :]
            current_first_part = self._sub_first_part

        for message in messages:
            await self._bot.send_message(
                chat_id=self._chat_id,
                text=message,
                parse_mode="MarkdownV2",
            )

        await self._bot.session.close()
