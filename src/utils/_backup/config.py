from __future__ import annotations

from dataclasses import dataclass

from utils._backup.host import BackupHost


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

    def backup_command(self) -> str:
        return ""

    def list_command(self) -> str:
        return ""


@dataclass
class RsyncBackupConfig(BackupConfig):
    def backup_command(self) -> str:
        return ""

    def list_command(self) -> str:
        return ""


@dataclass
class ResticBackupConfig(BackupConfig):
    def _base_command(self) -> str:
        return (f"{'sudo ' if self.sudo else ''}restic -r {self.backup_host.sftp}{self.backup_host.target} "
                f"{'--verbose ' if self.verbose else ''} "
                )

    def _password_file(self) -> str:
        return f"--password-file '{self.backup_host.password_file}' "

    def backup_command(self) -> str:
        return (
            f"{self._base_command()}"
            f"backup "
            f"{self._password_file()}"
            f"--exclude-file {self.exclude_file} "
            f"{'-n ' if self.dryrun else ''} "
            f"{self.source} "
        )

    def list_command(self) -> str:
        return (
            f"{self._base_command()}"
            f"snapshots "
            f"{self._password_file()}"
            f"--path={self.source}"
        )
