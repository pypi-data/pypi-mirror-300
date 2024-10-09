from langchain_cfg_build.infra import config


def initialize(env_dir_path: str):
    config.load_env(env_dir_path=env_dir_path)
