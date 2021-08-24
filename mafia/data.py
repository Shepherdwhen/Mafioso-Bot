import json
from os import path
from typing import NewType, Union

Role = NewType('Role', dict[
    str,          # key: role attribute
    Union[
        str,      # data: role attribute
        list[str] # data: role attribute (description)
    ]
])

ChannelDescriptor = NewType('ChannelDescriptor', dict[
    str,          # key: channel attribute
    Union[
        str,      # data: channel attribute
        list[str] # data: channel attribute (members)
    ]
])

with open(path.join('mafia', 'roles.json')) as file:
    _data = json.load(file)


    roles: dict[
        str,              # key: role id
        Role
    ] = _data['roles']

    for role in roles:
        roles[role]['id'] = role

    channels: dict[
        str,              # key: channel id
        ChannelDescriptor
    ] = _data['channels']
