import asyncio
import logging
import time
from datetime import datetime

import bs4
import requests
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent

from logger_helper import set_dict_config
from telegram_helper import send_message_text

set_dict_config()
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    checking_url = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"
    software_names = [SoftwareName.CHROME.value, SoftwareName.BRAVE.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.MACOS.value, OperatingSystem.ANDROID.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    err_cnt = 0
    loop = asyncio.get_event_loop()
    while err_cnt < 10:
        try:
            response = requests.get(checking_url, headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,ja;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'WSS_FullScreenMode=false',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user_agent_rotator.get_random_user_agent(),
            }, timeout=10)
            logger.info(f"Response status: {response.status_code}")
            soup = bs4.BeautifulSoup(response.text, "lxml")
            elms = soup.select(
                "#tab-pane-1 > div.container > div.row > div.content-main > div.ms-rtestate-field > table > tbody > tr"
            )
            text_status = None
            time_now = datetime.now()
            if elms and len(elms) > 0:
                for elm in elms:
                    country = elm.select_one("td:nth-child(1)")
                    if country and "Vietnam" in country.text:
                        status = elm.select_one("td:nth-child(2) > span")
                        if status and status.text:
                            text_status = status.text
                        break
            if text_status:
                opened = True if 'suspended' not in text_status.lower() else False
                message = f"{'✅' if opened else '🛑'}{datetime.now().isoformat()}: Current status of apply visa process is \"{text_status}\""
                logger.info(message)
                if opened:
                    loop.run_until_complete(
                        send_message_text(
                            chat_id="-806984740",
                            message=message
                        )
                    )
                    break
            err_cnt = 0
        except Exception as e:
            logger.error(e)
            err_cnt += 1
        time.sleep(30)
    loop.run_until_complete(send_message_text(
        message=f"❌{datetime.now().isoformat()}: Tool stopped, please check",
        chat_id="-806984740"
    ))
