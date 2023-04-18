from pathlib import Path
from ValStorage import save_to_drive

from ..structs import BackupFile
from ..storage import json_read, json_write, create_path, settingsPath


def backup_write(data, file, sub):
    create_path(settingsPath / "backup" / sub)
    json_write(data, settingsPath / "backup" / sub / file)


def backup_read(file, sub):
    return json_read(settingsPath / "backup" / sub / file)


def save_backup(file: BackupFile, path: Path):
    save_to_drive(file.to_json(), path)
