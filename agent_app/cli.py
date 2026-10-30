import json

from openai import APIError

from agent_app.config import load_config
from agent_app.model_client import create_client
from agent_app.agent import create_messages, run_turn
from agent_app.tools.registry import TOOLS, execute_function


def run_manual_tool():
    """手动调试工具: 输入名称和参数, 执行后显示结果."""

    tool_name = input(
    f"请输入工具名称（{' / '.join(TOOLS)}):").strip()

    arguments_text = input(
        '请输入 JSON 参数, 例如 {"a": 1, "b": 2}: '
    ).strip()

    try:
        arguments = json.loads(arguments_text)

        if not isinstance(arguments, dict):
            raise ValueError("工具参数必须是 JSON 对象.")

    except ValueError as error:
        print("参数错误:", error)
        return

    result = execute_function(
        tool_name=tool_name,
        tools=TOOLS,
        arguments=arguments,
    )

    print("工具结果:", result)


def main():
    # 1. 读取配置, 创建客户端
    try:
        config = load_config()
        client = create_client(config)

    except ValueError as error:
        print("配置失败:", error)
        print(
            "请先配置环境变量 "
            "LLM_API_KEY, LLM_API_URL, LLM_MODEL_NAME, "
            "然后重新运行."
        )
        return

    # 2. 读取模型名称, 初始化对话历史
    model_name = config["LLM_MODEL_NAME"]
    messages = create_messages()

    print("直接输入问题, 与模型对话")
    print("/tool: 手动工具调试")
    print("/clear: 清除对话历史")
    print("quit, exit 或退出: 结束程序")

    # 3. 循环读取用户输入
    while True:
        user_input = input("请输入问题: ").strip()

        if not user_input:
            print("用户输入不能为空, 请重新输入.")
            continue

        if user_input.lower() in ("quit", "exit", "退出"):
            print("感谢使用, 再见!")
            break

        if user_input == "/clear":
            messages = create_messages()
            print("已清除对话历史.")
            continue

        if user_input == "/tool":
            run_manual_tool()
            continue

        # 4. 将自然语言输入交给 Agent
        try:
            answer = run_turn(
                client=client,
                messages=messages,
                model_name=model_name,
                user_input=user_input,
            )

            print(answer)

        except (APIError, ValueError) as error:
            print("对话失败:", error)


if __name__ == "__main__":
    main()