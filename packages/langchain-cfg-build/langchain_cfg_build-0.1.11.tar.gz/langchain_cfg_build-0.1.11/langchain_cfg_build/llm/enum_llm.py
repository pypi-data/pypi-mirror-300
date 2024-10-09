from enum import Enum
from typing import Dict

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel

from langchain_cfg_build.obj.cache_provider import CacheProvider

_ALL_LLM_MAP: Dict[str, BaseLanguageModel] = dict()


class EnumLLM(Enum):
    gpt_4o = CacheProvider[BaseLanguageModel]("gpt_4o", _ALL_LLM_MAP, lambda: ChatOpenAI(model_name="gpt-4"))
    gpt_4o_mini = CacheProvider[BaseLanguageModel]("gpt_4o_mini", _ALL_LLM_MAP,
                                                   lambda: ChatOpenAI(model_name="gpt-4o-mini"))
    # gpt_4o: BaseLanguageModel = ChatOpenAI(model_name="gpt-4")


def get_enum_by_name(name: str) -> EnumLLM:
    return EnumLLM[name]


if __name__ == '__main__':
    name = "gpt_4o"
    enum_member = get_enum_by_name(name)
    print(enum_member)
    print(enum_member.value)
