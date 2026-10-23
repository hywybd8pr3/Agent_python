from agent_app.tools.registry import TOOLS,excute_function
import json
from openai import APIError
from agent_app.config import load_config
from agent_app.model_client import create_client
from agent_app.agent import create_message,run_turn

def run_manual_tool():

    ''' 接收工具名称,执行工具并显示结果'''

    tool_name = input('请输入工具名称(calculate/weather/search:').strip()

    arguements_text = input("请输入JSON参数,例如{'a':1,'b':2}:").strip()

    try:
        arguements = json.loads(arguements_text)
        if not isinstance(arguements_text,dict):
            raise ValueError('工具参数必须是JSON对象')

    except ValueError as e:
        print("参数解析失败：", error)
        return

    result = excute_function(tool_name, TOOLS, arguements)
    print("工具结果：", result)


def main():
    #1.读取配置
    try:
        config = load_config()
        client = create_client(config)

    except ValueError as e:
        print('自动失败：',e)

    #2.读取模型，初始化对话历史
    model_name = config['LLM_MODEL_NAME']
    messages = create_message()
    print('直接输入问题，与模型对话')
    print('/tool:手动调用工具')
    print('/clear:清除对话历史')
    print('quit,exit或退出:结束程序')

   #3.循环用户输入
    while True:
        user_input = input('请输入问题:').strip()

        if not user_input:
            print('用户输入不能为空，请重新输入')
            continue

        if user_input.lower() in ('quit','exit','退出'):
            print('感谢使用，再见')
            break

        if user_input == '/clear':
            messages = create_message()
            print('已清除对话历史')
            continue

        if user_input == '/tool':
            run_manual_tool()
            continue

    #4.普通问题交给模型，取得回答后再打印
    
    try:
        answer = run_turn(
            client = client,
            messages = messages,
            model = model_name,
            user_input = user_input
        )

        print('模型:',answer)

    except(APIError,ValueError) as e:
        print('对话失败':e)

if __name__ == '__main__':
    main()




    
              








