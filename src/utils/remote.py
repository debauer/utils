#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import subprocess
import sys

from argparse import ArgumentParser
from argparse import Namespace
from dataclasses import dataclass


@dataclass
class Connection:
    name: str
    user: str
    password: str
    host: str
    port: int
    client: str = "xfreerdp"


connections = [
    Connection("guse", "debauer", "123456", "192.168.1.83", 5900, "wlvncc"),
    Connection("windows", "debauer", "123456", "192.168.1.84", 3389),
    Connection("windows-extern", "debauer", "123456", "localhost", 13389),
]


def parse_args() -> Namespace:
    choices = [conn.name for conn in connections]

    parser = ArgumentParser(description="System to record the data on a trimodal crane")

    parser.add_argument("connection", type=str, help="connection", choices=choices)
    return parser.parse_args()


def main():
    if len(sys.argv) == 1:  # bit hacky because of positional argument in argparse
        print("available connections:\n")
        for i, wp in enumerate(connections):
            print(f"{i:<2} {wp.name:<15}")

        print()
        connection_id = int(input("choose connections: "))
        connection_name = connections[connection_id].name
    else:
        args = parse_args()
        connection_name = args.connection
    try:
        for conn in connections:
            if conn.name == connection_name:
                if conn.client == "xfreerdp":
                    command = f"xfreerdp /u:'{conn.user}' /p:'{conn.password}' /v:{conn.host}:{conn.port} /f +fonts /floatbar /smart-sizing"
                if conn.client == "wlvncc":
                    command = f"wlvncc {conn.host}"
                print(command)
                connect = subprocess.Popen(args=command, shell=True)
                while connect.poll() is None:
                    pass
                exit()
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
