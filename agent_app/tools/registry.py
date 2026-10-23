from typing import Callable
from agent_app.tools.calculator import calculate
from agent_app.tools.demo_tools import weather,search

TOOLS: dict[str,Callable[...,str]] = {
    'calculate':calculate,
    'weather':weather,
    'search':search}

def excute_function(tool_name:str,tools:dict[str,Callable[...,str]],arguements:dict[str,object]) -> str:
    if tool_name not in tools:
        return f'tool not found:{tool_name}'
    tool = tools[tool_name]

    try:
        return tool(**arguements)
    
    except(TypeError,ValueError) as e:
        return f'工具{tool_name}执行失败:{e}'
        

     
 
 