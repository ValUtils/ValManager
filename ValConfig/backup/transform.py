import json

from typing import Any, Dict

json_keys = ["SavedCrosshairProfileData", "MutedWords"]


def get_enum_index(enum: str, settings: list):
    return next((settings.index(x) for x in settings if enum in x["settingEnum"]), -1)


def load_key(enum: str, strSettings: list):
    index = get_enum_index(enum, strSettings)
    if index == -1:
        return
    setting = strSettings[index]
    setting["value"] = json.loads(setting["value"])


def dump_key(enum: str, strSettings: list):
    index = get_enum_index(enum, strSettings)
    if index == -1:
        return
    setting = strSettings[index]
    setting["value"] = json.dumps(setting["value"])


def to_raw_config(config: Dict[str, Any]):
    if "stringSettings" not in config:
        return config
    strSettings = config["stringSettings"]
    for key in json_keys:
        dump_key(key, strSettings)
    return config


def from_raw_config(config: Dict[str, Any]):
    if "stringSettings" not in config:
        return config
    strSettings = config["stringSettings"]
    for key in json_keys:
        load_key(key, strSettings)
    return config
