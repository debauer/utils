#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import subprocess
import sys

from argparse import ArgumentParser
from argparse import Namespace

from utils._backup.config import BackupConfig, ResticBackupConfig
from utils._backup.host import BackupHost


karl = BackupHost(
    host="karl.lan",
    target="/mnt/data/backups/synyx_t14/restic",
)

herbert = BackupHost(
    host="herbert.lan",
    target="/mnt/data/backups/synyx_t14/restic",
    wol=True,
    mac="D0:50:99:29:2E:91",
)

target = [
    ResticBackupConfig(hostname="bauer-t14s", backup_host=herbert, source="/etc", sudo=True),
    ResticBackupConfig(hostname="bauer-t14s", backup_host=herbert, source="/home/debauer")
]


def parse() -> Namespace:
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
        sys.exit()


def _list(conf: BackupConfig) -> None:
    print(conf.list_command())
    try:
        connect = subprocess.Popen(args=conf.list_command(), shell=True)
        while connect.poll() is None:
            pass
    except KeyboardInterrupt:
        sys.exit()


def main() -> None:
    args = parse()
    verbose = args.verbose
    dryrun = args.dryrun
    list = args.list

    herbert.wake_up()

    herbert.poweroff()


    if verbose:
        for a in target:
            a.verbose = True

    if dryrun:
        for a in target:
            a.dryrun = True

#    if list:
#        for t in target:
#            _list(t)
#        exit()
#
#    for t in target:
#        _backup(t)


if __name__ == "__main__":
    main()
