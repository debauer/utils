#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import subprocess
import sys

from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any
from typing import Union


@dataclass
class Host:
    name: str
    mac: str
    ping_address: str


hosts = [
    Host("herbert", "D0:50:99:29:2E:91", "herbert.lan"),
]


def call(cmd: Union[str, list], *, verbose: bool = False) -> Any:
    cmd_splitted = cmd.split(" ") if isinstance(cmd, str) else cmd
    output = None if verbose else subprocess.DEVNULL
    try:
        return subprocess.call(cmd_splitted, stdout=output, stderr=output)  # noqa: S603
    except KeyboardInterrupt:
        sys.exit()


def main() -> None:
    choices = [h.name for h in hosts]
    parser = ArgumentParser(description="System to record the data on a trimodal crane")
    parser.add_argument("wallpaper", type=str, help="wallpaper", choices=choices)
    hostname = parser.parse_args().wallpaper
    for h in hosts:
        if h.name == hostname:
            print(f"send magic packet to {h.name}")
            wol_cmd = f"wol {h.mac} -p 9"
            ping_cmd = f"ping -c 1 {h.ping_address}"
            call(wol_cmd)
            retry = 0
            print("send ping")
            while call(ping_cmd) and retry < 20:
                retry += 1
                print(f"retry ping {retry}")
            if retry == 20:
                print(f"{h.name} don't answer")
            else:
                print(f"{h.name} is up")


if __name__ == "__main__":
    main()
