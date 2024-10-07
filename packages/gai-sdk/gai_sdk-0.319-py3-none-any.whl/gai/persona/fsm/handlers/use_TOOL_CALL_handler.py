from gai.lib.common.logging import getLogger
from gai.agent.fsm.handlers.completion_handler_base import CompletionHandlerBase
logger = getLogger(__name__)

"""
This is the second part of the tool call. It is called after the tool choice has been made.
It is implemented from a copy of use_GENERATE_handler.py that is configured for tool calls.
Tool Calls:
- stream=False
- json_schema=None
- tool_choice="required"
- temperature=0
- top_p=0.5
- top_k=1
"""

class use_TOOL_CALL_handler(CompletionHandlerBase):

    def on_TOOL_CALL(self):

        # Fixed attributes
        stream = False
        tool_choice = "required"
        tool = self.tools_dict[self.tool_name]
        json_schema = None
        temperature=0
        top_p=0.5
        top_k=1

        # required attributes
        messages = self.monologue_messages
        ttt = self.ttt
        max_new_tokens=self.max_new_tokens
        max_tokens=self.max_tokens

        content=self.handle_completion(ttt=ttt,
            messages=messages,
            tools_dict=tool,
            json_schema=json_schema,
            stream=False,
            max_new_tokens=max_new_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            tool_choice=tool_choice,
            )
        
        self.content = content
        self.TOOL_CALL_output=content

        if hasattr(self, "state"):
            logger.info({"state": self.state, "data": self.content})
            self.step+=1
            self.results.append({"state": self.state, "result": self.content,"step": self.step})