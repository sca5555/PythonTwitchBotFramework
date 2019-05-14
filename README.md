Donate to original author here: [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9ZVUE7CR24738)

# PythonTwitchBotFramework
working twitchbot framework made in python 3.6+

# Quick Links
* [Quick Start](#quick-start)
* [Overriding Events](#overriding-events)
* [Adding Commands](#adding-commands)
* [SubCommands](#subcommands)
* [DummyCommands](#dummycommands)
* [Permissions](#permissions)
  * [Using Chat Commands](#managing-permissions-using-chat-commands)
  * [Editing The Config](#managing-permission-by-editing-the-configs)
* [Reloading Permissions](#reloading-permissions)
* [Command Server](#command-server)
* [Command Console](#command-console)

# basic info
This is a fully async twitch bot framework complete with:

* builtin command system using decorators
* overridable events (message received, whisper received, ect)
* full permission system that is individual for each channel
* message timers 
* quotes 
* custom commands
* builtin economy 


# Quick Start

the minimum code to get the bot running is this:
```python
from twitchbot.bots import BaseBot

if __name__ == '__main__':
    BaseBot().run()

```

this will start the bot. 

if you have a folder with your own custom commands you can load
the .py files in it with:
```python
from twitchbot import BaseBot, load_commands_from_directory

if __name__ == '__main__':
    load_commands_from_directory('PATH/TO/DIRECTORY')
    BaseBot().run()

```

# Overriding Events

the bots events are overridable via the following 2 ways:

1) using decorators:

```python
from twitchbot import override_event, Event, Message

@override_event(Event.on_privmsg_received)
async def on_privmsg_received(msg: Message):
    print(f'{msg.author} sent message {msg.content} to channel {msg.channel_name}')

```

2) subclassing BaseBot
```python
from twitchbot import BaseBot, Message
class MyCustomTwitchBot(BaseBot):
    async def on_privmsg_received(self, msg: Message):
        print(f'{msg.author} sent message {msg.content} to channel {msg.channel_name}')


```
then you would use MyCustomTwitchBot instead of BaseBot:
```python
MyCustomTwitchBot().run()
```

* all overridable events are:
```python
from twitchbot import Event

Event.on_after_command_execute : (self, msg: Message, cmd: Command)
Event.on_before_command_execute : (self, msg: Message, cmd: Command)
Event.on_bits_donated : (self, msg: Message, bits: int)
Event.on_channel_joined : (self, channel: Channel)
Event.on_connected : (self)
Event.on_privmsg_received : (self, msg: Message)
Event.on_privmsg_sent : (self, msg: str, channel: str, sender: str)
Event.on_whisper_received : (self, msg: Message)
Event.on_privmsg_sent : (self, msg: str, receiver: str, sender: str)
Event.on_raw_message : (self, msg: Message)
Event.on_user_join : (self, user: str, channel: Channel)
Event.on_user_part : (self, user: str, channel: Channel)
```


if this is the first time running the bot it will generate a folder
named `configs`. 

inside is `config.json` which you put the authentication into

as the bot is used it will also generate channel permission files 
in the `configs` folder

# Adding Commands

to register your own commands use the Command decorator:

* using decorators
```python
from twitchbot import Command

@Command('COMMAND_NAME')
async def cmd_function(msg, *args):
    await msg.reply('i was called!')
```
* you can also limit the commands to be whisper or channel chat only 
(default is channel chat only)
```python
from twitchbot import Command, CommandContext

# other options are CommandContext.BOTH and CommandContext.WHISPER
@Command('COMMAND_NAME', context=CommandContext.CHANNEL) # this is the default command context
async def cmd_function(msg, *args):
    await msg.reply('i was called!')
```
* you can also specify if a permission is required to be able to call
the command (if no permission is specified anyone can call the command):

```python
from twitchbot import Command

@Command('COMMAND_NAME', permission='PERMISSION_NAME')
async def cmd_function(msg, *args):
    await msg.reply('i was called!')
```

* you can also specify a help/syntax for the command for the help chat command to give into on it:
```python
from twitchbot import Command, Message

@Command('COMMAND_NAME', help='this command does a very important thing!', syntax='<name>')
async def cmd_function(msg: Message, *args):
    await msg.reply('i was called!')
```
so when you do `!help COMMAND_NAME`

it will this in chat:
```
help for "!command_name", 
syntax: "<name>", 
help: "this command does a very important thing!"
```

# SubCommands

the SubCommand class makes it easier to implement different actions based on a parameters passed to a command.

its the same as normal command except thats its not a global command

example: `!say` could be its own command, then it could have the sub-commands `!say myname` or `!say motd`.

you can implements this using something like this:

```python
from twitchbot import Command

@Command('say')
async def cmd_say(msg, *args):
    # args is empty
    if not args:
        await msg.reply("you didn't give me any arguments :(")
        return 
    
    arg = args[0].lower()
    if arg == 'myname':
        await msg.reply(f'hello {msg.mention}!')
    
    elif arg == 'motd':
        await msg.reply('the message of the day is: python is awesome')
    
    else:    
        await msg.reply(' '.join(args))
    

```
 
that works, but i would be done in a nicer way using the `SubCommand` class:

```python
from twitchbot import Command, SubCommand

@Command('say')
async def cmd_say(msg, *args):
    await msg.reply(' '.join(args))

# we pass the parent command as the first parameter   
@SubCommand(cmd_say, 'myname')
async def cmd_say_myname(msg, *args):
    await msg.reply(f'hello {msg.mention}!')


@SubCommand(cmd_say, 'motd')
async def cmd_say_motd(msg, *args):
    await msg.reply('the message of the day is: python is awesome')
```

both ways do the same thing, what you proffer to use is up to you, but it does make it easier to manage for larger commands to use SubCommand class

# DummyCommands
this class is basically a command that does nothing when executed, its mainly use is to be used as base command for sub-command-only commands

it has all the same options as a regular Command

when a dummy command is executed it looks for sub-commands with a matching name as the first argument passed to it

if no command is found then it will say in chat the available sub-commands

but if a command is found it executes that command


say you want a command to greet someone, but you always want to pass the language, you can do this:

```python
from twitchbot import DummyCommand, SubCommand

# cmd_greet does nothing itself when called
cmd_greet = DummyCommand('greet')

@SubCommand(cmd_greet, 'english')
async def cmd_greet_english(msg, *args):
    await msg.reply(f'hello {msg.mention}!')
    
@SubCommand(cmd_greet, 'spanish')
async def cmd_greet_spanish(msg, *args):
    await msg.reply(f'hola {msg.mention}!')
```

doing just `!greet` when make the bot say: 
```text
command options: {english, spanish}
```

doing `!greet english` will make the bot say this:
```text
hello @johndoe!
```

doing `!greet spanish` will make the bot say this:
```text
hola @johndoe!
```

# Config

the default config values are:
```json
{
  "oauth": "oauth:",
  "client_id": "CLIENT_ID",
  "nick": "nick",
  "prefix": "!",
  "default_balance": 200,
  "owner": "BOT_OWNER_NAME",
  "channels": [
    "channel"
  ],
  "loyalty_interval": 60,
  "loyalty_amount": 2,
  "command_server_enabled": true,
  "command_server_port": 1337,
  "command_server_host": "localhost"
}

```

`oauth` is the twitch oauth used to login  

`client_id` is the client_id used to get info like channel title, ect ( this is not required but twitch API info will not be available without it )

`nick` is the twitch accounts nickname

`prefix` is the command prefix the bot will use for commands that 
dont use custom prefixes

`default_balance `is the default balance for new users that dont
already have a economy balance

`owner` is the bot's owner

`channels` in the twitch channels the bot will join

`loyalty_interval` the interval for which the viewers will given currency for watching the stream, gives amount specified by `loyalty_amount`

`loyalty_amount` the amount of currency to give viewers every `loyalty_interval`

`command_server_enabled` specifies if the command server should be enabled (see [Command Server](#command-server) for more info)

`command_server_port` the port for the command server

`command_server_host` the host name (address) for the command server

# Permissions

the bot comes default with permission support

there are two ways to manage permissions,

1. using chat commands 
2. editing JSON permission files

## managing permissions using chat commands
to add a permission group: `!addgroup <group>`, ex: `!addgroup donators`

to add a member to a group: `!addmember <group> <user>`, ex: 
`!addmember donators johndoe`

to add a permission to a group: `!addperm <group> <permission>`, ex: 
`!addperm donators slap`

to remove a group: `!delgroup <group>`, ex: `!delgroup donators`

to remove a member from a group: `!delmember <group> <member>`, ex: 
`!delmember donators johndoe`

to remove a permission from a group: `!delperm <group> <permission>`, ex:
`!delperm donators slap`

## managing permission by editing the configs

find the `configs` folder the bot generated (will be in same directory as the 
script that run the bot)

inside you will find `config.json` with the bot config values required for 
authentication with twitch and such

if the bot has joined any channels then you will see file names
that look like `CHANNELNAME_perms.json`

for this example i will use a `johndoe`

so if you open `johndoe_perms.json` you will see this if you 
have not changed anything in it:

```json
{
  "admin": {
    "name": "admin",
    "permissions": [
      "*"
    ],
    "members": [
      "johndoe"
    ]
  }
}
```

`name` is the name of the permission group

`permissions` is the list of permissions the group has
("*" is the "god" permission, granting access to all bot commands)

`members` is the members of the group

to add more permission groups by editing the config 
you can just copy/paste the default one 
(be sure to remove the "god" permission if you dont them 
having access to all bot commands)

so after copy/pasting the default group it will look like this
 (dont forget to separate the groups using `,`):
 
 
```json
{
  "admin": {
    "name": "admin",
    "permissions": [
      "*"
    ],
    "members": [
      "johndoe"
    ]
  },
  "donator": {
    "name": "donator",
    "permissions": [
      "slap"
    ],
    "members": [
      "johndoe"
    ]
  }
}
```

# Reloading Permissions

if the bot is running be sure to do `!reloadperms` to load
the changes to the permission file

# Command Server
The command server is a small Socket Server the bot host that lets the Command Console be able to make the bot send messages given to it through a console. (see [Command Console](#command-console))

The server can be enabled or disabled through the config (see [Config](#config)), the server's port and host are specified by the config file


# Command Console
If the [Command Server](#command-server) is disabled in the [config](#config) the Command Console cannot be used

The Command Console is used to make the bot send chat messages and commands

To launch the Command Console make sure the bot is running, and the [Command Server](#command-server) is enabled in the [Config](#config), 

after verifying these are done, simply do `python command_console.py` to open the console, upon opening it you will be prompted to select a twitch channel that the bot is currently connected to.

after choose the channel the prompt changes to `(CHANNEL_HERE):` and you are now able to send chat messages / commands to the choosen channel by typing your message and pressing enter

