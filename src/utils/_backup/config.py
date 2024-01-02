#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import subprocess
import sys

from dataclasses import dataclass
from logging import getLogger
from typing import Any
from typing import Union

from utils._backup.host import BackupHost

_log = getLogger()

default_exclude_file = "/home/debauer/utils/config/backup_ignore"


@dataclass
class BackupConfig:
    backup_host: BackupHost
    hostname: str = ""
    sudo: bool = False
    source: str = ""
    exclude_file: str = default_exclude_file
    verbose: bool = False
    dryrun: bool = False

    def _call(self, cmd: Union[str, list], *, verbose: bool = False) -> Any:
        cmd_splitted = cmd.split(" ") if isinstance(cmd, str) else cmd
        output = None if verbose else subprocess.DEVNULL
        try:
            return subprocess.call(cmd_splitted, stdout=output, stderr=output)  # noqa: S603
        except KeyboardInterrupt:
            sys.exit()

    def _check_folder_exist_on_backup_host(self, folder: str, *, verbose: bool = False, create: bool = False) -> bool:
        cmd = ["ssh", f"{self.backup_host.user}@{self.backup_host.host}", f"test -d {folder}"]
        if verbose:
            _log.info(f"[Backup][_check_folder_exist_on_backup_host] check {folder}")
        exist = not self._call(cmd, verbose=True)
        if verbose:
            _log.info(f"[Backup][_check_folder_exist_on_backup_host] exist: {exist}")
        if not exist:
            _log.info(f"[Backup][_check_folder_exist_on_backup_host] create folder {folder}")
            cmd = ["ssh", f"{self.backup_host.user}@{self.backup_host.host}", f"mkdir {folder} -p"]
            self._call(cmd, verbose=True)
            return True
        return exist

    def backup(self) -> None:
        _log.info("not implemented")

    def list(self) -> None:
        _log.info("not implemented")

    def __str__(self) -> str:
        return f"{self.backup_host}, {self.hostname}, {self.source}"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class RsyncBackupConfig(BackupConfig):
    target_folder: str = ""

    def backup(self) -> None:
        if self._check_folder_exist_on_backup_host(f"{self.backup_host.rsync_target}/{self.target_folder}"):
            _log.info("[Rsync][backup] backup started")
            cmd = ("rsync -arPv "
                   f"{self.source} "
                   f"{self.backup_host.user}@{self.backup_host.host}:{self.backup_host.rsync_target}/{self.target_folder} ")
            _log.info(cmd)
            connect = subprocess.Popen(args=cmd, shell=True)
            while connect.poll() is None:
                pass
        else:
            _log.info(f"[Rsync][backup] target folder does not exist: {self.backup_host.rsync_target}")

    def list(self) -> None:
        _log.info("[Rsync][list] not implemented")

    def __str__(self) -> str:
        return f"{self.backup_host}, {self.hostname}, {self.source}, {self.target_folder}"


@dataclass
class ResticBackupConfig(BackupConfig):
    def _base_command(self) -> str:
        return (
            f"{'sudo ' if self.sudo else ''}restic -r sftp:{self.backup_host.user}@{self.backup_host.host}:{self.backup_host.restic_target} "
            f"{'--verbose ' if self.verbose else ''} "
        )

    def _password_file(self) -> str:
        return f"--password-file '{self.backup_host.password_file}' "

    def backup(self) -> None:
        _log.info("[Restic][backup] backup started")
        if self._check_folder_exist_on_backup_host(self.backup_host.restic_target):
            cmd = (
                f"{self._base_command()}"
                f"backup "
                f"{self._password_file()}"
                f"--exclude-file {self.exclude_file} "
                f"{'-n ' if self.dryrun else ''} "
                f"{self.source} "
            )
            connect = subprocess.Popen(args=cmd, shell=True)
            while connect.poll() is None:
                pass
        else:
            _log.info(f"[Restic][backup] target folder does not exist: {self.backup_host.restic_target}")

    def list(self) -> None:
        _log.info("[Restic][list] list snapshots")
        if self._check_folder_exist_on_backup_host(self.backup_host.restic_target):
            cmd = (
                f"{self._base_command()}"
                f"snapshots "
                f"{self._password_file()}"
                f"--path={self.source}"
            )
            self._call(cmd)
