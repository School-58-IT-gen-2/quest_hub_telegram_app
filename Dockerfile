FROM python:3.12-slim

WORKDIR /tgbot
COPY bot ./bot
COPY requirements.txt ./requirements.txt
COPY assets ./assets

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "bot/run_bot.py" ]