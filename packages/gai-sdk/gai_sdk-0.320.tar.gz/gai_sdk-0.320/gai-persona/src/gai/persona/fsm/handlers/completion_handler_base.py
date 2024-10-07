import logging, json,re
from typing import List, Optional
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.ttt.client.ttt_client import TTTClient
from gai.agent.dialogue.pydantic.MonologueMessagePydantic import MonologueMessagePydantic

class CompletionHandlerBase:

    def handle_completion(self, 
                 ttt: TTTClient,
                 messages: List[MonologueMessagePydantic] | list,
                 tool_choice: str,
                 tools_dict: dict=None,
                 json_schema: Optional[dict]=None,
                 stream:bool = True,
                 max_new_tokens:int = 1000,
                 max_tokens:int = 1000,
                 temperature:float=None,
                 top_p:float=None,
                 top_k:float=None,
                 stop_conditions:dict=None
                 ):
        
        # Convert MonologueMessages to ChatMessages
        if isinstance(messages, list) and all(isinstance(m, MonologueMessagePydantic) for m in messages):
            messages = [{"role":message.Role, "content":message.Content} for message in messages]
        if isinstance(messages,list) and not all("role" in m and "content" in m for m in messages):
            raise Exception(f"Invalid message format: {messages}")
        
        self.finish_reason = None
        self.content=""
        self.streamer = None

        tools_list=None
        if tools_dict:
            tools_list = list(tools_dict.values())
        
        # clean up whitespace from system messages
        for message in messages:
            if message["role"] == "system":
                message["content"] = re.sub(r'\s+',' ',message["content"])
        try:

            if (stream):
                # STREAMING -----------------

                def do_stream():
                    chunks=ttt(messages=messages, 
                                stream=stream, 
                                tools=tools_list,
                                json_schema=json_schema,
                                max_new_tokens=max_new_tokens, 
                                max_tokens=max_tokens,
                                temperature=temperature, 
                                top_p=top_p, 
                                top_k=top_k,
                                tool_choice=tool_choice,
                                stop_conditions=stop_conditions
                                )
                    for chunk in chunks:
                        decoded = chunk.extract()

                        if isinstance(decoded, str):

                            # Start streaming as long as the response is text
                            self.content += decoded
                            yield decoded

                return (chunk for chunk in do_stream())
            else:
                # GENERATING -----------------
                self.content = ttt(
                        messages=messages,
                        stream=False,
                        tools=tools_list,
                        json_schema=json_schema,
                        max_new_tokens=max_new_tokens,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k,
                        tool_choice=tool_choice,
                        stop_conditions=stop_conditions
                        )
                decoded = self.content.extract()

                # content
                if "content" in decoded:
                    self.content = decoded["content"]
                    if not isinstance(self.content, str):
                        self.content = json.dumps(self.content)
               
                # function
                if "type" in decoded and decoded["type"] == "function":
                    self.content = json.dumps(decoded)
                
                logger.info(f"on_GENERATE_handler:{self.content}")
                return self.content
        except Exception as e:
            logger.error(e)
            raise e    

    def stream_chunk(self, chunk):
        self.content += chunk
        return chunk            
