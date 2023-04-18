from pathlib import Path
from time import time
from datetime import datetime
from dictdiffer import diff, patch
from pympler.asizeof import asizeof
from ValStorage import get_settings

from ..structs import BackupData, BackupFile, BackupInfo
from ..storage import json_write, create_path, settingsPath
from .transform import from_raw_config, to_raw_config
from .storage import save_backup


def build_backup(settings, patches):
    try:
        iter_patches = iter(patches)
        result = patch(next(iter_patches), settings)
    except StopIteration:
        return settings

    for diff_result in iter_patches:
        patch(diff_result, result, True)
    return result


def new_backup(path: Path, file: BackupFile, info: BackupInfo, config):
    info.backups.append(BackupData(info.backupNumber, -1))
    file.creationDate = time()
    file.settings = config
    save_backup(file, path)


def create_backup(info: BackupInfo, config, user_path: Path):
    backup_path = user_path / f"{info.backupNumber}.json"
    file = get_settings(BackupFile, backup_path)
    if file.creationDate == 0:
        new_backup(backup_path, file, info, config)
        return
    settings = build_backup(file.settings, file.patches)
    settings_diff = list(diff(settings, config))
    if len(settings_diff) == 0:
        return
    file.patches.append(settings_diff)
    kilobyte = 1000
    size_patches = asizeof(file.patches)
    if size_patches > 5 * kilobyte:
        info.backupNumber += 1
        new_path = backup_path.with_stem(str(info.backupNumber))
        new_backup(new_path, BackupFile(), info, config)
        return
    newPatchIndex = len(file.patches) - 1
    info.backups.append(BackupData(info.backupNumber, newPatchIndex))
    save_backup(file, backup_path)


def backup_settings(user, config):
    preferences = from_raw_config(config)
    user_path = settingsPath / "backup" / user
    create_path(user_path)
    info = get_settings(BackupInfo, user_path / "info.json")
    info.lastBackup = time()
    create_backup(info, preferences, user_path)
    json_write(info.to_dict(), user_path / "info.json")


def to_date(timestamp: float):
    return datetime.fromtimestamp(timestamp).strftime("%H:%M %d/%m/%y")


def backup_list(user):
    user_path = settingsPath / "backup" / user
    create_path(user_path)
    info = get_settings(BackupInfo, user_path / "info.json")
    return [to_date(x.timestamp) for x in info.backups]


def get_backup(user, index):
    user_path = settingsPath / "backup" / user
    create_path(user_path)
    info = get_settings(BackupInfo, user_path / "info.json")
    backup = info.backups[index]
    path = user_path / f"{backup.file}.json"
    file = get_settings(BackupFile, path)
    if backup.patchIndex == -1:
        return to_raw_config(file.settings)
    patches = file.patches[:backup.patchIndex + 1]
    settings = build_backup(file.settings, patches)
    return to_raw_config(settings)
