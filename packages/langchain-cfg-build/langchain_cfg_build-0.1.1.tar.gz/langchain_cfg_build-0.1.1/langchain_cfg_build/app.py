from langchain_cfg_build.infra import config


def initialize():
    config.load_env()
