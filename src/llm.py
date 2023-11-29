'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
from langchain.llms import CTransformers
from langchain.llms import LlamaCpp
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import find_dotenv, load_dotenv
import box
import yaml
from typing import Any, Dict, List, Optional

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

DEFAULT_ANSWER_PREFIX_TOKENS = ["Final", "Answer", ":"]

# Setup token streaming for streamlit. Obtained from: https://gist.github.com/goldengrape/84ce3624fd5be8bc14f9117c3e6ef81a
class StreamDisplayHandler(BaseCallbackHandler):
    
    def append_to_last_tokens(self, token: str) -> None:
        self.last_tokens.append(token)
        self.last_tokens_stripped.append(token.strip())
        if len(self.last_tokens) > len(self.answer_prefix_tokens):
            self.last_tokens.pop(0)
            self.last_tokens_stripped.pop(0)

    def check_if_answer_reached(self) -> bool:
        if self.strip_tokens:
            return self.last_tokens_stripped == self.answer_prefix_tokens_stripped
        else:
            return self.last_tokens == self.answer_prefix_tokens
    
    def __init__(self, container, initial_text="", display_method='markdown', 
                 answer_prefix_tokens: Optional[List[str]] = None,        
                 strip_tokens: bool = True,
                 stream_prefix: bool = False):
        super().__init__()
        if answer_prefix_tokens is None:
            self.answer_prefix_tokens = DEFAULT_ANSWER_PREFIX_TOKENS
        else:
            self.answer_prefix_tokens = answer_prefix_tokens
        if strip_tokens:
            self.answer_prefix_tokens_stripped = [
                token.strip() for token in self.answer_prefix_tokens
            ]
        else:
            self.answer_prefix_tokens_stripped = self.answer_prefix_tokens
        self.last_tokens = [""] * len(self.answer_prefix_tokens)
        self.last_tokens_stripped = [""] * len(self.answer_prefix_tokens)
        self.strip_tokens = strip_tokens
        self.stream_prefix = stream_prefix
        self.answer_reached = False
        
        self.container = container
        self.text = initial_text
        self.display_method = display_method
        self.new_sentence = ""
    
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Run when LLM starts running."""
        self.answer_reached = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # Remember the last n tokens, where n = len(answer_prefix_tokens)
        self.append_to_last_tokens(token)
        
        if self.check_if_answer_reached():
            self.text += token
            self.new_sentence += token

            display_function = getattr(self.container, self.display_method, None)
            if display_function is not None:
                display_function(self.text)
            else:
                raise ValueError(f"Invalid display_method: {self.display_method}")

    def on_llm_end(self, response, **kwargs) -> None:
        self.text=""


def build_llm(model_path, length, temp, gpu_layers, chat_box=None):
    # Local LlamaCpp model, automatically supports multiple model types
    llm = LlamaCpp(model_path=model_path,
                    max_tokens=length, 
                    temperature=temp,
                    n_gpu_layers=gpu_layers,
                    n_batch=128, # ! arbitrary
                    callbacks=[
                        StreamingStdOutCallbackHandler() if not chat_box else # streaming for main.py else main_st.py
                        StreamDisplayHandler(chat_box, display_method='write')],
                    verbose=False, # suppresses llama_model_loader output
                    streaming=True,
                    n_ctx=2048 # ! arbitrary
                    )
    return llm