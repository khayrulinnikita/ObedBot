# ObedBot

Telegram bot to automatically send lunchtime voting on weekdays.

## Features

- Send voting at 12:00 p.m.
- Send Uncle Sam photo.

## Docker

```sh
git clone https://github.com/khayrulinnikita/ObedBot.git
cd ObedBot
docker build -t obed_bot .
docker run -e API_TOKEN=<API_TOKEN> \
           -e CHAT_ID=<CHAT_ID> \
           -d obed_bot
```

## License

MIT

**Free Software, Hell Yeah!**