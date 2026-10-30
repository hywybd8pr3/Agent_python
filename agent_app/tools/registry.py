from typing import Callable

from agent_app.tools.calculator import calculate
from agent_app.tools.demo_tools import weather, search
from agent_app.tools.notes import (
    add_note,
    list_notes,
    read_note,
    search_notes,
)

TOOLS: dict[str, Callable[..., str]] = {
    "calculate": calculate,
    "weather": weather,
    "search": search,
    "add_note": add_note,
    "list_notes": list_notes,
    "read_note": read_note,
    "search_notes": search_notes,
}


def execute_function(
    tool_name: str,
    tools: dict[str, Callable[..., str]],
    arguments: dict[str, object],
) -> str:
    """根据名称执行已注册的工具，返回结果或错误说明。"""

    if tool_name not in tools:
        return f"Tool not found: {tool_name}"

    tool = tools[tool_name]

    try:
        return tool(**arguments)

    except (TypeError, ValueError, OSError) as error:
        return f"工具 {tool_name} 执行失败：{error}"