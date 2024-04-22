import os
from pathlib import Path
from dotenv import load_dotenv

ENV = ".env"

BASE_DIR = Path(__file__).absolute()
load_dotenv(os.path.join(BASE_DIR.parent.parent, ENV))


def get_env(env_var: str = "") -> str | None:
    try:
        return os.environ.get(env_var) or open(os.environ.get(f"{env_var}_FILE")).read()
    except TypeError:
        return None
