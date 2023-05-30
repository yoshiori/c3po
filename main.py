import json
import logging, os

logging.basicConfig(level=logging.INFO)

from slack_sdk import WebClient
client = WebClient(os.environ["SLACK_API_TOKEN"])

response = client.conversations_history(
    channel="C013ZEZ5VQD"
)

messages = response.data['messages']
user_ids = set([message['user'] for message in filter(lambda message: 'user' in message.keys(), messages)])
user_map = dict([[user_id, client.users_info(user=user_id)['user']['name'] ] for user_id in user_ids])

history = []
for message in filter(lambda message: 'user' in message.keys(), messages):
    chat = {
        'text': message['text'],
        'user': message['user'],
        'ts': message['ts']
        }
    history.append(chat)
history_json = json.dumps(history[:30])
for user_id, name in user_map.items():
    history_json = history_json.replace(user_id, name)

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

llm = ChatOpenAI(temperature=0)

template="""
You are an excellent chat summarization assistant. I'm going to give you the chat history in JSON format, please output a summary.
Output the results in English and Japanese.
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template="{history}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

request = chat_prompt.format_prompt(
    history=history_json,
).to_messages()
response = llm(request)

print(f"""
summary: {response.content}
number of tokens in request: {llm.get_num_tokens_from_messages(request)}""")
