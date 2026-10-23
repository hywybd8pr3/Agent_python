from openai import OpenAI

def create_client(config):
    return OpenAI(
        api_key = config['LLM_API_KEY'],
        base_url = config['LLM_API_URL'],
        timeout = 30,
        max_retries=0,)

def call_model(client,model_name,messages):
    response = client.chat.completions.create(
        model = model_name,
        messages = messages,
        temperature = 0.6
    )

    return response.choices[0].message
