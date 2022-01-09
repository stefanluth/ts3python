# TeamSpeak 3 Python Interface

## About

This is a **very** simple pythonic interface for interacting with the TeamSpeak 3 Server Query.
<br>
I mainly made this repository to use in other projects.
I felt like others might find it useful, so I made it public.
<br><br>
There are other, **better** interfaces on GitHub, like
<a href='https://github.com/benediktschmitt'>@benediktschmitt's</a> excellent
<a href='https://github.com/benediktschmitt/py-ts3/tree/v2'>API</a> or
<a href='https://github.com/Murgeye'>@Murgeye's</a>
<a href='https://github.com/Murgeye/teamspeak3-python-api'>API</a> and
<a href='https://github.com/Murgeye/teamspeak3-python-bot'>Bot</a>.
<br>
I have resorted to writing my own versions from scratch because those projects were too big and extensive for my needs.

## How to use

### 1. Create credentials.py

Use the `credentials.example.py` as a template.

### 2. Create configuration.py (optional)

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

## Modules
The project used to be limited to the `TS3Bot` and `TS3Query` classes but as I worked on it,
I added modules I thought others would want to use as well, especially the `move_afk` module.
<br><br>
The other modules - namely `time_measurement`, `crackerbarrel_reminder`, `holiday_doodle` and `update_wordpress` -
are rather specific for my circle of friends' TS3 server:
1. We update our host banner for special occasions, an homage to Google's doodles, which is what the `holiday_doodle`
module is for.
2. Since the pandemic we have established a monthly crackerbarrel meeting at the last wednesday of each month.
We (actually just me) like to forget it, so that's what the `crackerbarrel_reminder` module is for.
3. Being a group consisting mostly of gamers, we tend to spend a lot of time online and on the server.
To keep track of our addiction, I made the `time_measurement` module. This actually was the main reason for creating the bot.
4. To display our time rankings, we used to update the description of a channel within the server itself.
To enable prettier formatting and easier accessibility we now use our WordPress website, hence the `update_wordpress` module.

I understand that these use cases are extremely specific. These modules are meant to be a source of inspiration for
others to write their own modules, tailored to their own, extremely specific, needs.

## Questions

If you have questions on how to use this repository, open an issue; I'll be happy to help.

## Suggestions

If you have feature requests e.g. commands that the TS3Bot doesn't currently support or a module you need,
just create an issue and I'll check it out. Or you can always create a pull request for me to review, if you
have written your own solution to a problem you had and think others would want it too.
<br><br>
And ~~if~~ **when** you find ways to improve the code, please open a PR and let me know about it, 
I love to learn and I know my code is far from perfect.

## License

I just copied the generic Creative Commons Zero license, because it ensures I'm not liable for anything going wrong
and I don't have to give any warranty that this stuff actually works.
