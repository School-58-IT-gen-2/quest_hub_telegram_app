FROM python:3.12-slim

WORKDIR /tgbot
COPY bot ./bot
COPY requirements.txt ./requirements.txt
COPY assets ./assets

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f https://questhub.pro/health || exit 1

ENTRYPOINT [ "python3", "bot/run_bot.py" ]