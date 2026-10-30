import json
from pathlib import Path 
from tempfile import TemporaryDirectory

SESSION_FILE = Path(__file__).resolve().parents[1]/"data"/"session.json"

def _validate_history(history):
    '''检查项目的消息结构，完整轮次，工具请求/结果匹配'''
    if not isinstance(history,list):
        raise ValueError("存档中的message必须是列表")

    expected = "user"
    pending_ids = set()

    for message in history:
        if not isinstance(message,dict):
            raise ValueError("每条消息必须是字典")

        role = message.get("role")
        content = message.get("content")

        if role != expected:
            raise ValueError(f"消息顺序错误：应为{expected}，实际为{role}")

        if role == "user":
            if set(message) != {"role" , "content"}:
                raise ValueError("用户消息字段不正确")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("用户消息必须有文字。")
            expected = "assistant"

        elif role == "assistant":
            if set(message) - {"role","content","tool_calls"}:
                raise ValueError("助手消息包含本项目不支持的字段。")

            calls = message.get("tool_calls",[])

            if not isinstance(calls,list):
                raise ValueError("tool_calls 必须是列表")

            if calls:
                if content is not None and not isinstance(content,str):
                    raise ValueError("请求的content必须是文字或者Null")
                for call in calls:
                    if(
                        not isinstance(call,dict) or set(call) != {"id","type","function"}
                    ):
                        raise ValueError("请求字段不完整或者不受支持")

                    call_id = call["id"]
                    function = call["function"]

                    if (not isinstance(call_id,str) or not call_id.strip() or call_id in pending_ids):
                        raise ValueError("同一批工具请求ID必须非空且不重复")

                    if (call["type"] != "function" or not isinstance(function,dict)):
                        raise ValueError("只支持function工具请求")

                    if set(function) != {"name","arguments"}:
                        raise ValueError("工具请求的name,arguments不正确")

                    if (not isinstance(function["name"],str) or not function["name"].strip()):
                        raise ValueError("工具名称必须是非空字符串")

                    if not isinstance(function["arguments"],str):
                        raise ValueError("工具参数arguments必须是字符串格式")

                    pending_ids.add(call_id)
                expected = "tool"
            else:
                if not isinstance(content,str) or not content.strip():
                    raise ValueError("回答必须有文字")
                expected = "user"

        elif role == "tool":
            if set(message) != {"role","tool_call_id","content"}:
                raise ValueError("工具结果字段不正确")

            call_id = message["tool_call_id"]

            if (not isinstance(call_id,str) or call_id not in pending_ids):
                 raise ValueError(
                    "工具结果找不到对应请求，或结果重复。"
                )

            if not isinstance(content, str):
                raise ValueError("工具结果必须是字符串。")

            pending_ids.remove(call_id)

            if not pending_ids:
                expected = "assistant"

    if expected != "user":
        raise ValueError(
            "聊天尚未形成完整轮次，不能保存或恢复。"
        )


def save_message(messages):
    '''保存正式历史，不保存ststem，加载时使用代码中的当前提示词'''
    if not isinstance(messages,list) or not messages:
        raise ValueError("message必须是system中的消息列表")

    first = messages[0]

    if not isinstance(first,dict) or first.get("role") != "system":
        raise ValueError("第一条消息必须时system")

    history = messages[1:]

    _validate_history(history)

    payload = {"version" :1,"messages":history}

    text = json.dumps(payload,ensure_ascii=False,indent=2)

    SESSION_FILE.parent.mkdir(parents =True,exist_ok = True)

    #先写完临时文件，再替换上次存档
    with TemporaryDirectory( dir=SESSION_FILE.parent,
        prefix=".session-",) as directory:
        temp_path = Path(directory) / "session.json"
        temp_path.write_text(text, encoding="utf-8")
        temp_path.replace(SESSION_FILE)


def load_session():
    """返回存档的聊天部分；由 CLI 加上当前 system 消息。"""
    text = SESSION_FILE.read_text(encoding="utf-8")
    payload = json.loads(text)

    if not isinstance(payload, dict):
        raise ValueError("存档顶层必须是 JSON 对象。")

    if (
        type(payload.get("version")) is not int
        or payload["version"] != 1
    ):
        raise ValueError("不支持这个存档版本。")

    history = payload.get("messages")
    _validate_history(history)

    return history



                
                   

        