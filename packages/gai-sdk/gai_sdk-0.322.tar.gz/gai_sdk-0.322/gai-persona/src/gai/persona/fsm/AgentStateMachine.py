import os
from typing import Optional, Callable, List

from gai.lib.common.utils import this_dir
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.rag.client.rag_client_async import RagClientAsync
from gai.ttt.client.ttt_client import TTTClient
from gai.agent.fsm.FSMBase import FSMBase
from gai.agent.profile.pydantic.AgentPydantic import AgentPydantic
from gai.agent.dialogue.pydantic.DialogueMessagePydantic import DialogueMessagePydantic
from gai.agent.fsm.handlers.use_CRAFT_PROMPT_handler import use_CRAFT_PROMPT_handler
from gai.agent.fsm.handlers.use_TOOL_CHOICE_handler import use_TOOL_CHOICE_handler
from gai.agent.fsm.handlers.use_GENERATE_handler import use_GENERATE_handler
from gai.agent.fsm.handlers.use_GOOGLE_handler import use_GOOGLE_handler
from gai.agent.fsm.handlers.use_PROCESS_handler import use_PROCESS_handler
from gai.agent.fsm.handlers.use_RETRIEVAL_handler import use_RETRIEVAL_handler
from gai.agent.fsm.handlers.use_TOOL_CALL_handler import use_TOOL_CALL_handler
from gai.agent.fsm.handlers.use_ERROR_handler import use_ERROR_handler
from gai.agent.fsm.handlers.use_BOOLEAN_handler import use_BOOLEAN_handler

# The AgentStateMachine is created by integrating  6 parent classes together.
# It then combine with its own state handler called on_CRAFT_PROMPT_handler to provide a customed prompting message.
# The difference between AgentStateMachine and Agent is that the FSM does not have the ability to interact with external services such as the database and dialogue channels.

class AgentStateMachine(FSMBase,
                        use_CRAFT_PROMPT_handler,
                        use_TOOL_CHOICE_handler,
                        use_TOOL_CALL_handler,
                        use_GENERATE_handler,
                        use_PROCESS_handler,
                        use_GOOGLE_handler,
                        use_RETRIEVAL_handler,
                        use_ERROR_handler,
                        use_BOOLEAN_handler
                        ):

    def __init__(self,
                ttt:TTTClient,
                rag: RagClientAsync,
                collection_name: str,
                user_message:str,
                agent_data: AgentPydantic,
                dialogue_messages: List[DialogueMessagePydantic],
                tools_dict:dict,
                status_updater: Optional[Callable] = None,
                n_search:int=3,
                n_rag:int=4,
                max_new_tokens:int=None,
                max_tokens:int=None,
                temperature:float=None,
                top_p:float=None,
                top_k:float=None,
                stop_conditions:List[str]=None,
                tool_choice:str="auto",
                tool_name:str="text",
                state_diagram_path:str=None,
                state_diagram:str=None,
                custom_message:str=None,
                ):
        
        FSMBase.__init__(self, state_diagram_path=state_diagram_path, state_diagram=state_diagram)
        use_ERROR_handler.__init__(self)
        
        # init states
        self.ttt=ttt
        self.rag=rag
        self.user_message=user_message
        self.agent_name = agent_data.Name
        self.tool_name = tool_name
        self.tools_dict = tools_dict
        self.schema=None
        self.dialogue_messages=dialogue_messages
        self.monologue_messages=[]
        self.agent_data = agent_data
        if not collection_name:
            raise Exception("collection_name cannot be empty.")
        self.collection_name = collection_name
        self.custom_message = custom_message
        
        # hyperparameters
        self.stream=True
        self.n_search=n_search
        self.n_rag=n_rag
        self.max_new_tokens=max_new_tokens
        self.max_tokens=max_tokens
        self.temperature=temperature
        self.top_p=top_p
        self.top_k=top_k
        self.tool_choice=tool_choice
        self.stop_conditions=stop_conditions

        # tracing
        self.results = []
        self.step = 0
        self.status_updater=status_updater

    def use_text(self):
        return self.tool_name=="text"

