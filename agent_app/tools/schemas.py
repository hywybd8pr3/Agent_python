TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算两个数字的和，适用于两个数字相加。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "第一个数字",
                    },
                    "b": {
                        "type": "number",
                        "description": "第二个数字",
                    },
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": (
                "演示天气查询流程。"
                "仅返回收到的城市名，不提供实时天气。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "要查询的城市",
                    },
                },
                "required": ["city"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "演示搜索流程。"
                "仅返回收到的关键词，不进行真实联网搜索。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]

TOOL_SCHEMAS.extend([
    {
        "type": "function",
        "function": {
            "name": "add_note",
            "description": (
                "将用户明确要求保存的标题和正文保存为本地笔记。"
                "每次成功调用都会新建一份笔记；"
                "不要重复保存同一次请求。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "用户要求保存的笔记标题",
                    },
                    "content": {
                        "type": "string",
                        "description": "用户要求保存的笔记正文",
                    },
                },
                "required": ["title", "content"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "列出本地笔记的编号和标题，不返回正文。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": (
                "按已有编号读取本地笔记全文。"
                "编号必须来自 add_note、list_notes 或 search_notes 的结果，"
                "不要编造。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": (
                            "工具返回的 32 位小写十六进制笔记编号"
                        ),
                    },
                },
                "required": ["note_id"],
                "additionalProperties": False,
            },
        },
    },
])

TOOL_SCHEMAS.append({
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": (
            "在本地笔记标题和正文中进行不区分大小写的关键词子串搜索。"
            "返回匹配总数及有限条笔记编号、标题、正文开头预览。"
            "查询词应是简短关键词，不是完整问题。"
            "预览不是全文；回答具体内容前应调用 read_note。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "要查找的非空关键词，例如 Agent 或 工具调用"
                    ),
                },
                "limit": {
                    "type": "integer",
                    "description": (
                        "最多返回多少条，省略时为 5，范围 1 到 10"
                    ),
                    "minimum": 1,
                    "maximum": 10,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
})