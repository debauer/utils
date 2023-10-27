#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import sys

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from utils.helper.process import command_silent

import yt_dlp

output_path = "/media/hermine_medien/_download_yt/%(title)s.%(ext)s"


def main():
    args = ["-o", output_path, "-x", "--audio-format", "mp3", "--audio-quality", "0"]
    for e in sys.argv[1:]:
        args.append(e)
    yt_dlp.main(args)


if __name__ == '__main__':
    main()
