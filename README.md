Creates a Telegram bot https://core.telegram.org/bots

- resumes processing messages where it left off
- commands:
  - /ping - Sends a pong

```
sudo apt-get install python3-pip
pip3 install --user virtualenv
~/.local/bin/virtualenv -p python3 myenv
source myenv/bin/activate

pip3 install -r requirements.txt

python3 telegram-bot.py
```

With Docker:
```
docker build -t telegram-bot .
docker run telegram-bot
```
