from enum import Enum
from typing import Dict

from langchain import hub
from langchain_core.prompts import BasePromptTemplate

from langchain_cfg_build.obj.cache_provider import CacheProvider

_ALL_PROMPT_MAP: Dict[str, BasePromptTemplate] = dict()


class EnumPrompt(Enum):
    HWCHASE17_REACT = CacheProvider[BasePromptTemplate]("HWCHASE17_REACT", _ALL_PROMPT_MAP,
                                                        lambda: hub.pull("hwchase17/react"))
