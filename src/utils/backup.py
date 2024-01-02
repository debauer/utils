#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import socket
import sys

from argparse import ArgumentParser
from argparse import Namespace

from utils._backup.config import ResticBackupConfig
from utils._backup.config import RsyncBackupConfig
from utils._backup.host import BackupHost


karl = BackupHost(
    host="karl.lan",
    base_backup_folder="/mnt/data/backups",
)

herbert = BackupHost(
    host="herbert.lan",
    base_backup_folder="/mnt/backup",
    wol=True,
    mac="D0:50:99:29:2E:91",
)

backup_configs = [
    ResticBackupConfig(hostname="bauer-t14s", backup_host=karl, source="/etc", sudo=True),
    ResticBackupConfig(hostname="bauer-t14s", backup_host=karl, source="/home/debauer"),
    RsyncBackupConfig(hostname="karl", backup_host=herbert, source="/mnt/data/files/", target_folder="files"),
    RsyncBackupConfig(hostname="karl", backup_host=herbert, source="/mnt/data/medien/ebooks/", target_folder="medien/ebooks"),
    RsyncBackupConfig(hostname="karl", backup_host=herbert, source="/mnt/data/medien/musik/", target_folder="medien/musik"),
    RsyncBackupConfig(hostname="karl", backup_host=herbert, source="/mnt/data/medien/software/", target_folder="medien/software"),
    RsyncBackupConfig(hostname="karl", backup_host=herbert, source="/mnt/data/medien/audiobooks/", target_folder="medien/audiobooks"),
]


def parse() -> Namespace:
    parser = ArgumentParser(description="Backup System")
    parser.add_argument("-n", "--dryrun", action="store_const", const="dryrun", help="dry-run")
    parser.add_argument("-v", "--verbose", action="store_const", const="verbose", help="verbose")
    parser.add_argument("-l", "--list", action="store_const", const="list", help="list all snapshots")
    return parser.parse_args()


def main() -> None:
    args = parse()
    verbose = args.verbose
    dryrun = args.dryrun
    list_backups = args.list
    hostname = socket.gethostname()
    filtered_configs = [x for x in backup_configs if x.hostname == hostname]
    if verbose:
        print("USED CONFIGS:")
        for f in filtered_configs:
            print(f)
    if verbose:
        for a in filtered_configs:
            a.verbose = True

    if dryrun:
        for a in filtered_configs:
            a.dryrun = True

    if list_backups:
        for t in filtered_configs:
            t.list()
        sys.exit()
    for t in filtered_configs:
        t.backup_host.wake_up()

    for t in filtered_configs:
        t.backup()

    for t in filtered_configs:
        t.backup_host.poweroff()


if __name__ == "__main__":
    main()
