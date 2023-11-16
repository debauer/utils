#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from datetime import datetime

from helper.process import command_print


sources = ["Flatbed", "ADF"]
resolution = [75, 100, 150, 200, 300]

imagename = datetime.now().isoformat()
devices = {"home": "airscan:w1:Samsung Electronics Co., Ltd. M2070 Series", "hoelle": "airscan:w0:Brother MFC-J6720DW"}


def parse_args() -> Namespace:
    parser = ArgumentParser(description="scan image")

    parser.add_argument("--source", type=str, help="Flatbed or ADF", choices=sources, default="Flatbed")
    parser.add_argument("--dpi", type=int, help="DPI", choices=resolution, default=300)
    parser.add_argument("--brightness", type=int, help="brightness -100..100 in steps of 1", default=0)
    parser.add_argument("--contrast", type=int, help="contrast -100..100 in steps of 1", default=0)
    parser.add_argument("--name", type=str, help="name of file", default=imagename)
    parser.add_argument("--batch", help="reset", action="store_const", const="reset")
    parser.add_argument("--scanner", type=str, help="scanner", default="home", choices=devices.keys())

    return parser.parse_args()


def build_dokument():
    tempname = imagename
    if args.batch:
        tempname = "batch*"
    cmd = f"convert {tempname}.jpg {imagename}.pdf"
    command_print(cmd, timeout=None)


def scan(
    name: str,
    device: str = "home",
    source: str = "Flatbed",
    brightness: int = 0,
    contrast: int = 0,
    dpi: int = 300,
    batch: bool = False,
) -> None:
    device = devices[device]
    cmd = f'scanimage -d "{device}" -p -v '
    cmd += f" --source {source}"
    cmd += f" --brightness {brightness}"
    cmd += f" --contrast {contrast}"
    cmd += f" --resolution {dpi}"
    if batch:
        batch += " --batch=batch%d.jpg"
        if source == "Flatbed":
            batch += " --batch-prompt "
    else:
        cmd += f" -o {name}.jpeg"
    command_print(cmd, timeout=None)
    if batch:
        build_dokument()


if __name__ == "__main__":
    args = parse_args()
    scan(
        name=args.name,
        device=args.scanner,
        source=args.source,
        brightness=args.brightness,
        contrast=args.contrast,
        dpi=args.dpi,
        batch=args.batch,
    )
