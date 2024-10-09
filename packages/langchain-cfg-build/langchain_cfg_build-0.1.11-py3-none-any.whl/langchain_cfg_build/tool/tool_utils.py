from typing import Callable

from langchain_core.tools import StructuredTool, BaseTool


def gen_tool(name: str, desc: str, func: Callable[[any], any]) -> BaseTool:
    ans = StructuredTool.from_function(
        func=func,
        name=name,
        description=desc,
        # coroutine= ... <- you can specify an async method if desired as well
    )
    return ans
