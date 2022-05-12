import telebot
import time
from isdayoff import DateType, ProdCalendar
import asyncio
import schedule
from threading import Thread
import os
import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

expected_hour = 12
expected_minute = '00'
gmt = 3


class ObedBot:
    def __init__(self):
        logger.debug('Initialize bot')
        self._token = os.environ['API_TOKEN']
        self._chat_id = os.environ['CHAT_ID']
        self.bot = telebot.TeleBot(self._token)
        self.calendar = ProdCalendar(locale='ru')
        self._its_time = False
        self._offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        self._delta = self._offset // 60 // 60 * -1
        self._real_hour = expected_hour - self._delta + gmt
        self.real_hour_str = str(self._real_hour) + f":{expected_minute}"
        logger.debug(f"Real time to send is {self.real_hour_str}")

    async def main(self):
        while True:
            if self._its_time:
                if await self.calendar.today() == DateType.WORKING:
                    logger.debug('Bot send photo and vote')
                    self.bot.send_photo(self._chat_id, open('photo.jpg', 'rb'))
                    self.bot.send_poll(self._chat_id, "А ты идешь на обэд?", ['да', 'нет'], is_anonymous=False)
                self._its_time = False
            time.sleep(60)

    def set_flag(self):
        logger.debug('Set time flag. Now its the time!')
        self._its_time = True


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    bot = ObedBot()
    try:
        logger.debug('Set schedule task')
        schedule.every().day.at(bot.real_hour_str).do(bot.set_flag)
        Thread(target=schedule_checker, daemon=True).start()
        logger.debug('Run bot')
        loop = asyncio.get_event_loop()
        loop.create_task(bot.main())
        loop.run_forever()
    except Exception as e:
        logger.error(e)