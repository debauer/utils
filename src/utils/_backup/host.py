from __future__ import annotations

import subprocess
import sys

from dataclasses import dataclass
from typing import Any


default_password_file = "/home/debauer/.resticcredentials"


@dataclass
class BackupHost:
    wol: bool = False
    target: str = ""
    user: str = "debauer"
    password_file: str = default_password_file
    host: str = ""
    mac: str = ""
    ping_retry: int = 20

    def sftp(self) -> str:
        return f"sftp:{self.user}@{self.host}:"

    def _call(self, cmd: str | list) -> Any:
        if isinstance(cmd, str):
            cmd_splitted = cmd.split(" ")
        else: 
            cmd_splitted = cmd
        try:
            return subprocess.call(cmd_splitted, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # noqa: S603
        except KeyboardInterrupt:
            sys.exit()

    def wake_up(self) -> None:
        if self.wol:
            wol_cmd = f"wol {self.mac} -p 9"
            ping_cmd = f"ping -c 1 {self.host}"
            print(f"[BackupHost][wake_up][{self.host}] wol: send magic packet")
            self._call(wol_cmd)
            print(f"[BackupHost][wake_up][{self.host}] start pinging")
            retry = 0
            while self._call(ping_cmd) and retry < self.ping_retry:
                retry += 1
                print(f"[BackupHost][wake_up][{self.host}] retry ping {retry}")
            print(f"[BackupHost][wake_up][{self.host}] got ping")

    def poweroff(self) -> None:
        if self.wol:
            poweroff_cmd = ["ssh", f"{self.user}@{self.host}", "sudo poweroff"]
            print(f"[BackupHost][poweroff][{self.host}] shutdown host")
            self._call(poweroff_cmd)