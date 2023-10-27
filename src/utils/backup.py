#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import subprocess

from argparse import ArgumentParser
from dataclasses import dataclass

default_password_file = "/home/debauer/.resticcredentials"
default_exclude_file = "/home/debauer/scripts/config/backup_ignore"


@dataclass
class BackupHost:
    target: str = ""
    password_file: str = default_password_file
    host: str = ""


@dataclass
class BackupConfig:
    host: BackupHost
    sudo: bool = False
    source: str = ""
    exclude_file: str = default_exclude_file
    verbose: bool = False
    dryrun: bool = False

    def _base_command(self) -> str:
        return (f"{'sudo ' if self.sudo else ''}restic -r {self.host.host}{self.host.target} "
                f"{'--verbose ' if self.verbose else ''} "
                )

    def _password_file(self) -> str:
        return f"--password-file '{self.host.password_file}' "

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


# restic -r /srv/restic-repo check

herbert = BackupHost(host="sftp:debauer@herbert:", target="/mnt/data/backups/synyx_t14/restic")

target = [BackupConfig(host=herbert, source="/etc", sudo=True), BackupConfig(host=herbert, source="/home/debauer")]


def parse():
    parser = ArgumentParser(description="Backup System")
    parser.add_argument("-n", "--dryrun", action="store_const", const="dryrun", help="dry-run")
    parser.add_argument("-v", "--verbose", action="store_const", const="verbose", help="verbose")
    parser.add_argument("-l", "--list", action="store_const", const="list", help="list all snapshots")
    return parser.parse_args()


def _backup(conf: BackupConfig) -> None:
    try:
        connect = subprocess.Popen(args=conf.backup_command(), shell=True)
        while connect.poll() is None:
            pass
    except KeyboardInterrupt:
        exit()


def _list(conf: BackupConfig) -> None:
    print(conf.list_command())
    try:
        connect = subprocess.Popen(args=conf.list_command(), shell=True)
        while connect.poll() is None:
            pass
    except KeyboardInterrupt:
        exit()


def main():
    args = parse()
    verbose = args.verbose
    dryrun = args.dryrun
    list = args.list



    if verbose:
        for a in target:
            a.verbose = True

    if dryrun:
        for a in target:
            a.dryrun = True

    if list:
        for t in target:
            _list(t)
        exit()

    for t in target:
        _backup(t)


if __name__ == "__main__":
    main()
