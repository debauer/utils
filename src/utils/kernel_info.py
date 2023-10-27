#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import os
import sys

from pathlib import Path

def main():
    file = list(Path("/boot").glob("vmlinuz-*"))
    os_info = os.uname()
    print(f"{os_info.sysname=}")
    print(f"{os_info.nodename=}")
    print(f"{os_info.release=}")
    print(f"{os_info.version=}")
    print(f"{os_info.machine=}")
    print(f"is current version: {os_info.release not in file[0].as_posix()}")
    sys.exit(os_info.release in file[0].as_posix())


if __name__ == "__main__":
    main()
