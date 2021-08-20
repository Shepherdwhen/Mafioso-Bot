#!/usr/bin/env python3

from discord.ext import commands

import globvars
from config import OWNER_ID, PREFIX, TOKEN

globvars.client = commands.Bot(
    owner_id=OWNER_ID,
    command_prefix=PREFIX, # Might be an array
    case_insensitive=True
)

globvars.client.load_extension('listeners')

globvars.client.run(TOKEN)
