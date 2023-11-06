from pathlib import Path

import tomllib


ROOT_DIR = Path(__file__).parent

with open(ROOT_DIR / "pyproject.toml", mode="rb") as f:
    pyproject = tomllib.load(f)

    ver = pyproject["project"]["version"]

    print(f"{ver}")
