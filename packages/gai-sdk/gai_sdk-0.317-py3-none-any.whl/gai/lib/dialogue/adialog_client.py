import json
from abc import ABC, abstractmethod
from gai.lib.dialogue.dialog_message import DialogueMessage

class ADialogClient(ABC):

    @staticmethod
    # """
    # Description: Extract last_n messages from the dialogue and convert into string for use as context.
    # """
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

    @abstractmethod
    def register(self, persona, dialog_callback):
        pass

    @abstractmethod
    def list_dialogue_messages(self):
        pass

    @abstractmethod
    def update_dialogue(self, user_message_id:str, user_id:str, user_message:str, agent_name:str, monologue:str):
        pass