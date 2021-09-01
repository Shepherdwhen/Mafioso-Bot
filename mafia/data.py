import json
from os import path
from typing import NewType, Union

Role = NewType('Role', 'dict[str, Union[str, list[str]]]')

ChannelDescriptor = NewType('ChannelDescriptor', 'dict[str, Union[str, list[str]]]')

with open(path.join('mafia', 'roles.json')) as file:
    _data = json.load(file)


    roles: 'dict[str, Role]' = _data['roles']

    for role in roles:
        roles[role]['id'] = role

    channels: 'dict[str, ChannelDescriptor]' = _data['channels']
