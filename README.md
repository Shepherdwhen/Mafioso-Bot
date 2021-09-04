# Mafioso bot

This bot is a simple bot designed to help hosts host games of Mafia/Werewolves on the Small Town Mafia Discord server.

You can join the server here: [https://discord.gg/ZC7nSArSFD](https://discord.gg/ZC7nSArSFD)


## Running the bot

1. Clone this repository.
2. Copy `config.toml.example` to `config.toml` and fill out the required fields.
3. Install dependancies using [poetry](https://python-poetry.org/) by running `poetry install`.
4. Run the file `main.py` with `poetry run python3 main.py` or `poetry run python main.py` (you may need to use `python3`, `py` or `py -3.6.1` instead of `python`).

## Using the bot

There are two main states to the bot:
- [The pregame state](#pregame)
- [The ingame state](#ingame)

### Pregame

During the pregame state, mods can set themselves as hosts using the `host` command, unhost using the `unhost` command, force-join players with the `fjoin <player>` command and force-quit players with the `fquit <player>` command.

Players can join with the `join` command and leave with the `quit` command.

A `list` command is availible to see signed up players and hosts.

During the pregame, players can set their emoji using the `emoji <emoji>` command. This cannot be changed in the game for consistency, and hosts can refer to players using their emoji in commands.

Once all players have signed up, hosts can transition to the ingame state using the `start` command. After this command is run, signups are closed and new hosts cannot join the hosting team.

### Ingame

Just after running the `start` command, hosts should set individual players' roles. This is done using the `role set <player> <role>` command. A list of already set roles can be viewed with the `role list` command. **These commands should always be run in a host-restricted channel or in DMs with the bot**, as players may learn others roles if they see the command.

Once all players have roles, the `init` command will set up roles and channels with the relevant permissions for the game. It will also send a DM to all players informing them of their roles. If there is an issue, the `cleanup` command will remove all channels and roles so that the hosts can tweak roles. For convenience, the `reload` command will execute `cleanup` and `init` in order.  
Note that roles can still be changed with the `role set <player> <role>` command after `init` is run. This will not, however, change channel permissions.  
Because the `init` command also sends a DM to all players telling them their role, **roles that should not learn their true role should not be set. Set the fake role for that player instead.** You can change this back after `init` so that the player's true role appears in `role list`.

The `killq add <player> [...<player>]`, `killq remove <player> [...<player>]` and `killq exec` commands can be used to manage the kill queue. `killq` alone will list the current kill queue.  
As well as these commands, the `kill <player> [...<player>]` and `revive <player> [...<player>]` commands can be used to instantly kill and revive players.

The `whisper send <player> <message>` command can be used to send an anonymous message to another player. Hosts can limit the maximum whispers per day with the `whisper setmax <max>` command. Since the bot does not include phase management, hosts must manually reset the counter with `whisper clear` every day.  
Similarly to `role list`, the `whisper send` command should not be executed in a public channel where other players may see the message.

The `backup <player> <backup>` command can be used to swap `<player>` with `<backup>` if need be. There are however resitrictions on `<backup>`:
- `<backup>` cannot have spectated at any point during this game
- `<backup>` cannot be a current player or host
- `<backup>` cannot be a previous player who was also swapped out during a backup.

A `list` command is availible to see hosts, alive players and dead players.

Hosts can use the `end` command to end the game and transition back into the pregame state. All channels and roles are removed, and all players and hosts are quit.

### General

Some commands are globally availible for use in and out of the game.

The `info <role>` command will display information about `<role>`.

The `nick <player> <nick>` command can be used by hosts to set a player's nickname. This will appear in `list` commands and can be used to refer to the player in other commands.

The `ping` command checks if the bot is up, and the bots response time.

The `poll create <prompt> <option> [...<option>]` can be used by hosts to create polls. There is  maximum of twenty options, as Discord limits the number of reactions per message. For convenience, the command `poll ask <prompt>` will create a poll with yes/no options and `poll alive <prompt>` will create a poll with an option for each alive player when ingame, and for each joined player when in pregame.  
The `poll end <poll ID>` command can be used to end and get the results of a poll.
Hosts and admins can use the `poll power <user> <power>` command to set the voting power of a player. This is reset to 1 when games start and end.

Admins and moderators can use the `promote` and `demote` commands to switch between ingame versions of their admin and moderator roles.

The `spectate` command can be used by any non-joined player or host to spectate a game. Spectators can see all game channels but cannot send messages, and as such are not legible to be backups. Use `unspectate` to stop spectating.

### Command quick reference

Pregame :
- `host`/`unhost` (mod) : Become a host or step down from being a host.
- `fjoin <player>`/`fquit <player>` (host) : Force join or force quit a player.
- `join`/`quit` : Join or quit the sign-up queue.
- `list` : List hosts and signed-up players.
- `emoji <emoji>` : Set your emoji.
- `start` (host) : Transition into the game state

Ingame :
- `role set <player> <role>` (host) : Set a players role.
- `role list` (host) : List players and their roles.
- `init` (host) : Initialize roles and channels.
- `cleanup`/`reload` (host) : Reset roles and channels. `reload` will also call `init` straight after.
- `killq add <player>`/`killq remove <player>` (host) : Add or remove a player from the kill queue.
- `killq exec` (host) : Execute the kill queue.
- `killq` (host) : List the kill queue.
- `kill <player>`/`revive <player>` (host) : Kill or revive a player.
- `whisper send <player> <message>` : Send an anonymous message to `<player>`.
- `whisper setmax <max>` (host) : Sets the maximum whispers per phase.
- `whisper clear` (host) : Reset the whisper count.
- `backup <player> <backup>` (host) : Swap `<player>` with `<backup>`.
- `list` : List hosts, alive players and dead players.
- `end` (host) : End game and transition to pregame.

Global :
- `info <role>` : Display information about `<role>`.
- `roles` : Display a list of all roles.
- `nick <player> <nick>` (host) : Set `<player>`'s nickname.
- `poll create <prompt> <options>` (host) : Create a poll.
- `poll end <poll ID>` (host) : End a poll.
- `poll power <player> <power>` (host / admin) : Set the voting power of a player.
- `promote`/`demote` (admin, mod) : Switch between ingame and active admin and mod roles.
- `spectate`/`unspectate` : Become a spectator or stop being a spectator.
