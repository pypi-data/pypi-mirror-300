import argparse
import os

from dotenv import load_dotenv

from langchain_cfg_build import get_root_path

_inited = False


def load_env():
    global _inited
    if _inited:
        return
    _inited = True
    load_dotenv()
    load_dotenv(verbose=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", help="environment")
    args = parser.parse_args()
    if not args.env:
        return
    env_path = get_root_path() / f'{args.env}.env'
    load_dotenv(dotenv_path=env_path, override=True)


def env(s) -> str:
    load_env()
    return os.getenv(s)


def env_int(s) -> int:
    load_env()
    return int(os.getenv(s))


def env_float(s) -> float:
    load_env()
    return float(os.getenv(s))


def env_bool(s) -> bool:
    load_env()
    return env(s) == 'true'


if __name__ == '__main__':
    load_env()
    print(env('db_port'))
