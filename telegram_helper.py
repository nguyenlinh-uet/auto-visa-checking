import logging

import telegram

logger = logging.getLogger(__name__)

BOT_TOKEN = "5881546052:AAGFPdrG5KQqa_sWHs1MwsAPU2p3rNpEd8Q"

bot = telegram.Bot(token=BOT_TOKEN)


async def send_message_text(chat_id: str, message: str) -> bool:
    status = True
    try:
        await bot.sendMessage(chat_id=chat_id, text=message)
    except Exception as e:
        status = False
        logger.error(f"Error when sending message to telegram: {e}")
    return status
