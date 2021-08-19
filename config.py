import sys

import toml
from toml import TomlDecodeError

try:
    with open('config.toml') as file:
        config = toml.load(file)

        TOKEN = config['bot']['token']
        PREFIX = config['bot']['prefix']

        OWNER_ID = config['ids']['owner_id']
        SERVER_ID = config['ids']['server_id']

        ADMIN_ROLE_ID = config['ids']['admin_role_id']

        LOBBY_CHANNEL_ID = config['ids']['lobby_channel_id']

        AUTO_UNHOST_TIMEOUT = config['durations']['auto_unhost_timeout']

except FileNotFoundError:
    print("Config file not found.\nDo you have a file named config.toml in the projects root directory?")
    sys.exit(1)
except (TomlDecodeError, KeyError):
    print("Invalid config file.")
    sys.exit(1)
