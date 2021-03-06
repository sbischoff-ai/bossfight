# -*- coding: utf-8 -*-
"""
Module that manages access to the clients configuration. With *config.get* provides
as a singleton object that allows access to the config keys as attributes.
Use *load()* and *save()* to persist and restore config on/from disk.
"""

import sys
import os
import json
import appdirs

# Default client configuration is a small window.
# The command line to start the server only works with the venv
# and this should be changed to a "proper" .exe later on.
_DEFAULT_CONFIG = {
    "screen_mode": {"width": 854, "height": 480, "fullscreen": False},
    "local_server_exec": [sys.executable, "-m", "rottn.server"],
}

# Keep different config files for regular python and experimental PyPy version.
if "pypy3.exe" in sys.executable:
    CONFIG_PATH = os.path.join(
        appdirs.AppDirs(appname="rottn", appauthor="pxlbrain").user_config_dir,
        "client_config_pypy.json",
    )
else:
    CONFIG_PATH = os.path.join(
        appdirs.AppDirs(appname="rottn", appauthor="pxlbrain").user_config_dir,
        "client_config.json",
    )
_CURRENT_CONFIG = {}

get = type("Config", (object,), _CURRENT_CONFIG)()
get.__dict__ = _CURRENT_CONFIG


def get_default():
    """
    Returns a deep copy of the default configuration dictionary.
    """
    return json.loads(json.dumps(_DEFAULT_CONFIG))


def revert_to_default():
    """
    Reverts config data to the default configuration.
    """
    _CURRENT_CONFIG.update(get_default())


def save():
    """
    Saves the client configuration data in a json file in the application data directory.

    Windows 7+: `C:\\Users\\{username}\\AppData\\Local\\pxlbrain\\rottn\\client_config.json`
    """
    if not os.path.exists(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))
    with open(CONFIG_PATH, mode="w") as file:
        json.dump(_CURRENT_CONFIG, file, indent=4)


def load():
    """
    Loads the client configuration data from a json file in the application data directory.

    Windows 7+: `C:\\Users\\{username}\\AppData\\Local\\pxlbrain\\rottn\\client_config.json`
    """
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, mode="r") as file:
            _CURRENT_CONFIG.update(json.load(file))


if os.path.exists(CONFIG_PATH):
    load()
    # If config keys have been added or changed:
    for key in _DEFAULT_CONFIG:
        if key not in _CURRENT_CONFIG:
            _CURRENT_CONFIG[key] = get_default()[key]
else:
    revert_to_default()
    save()
