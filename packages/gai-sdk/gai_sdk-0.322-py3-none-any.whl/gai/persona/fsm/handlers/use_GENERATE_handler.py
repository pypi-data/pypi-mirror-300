from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.agent.fsm.handlers.completion_handler_base import CompletionHandlerBase

class use_GENERATE_handler(CompletionHandlerBase):

    def on_GENERATE(self):

        # Fixed attributes
        stream = True
        tool_choice = "none"
        tools_dict = None
        json_schema = None

        # required attributes
        messages = self.monologue_messages
        ttt = self.ttt
        max_new_tokens=self.max_new_tokens
        max_tokens=self.max_tokens
        temperature=self.temperature
        top_p=self.top_p
        top_k=self.top_k
        stop_conditions=self.stop_conditions

        content=self.handle_completion(ttt=ttt,
            messages=messages,
            tools_dict=tools_dict,
            json_schema=json_schema,
            stream=stream,
            max_new_tokens=max_new_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            tool_choice=tool_choice,
            stop_conditions=stop_conditions,
            )
        
        if stream:
            self.content = ""
            self.streamer = (chunk for chunk in content )
        else:
            self.content = content

        if hasattr(self, "state"):
            logger.info({"state": self.state, "data": self.content})
            self.step+=1
            self.results.append({"state": self.state, "result": self.content,"step": self.step})     