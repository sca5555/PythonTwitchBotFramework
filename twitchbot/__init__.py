from .arena import *
from .channel import *
from twitchbot.api.chatters import *
from .colors import *
from .command import *
from .config import *
from .enums import *
from .irc import *
from .message import *
from .permission import *
from .ratelimit import *
from .regex import *
from .util import *
from .database import *
from .bots import *
from .api import *
from .overrides import *
from .loyalty_ticker import *
from .disabled_commands import *
from .duel import *
from .command_server import start_command_server
from .modloader import *
from .disabled_mods import *

import os

load_commands_from_directory(os.path.join(__path__[0], 'builtin_commands'))
load_mods_from_directory(os.path.join(__path__[0], 'builtin_mods'))
load_mods_from_directory(os.path.abspath(cfg.mods_folder))
ensure_mods_folder_exists()
start_command_server()
