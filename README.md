# TeamSpeak 3 Python Interface

## About

This is a **very** simple pythonic interface for interacting with the TeamSpeak 3 Server Query.
<br>
I mainly made this repository to use in other projects. 
I felt like other's might find it useful, so I made it public.
<br>
<br>
There are other, **better** interfaces on GitHub, like 
<a href='https://github.com/benediktschmitt'>@benediktschmitt's</a> excellent
<a href='https://github.com/benediktschmitt/py-ts3/tree/v2'>API</a> or 
<a href='https://github.com/Murgeye'>@Murgeye's</a> 
<a href='https://github.com/Murgeye/teamspeak3-python-api'>API</a> and 
<a href='https://github.com/Murgeye/teamspeak3-python-bot'>Bot</a>.
<br>
I have resorted to writing my own versions from scratch because those projects were too big for my needs.

## How to use

### Create credentials.py

Use the `credentials.example.py` as a template.

### Create configuration.py (optional)

Use the `configuration.example.py` as a template.

### Example

All you really need to do is fill in your credentials (see above) and go for it.

```
from TS3Bot import TS3Bot
from credentials import SERVER_IP, SERVER_PORT, TELNET_LOGIN, TELNET_PW, TELNET_PORT
from configuration import BOT_NAME

bot = TS3Bot(ip=SERVER_IP,
             port=SERVER_PORT,
             login=TELNET_LOGIN,
             password=TELNET_PW,
             telnet_port=TELNET_PORT)

bot.set_bot_name(BOT_NAME)
bot.send_channel_message('Hello channel!')
bot.exit()
```

## Questions

If you have questions on how to use this repository, open an issue; I'll be happy to help.

## Suggestions

If you have feature requests e.g. commands that the TS3Bot doesn't currently support, 
just create an issue and I'll get to it. Or you can always create a pull request for me to review.

## License

I just copied the generic Creative Commons Zero license, because it ensures I'm not liable for anything 
and I don't have to give any warranty that this stuff actually works.
