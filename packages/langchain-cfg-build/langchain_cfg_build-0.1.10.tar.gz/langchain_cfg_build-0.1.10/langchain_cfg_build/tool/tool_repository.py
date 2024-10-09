from typing import Dict, List, Callable

from langchain_core.tools import BaseTool

from langchain_cfg_build.obj.cache_provider import CacheProvider

_ALL_TOOL_MAP: Dict[str, BaseTool] = dict()


class ToolRepository:
    def __init__(self):
        self._provider_list: List[CacheProvider[BaseTool]] = list()

    def add_tool(self, tool_name: str, provide: Callable[[], BaseTool]):
        self._provider_list.append(CacheProvider[BaseTool](tool_name, _ALL_TOOL_MAP, provide))


instance: ToolRepository = None


def get_tool_repo():
    global instance
    if not instance:
        instance = ToolRepository()
    return instance


if __name__ == '__main__':
    print('Testing')
