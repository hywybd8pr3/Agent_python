from openai import OpenAI


def create_client(config):
    return OpenAI(
        api_key=config["LLM_API_KEY"],
        base_url=config["LLM_API_URL"],
        timeout=30,
        max_retries=0,
    )


def call_model(client, model_name, messages, tools=None):
    # 1. 准备请求参数
    request = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.6,
    }

    # 2. 如果提供了工具说明，就一起发送
    if tools:
        request["tools"] = tools
        request["tool_choice"] = "auto"

    # 3. 请求模型
    response = client.chat.completions.create(**request)

    # 4. 返回完整的助手消息对象
    return response.choices[0].message