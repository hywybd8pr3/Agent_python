import json 
from pathlib import Path
from uuid import uuid4

NOTES_DIR = Path(__file__).resolve().parents[2] /"data" /"notes"

def _note_path(note_id:str) -> Path:
    '''只接受程序生成的编号，不接受任意文件路径'''
    if(
        not isinstance(note_id,str)
        or len(note_id) != 32
        or any(char not in "0123456789abcdef" for char in note_id)
    ):
        raise ValueError("note_id必须是工具返回的32位小写十六进制编号")

    return NOTES_DIR / f"{note_id}.json"

def _load_note(note_id:str) -> dict:
    '''读取并检查一笔记，供下面两个工具复用'''
    path = _note_path(note_id)

    try:
        with path.open("r", encoding="utf-8") as file:
            note = json.load(file)            
    except FileNotFoundError as e:
        raise ValueError(f"笔记不存在:{note_id}") from e

    except(json.JSONDecodeError,UnicodeError) as e:
        raise ValueError(f"笔记无法解析：{note_id}") from e

    if(
        not isinstance(note,dict)
        or note.get("note_id") != note_id
        or not isinstance(note.get("title"),str)
        or not note["title"].strip()
        or not isinstance(note.get("content"),str)
        or not note["content"].strip()
    ):
        raise ValueError(f"笔记文件结构不正确：{note_id}")

    return note

def add_note(title:str,content:str) -> str:
    '''创建一份笔记，返回实际保存的编号和选题'''
    if not isinstance(title,str) or not title.strip():
        raise ValueError("title 必须是非空字符串")

    if not isinstance(content,str) or not content.strip():
        raise ValueError("content 必须是非空字符串")

    note_id = uuid4().hex

    note = {"note_id" : note_id,
            "title" : title,
            "content" : content}

    NOTES_DIR.mkdir(parents = True, exist_ok = True)
    path = _note_path(note_id)

     # x 表示新建；如果编号已存在，报错而不是覆盖原文件。
    with path.open("x", encoding="utf-8") as file:
        json.dump(
            note,file,ensure_ascii=False,indent=2
        )
    return json.dumps(
        {
            "status" : "saved",
            "note_id" : note_id,
            "title" : note["title"]
        },
        ensure_ascii=False
    )

def list_notes() -> str:
    '''列出编号和标题，保存笔记时返回空列表'''
    try:
        paths = sorted(NOTES_DIR.iterdir())
    except FileNotFoundError:
        return"[]"

    items = []

    for path in paths:
        if path.suffix == ".json":
            note = _load_note(path.stem)
            items.append({
                "note_id" : note["note_id"],
                "title" : note["title"]
            })
    return json.dumps(items,ensure_ascii=False)

def read_note(note_id:str) -> str:
    '''根据已有编号读取笔记，包括完整正文'''
    note = _load_note(note_id)
    return json.dumps(note,ensure_ascii=False)

def search_notes(query:str,limit = 5) -> str:
    '''按照标题或者正文关键词查找笔记，返回有限数量的预览'''
    if not isinstance(query,str) or not query.strip():
        raise ValueError("query 必须是非空字符串")

    if type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("limit 必须是 1 到 10 之间的整数")

    query = query.strip()

    keyword = query.casefold()#忽略大小写

    result = {
        "query" : query,
        "total" : 0,
        "returned" : 0,
        "truncated" : False,
        "items" : [],
        
    }

    try:
        paths = sorted(NOTES_DIR.iterdir())
    except FileNotFoundError:
        return json.dumps(result,ensure_ascii=False)

    for path in paths:
        if path.suffix != ".json":
            continue

        note = _load_note(path.stem)

        if (
            keyword not in note["title"].casefold() and
            keyword not in note["content"].casefold()
        ):
            continue

        result["total"] += 1

        if len(result["items"]) < limit:
            preview = note["content"][:120]

            if len(note["content"]) > 120:
                preview += "..."

            result["items"].append({
                "note_id" : note["note_id"],
                "title" : note["title"],
                "preview" : preview
            })


    result["returned"] = len(result["items"])
    result["truncated"] = result["total"] > result["returned"]

    return json.dumps(result,ensure_ascii= False)




    