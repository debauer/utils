#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import socket
import subprocess
import sys

from dataclasses import dataclass
from typing import Any, Union

default_password_file = "/home/debauer/.resticcredentials"


@dataclass
class BackupHost:
    wol: bool = False
    base_backup_folder : str = ""
    user: str = "debauer"
    password_file: str = default_password_file
    host: str = ""
    mac: str = ""
    ping_retry: int = 20
    
    _waked_up: bool = False
    _power_off: bool = False

    @property
    def restic_target(self) -> str:
        hostname = socket.gethostname()
        return f"{self.base_backup_folder}/{hostname}/restic"

    @property
    def rsync_target(self) -> str:
        hostname = socket.gethostname()
        return f"{self.base_backup_folder}/{hostname}/rsync"

    def _call(self, cmd: Union[str, list], *, verbose: bool = False) -> Any:
        cmd_splitted = cmd.split(" ") if isinstance(cmd, str) else cmd
        output = None if verbose else subprocess.DEVNULL
        try:
            return subprocess.call(cmd_splitted, stdout=output, stderr=output)  # noqa: S603
        except KeyboardInterrupt:
            sys.exit()

    def wake_up(self) -> None:
        if self.wol and not self._waked_up:
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
            self._waked_up = True

    def poweroff(self) -> None:
        if self.wol and not self._power_off:
            poweroff_cmd = ["ssh", f"{self.user}@{self.host}", "sudo poweroff"]
            print(f"[BackupHost][poweroff][{self.host}] shutdown host")
            self._call(poweroff_cmd)
            self._power_off = True