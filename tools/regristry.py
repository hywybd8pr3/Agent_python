from typing import Callable

def calculate() -> str:
    return 'excuted calculate'

def weather() -> str:
    return 'excuted weather'

def search() -> str:
    return 'excuted search'

def select_tool(user_input: str) -> str:
    if '计算' in user_input:
        return 'calculate'
    elif '天气' in user_input:
        return 'weather'
    elif '搜索' in user_input:
        return 'search'
    else:
        return 'none'
def execute_function(tools_name:str,
                     tools:dict[str,Callable]) -> str:
    if tools_name not in tools:
        return 'Tool not found: email'
    else:
        tool = tools[tools_name]
        return tool()

tools =  {'calculate': calculate, 'weather': weather, 'search': search}
user_input = str(input('请输入你想要的功能：'))
tools_name = select_tool(user_input)
print(execute_function(tools_name, tools))

