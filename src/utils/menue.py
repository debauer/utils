#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

from cursesmenu import CursesMenu
from cursesmenu.items import CommandItem

from utils.remote import main as remote
from utils.sound import main as sound
from utils.wallpaper import main as wallpaper


@dataclass
class Tool:
    fn: Callable
    name: str = ""


tools = [Tool(wallpaper, "wallpaper"), Tool(sound, "sound"), Tool(remote, "remote")]


def main():
    print("available wallpapers:\n")
    for i, wp in enumerate(tools):
        print(f"{i:<2} {wp.name:<15}")

    print()
    tool_id = int(input("choose tool: "))
    os.system('clear')
    tools[tool_id].fn()
    exit()

    menu.start()
    _ = menu.join()


if __name__ == "__main__":
    main()
