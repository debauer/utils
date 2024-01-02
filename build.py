import tomllib
from pathlib import Path


def build() -> None:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        bin = Path(".venv/bin")
        bin2 = Path(".venv/bin2")
        bin2.mkdir(exist_ok=True)
        for script in data["tool"]["poetry"]["scripts"]:
            print(f"create symlink for {script}")
            if not (bin2 / script).is_file():
                print(f"source file {script} is missing. run poetry install")
            link_path = (bin2 / script)
            link_path.unlink(missing_ok=True)
            Path(link_path).symlink_to(bin.absolute() / script)


if __name__ == "__main__":
    build()
