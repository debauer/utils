#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import random
import sys

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from utils.helper.process import command_silent


@dataclass
class Wallpaper:
    path: Path
    name: str = ""


def set_wallpaper(wallpapers: list[Wallpaper], name: str) -> None:
    for w in wallpapers:
        if w.name == name:
            command = f"swaymsg output '*' background {w.path} fill"
            command_silent(command)
            print("done")


def main() -> None:
    wallpaper_folder = Path("/home/debauer/Bilder/Wallpaper/")
    wallpaper_glob = wallpaper_folder.glob("**/*")

    wallpaper = [Wallpaper(wg, name=wg.name.split(".")[0]) for wg in wallpaper_glob]
    choices = [wg.name for wg in wallpaper]
    print(sys.argv)
    if len(sys.argv) == 1:  # bit hacky because of positional argument in argparse
        print("available wallpapers:\n")
        for i, wp in enumerate(wallpaper):
            print(f"{i:<2} {wp.path.name:<15}")

        print()
        wallpaper_id = int(input("choose wallpaper: "))
        wallpaper_name = wallpaper[wallpaper_id].name
    elif len(sys.argv) == 2 and sys.argv[1] == "random":
        wallpaper_name = random.choice(choices)
    else:
        parser = ArgumentParser(description="System to record the data on a trimodal crane")
        parser.add_argument("wallpaper", type=str, help="wallpaper", choices=choices)
        wallpaper_name = parser.parse_args().wallpaper
    set_wallpaper(wallpaper, wallpaper_name)


if __name__ == "__main__":
    main()
