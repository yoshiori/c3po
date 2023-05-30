import json
import logging, os

logging.basicConfig(level=logging.DEBUG)

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
        'user': user_map[message['user']],
        'ts': message['ts']
        }
    history.append(chat)
print(json.dumps(history[0:10]))
