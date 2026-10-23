from agent_app.model_client import call_model
def create_message():
    ''' 创建一份新的对话历史，保留助手的基本设定'''
    return [
        {
            'role':'system',
            'content':'你是一个用中文简洁回答问题的AI助手'
        }
    ]

def run_turn(client,messages,model,user_input):

    ''' 完成一轮对话后，成功更新历史，并返回回答文字'''

    #1.整理第一轮用户信息
    user_message = {'role':'user','content':user_input}

    #2.创建本次请求使用的消息列表
    request_messages = messages + [user_message]

    #3.调用模型
    message = call_model(
        client = client,
        messages = request_messages,
        model_name = model       
    )

    #4.从消息对象中获取回答
    answer = message.content

    if not isinstance(answer,str) or not answer:
        raise ValueError('模型没有可显示的文本回答')

    #5.将问题和回答一起加入历史
    messages.append(user_message)
    messages.append({'role':'assistant','content':answer})

    #6.将文字返回给cli.py打印
    return answer


