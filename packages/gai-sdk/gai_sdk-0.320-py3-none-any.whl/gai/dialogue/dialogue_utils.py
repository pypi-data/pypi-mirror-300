import json
from gai.lib.dialogue.dialogue_message import DialogueMessage

def ExtractRecap(messages:list[DialogueMessage] , last_n:int=6) -> str:
    recap = []

    # Get past messages and last user message
    for message in messages:

        # ignore placeholder
        if not message.Content:
            continue

        # ignore images
        if message.Content.startswith('data:image'):
            continue

        if message.Role == 'user':
            recap.append({"user": message.Content})
        else:
            recap.append({message.Name: message.Content})

    # Recap last n messages and inject into monologue template [1]
    recap = recap[-last_n:]

    # Convert to JSON string
    recap = json.dumps(recap)

    return recap