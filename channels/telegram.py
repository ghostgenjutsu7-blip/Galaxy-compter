"""channels/telegram.py — Telegram channel adapter.

§7, §25 Phase 5 ㉒. A thin adapter: translates Telegram messages into the same
internal input the CLI produces, and translates Goal-mode updates back out as
message edits/replies. Galaxy processes Telegram input through the same
Orchestrator pipeline — there's no separate Telegram logic.

Library: python-telegram-bot (>=21.0). Lazily imported so the rest of Galaxy
runs without it. Setup via /channel add: Galaxy gives a @BotFather link, the
user pastes the bot token, Galaxy tests the connection, the user picks access
control (only me / specific IDs / open).
"""
from __future__ import annotations

import json
from typing import Any

from core.agent.base_agent import new_id
from storage.local import get_storage


class TelegramChannel:
    """One Telegram bot connection."""

    def __init__(self) -> None:
        self.token: str = ""
        self.allowed_user_ids: list[int] | None = None  # None = open
        self._bot: Any = None
        self._app: Any = None
        self._running = False
        self._load()

    def _load(self) -> None:
        st = get_storage()
        try:
            row = st.query_one("SELECT * FROM channels WHERE kind='telegram' LIMIT 1;")
            if row:
                from security.secrets_fallback import decrypt_secret
                self.token = decrypt_secret(row.get("token") or "")
                self.allowed_user_ids = json.loads(row.get("allowed_user_ids") or "null")
        except Exception:
            pass

    def configure(self, token: str, allowed_user_ids: list[int] | None = None) -> dict:
        """Set the bot token + access control. Tests the connection."""
        self.token = token
        self.allowed_user_ids = allowed_user_ids
        from security.secrets_fallback import encrypt_secret
        st = get_storage()
        cid = new_id("channel-tg-")
        try:
            with st.transaction() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO channels(id,kind,token,allowed_user_ids,configured_at) "
                    "VALUES(?,?,?,?,?);",
                    (cid, "telegram", encrypt_secret(token), json.dumps(allowed_user_ids), __import__("time").time()),
                )
        except Exception:
            pass
        # test connection
        test = self.test_connection()
        return {"ok": test["ok"], "error": test.get("error"), "configured": test["ok"]}

    def test_connection(self) -> dict:
        if not self.token:
            return {"ok": False, "error": "no token set"}
        try:
            import httpx
            r = httpx.get(f"https://api.telegram.org/bot{self.token}/getMe", timeout=10.0)
            data = r.json()
            if data.get("ok"):
                bot = data["result"]
                return {"ok": True, "bot_username": bot.get("username", "")}
            return {"ok": False, "error": data.get("description", "unknown error")}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def is_allowed(self, user_id: int) -> bool:
        if self.allowed_user_ids is None:
            return True  # open
        return user_id in self.allowed_user_ids

    async def start(self, on_message) -> None:
        """Start polling. on_message(text, user_id) is called for each allowed
        message. Requires python-telegram-bot installed."""
        if self._running:
            return
        try:
            from telegram.ext import (
                ApplicationBuilder,
                CommandHandler,
                MessageHandler,
                filters,
            )
        except Exception as e:
            raise RuntimeError(f"python-telegram-bot not installed: {e}")

        async def handle(update, context):
            if not update.message or not update.message.text:
                return
            uid = update.effective_user.id
            if not self.is_allowed(uid):
                await update.message.reply_text("Not authorized.")
                return
            response = await on_message(update.message.text, uid)
            if response:
                await update.message.reply_text(response)

        app = ApplicationBuilder().token(self.token).build()
        app.add_handler(CommandHandler("start", handle))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
        self._app = app
        self._running = True
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

    async def stop(self) -> None:
        if self._app and self._running:
            try:
                await self._app.updater.stop()
                await self._app.stop()
                await self._app.shutdown()
            except Exception:
                pass
        self._running = False


_tg: TelegramChannel | None = None


def get_telegram_channel() -> TelegramChannel:
    global _tg
    if _tg is None:
        _tg = TelegramChannel()
    return _tg
