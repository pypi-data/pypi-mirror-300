from portkey_ai import Portkey
from typing import Dict, List, Optional
import random

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class BaseModel:
    def __init__(self, api_key: str, virtual_key: str, config_id: str):
        self.portkey = Portkey(api_key=api_key, virtual_key=virtual_key, config=config_id)

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        raise NotImplementedError

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        raise NotImplementedError

class AzureModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        common_params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096
        }
        if top_p != 0:
            common_params["top_p"] = top_p
        return self.portkey.chat.completions.create(**common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        common_params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
            "stream": True
        }
        if top_p != 0:
            common_params["top_p"] = top_p
        return self.portkey.chat.completions.create(**common_params)

class BedrockModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        common_params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
        }
        if top_p != 0:
            common_params["top_p"] = top_p
        return self.portkey.chat.completions.create(**common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        common_params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
            "stream": True,
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
        }
        if top_p != 0:
            common_params["top_p"] = top_p
        return self.portkey.chat.completions.create(**common_params)

class GeminiModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        common_params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
            "model": "gemini-1.5-pro"
        }
        if top_p != 0:
            common_params["top_p"] = top_p
        return self.portkey.chat.completions.create(**common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        common_params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
            "stream": True,
            "model": "gemini-1.5-pro"
        }
        if top_p != 0:
            common_params["top_p"] = top_p
        return self.portkey.chat.completions.create(**common_params)

class AIGateway:
    _instance = None

    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure": "azure-7e4746",
        "bedrock": "bedrock-bfa916",
        "gemini": "gemini-b5d385",
        "dalle3": "dalle3-ea9815"
    }

    MODEL_WEIGHTS = {
        "azure": 0.6,
        "bedrock": 0.4,
        "gemini": 0.0,  # Added Gemini with 0 weight for non-streaming
    }

    STREAM_MODEL_WEIGHTS = {
        "azure": 0.4,
        "bedrock": 0.3,
        "gemini": 0.3
    }

    CODING_MODEL_WEIGHTS = {
        "azure": 0.2,
        "bedrock": 0.8,
        "gemini": 0.0
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIGateway, cls).__new__(cls)
            cls._instance.azure_model = AzureModel(cls.API_KEY, cls.VIRTUAL_KEYS["azure"], cls.CONFIG_ID)
            cls._instance.bedrock_model = BedrockModel(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock"], cls.CONFIG_ID)
            cls._instance.gemini_model = GeminiModel(cls.API_KEY, cls.VIRTUAL_KEYS["gemini"], cls.CONFIG_ID)
            logger.debug("AIGateway initialized with all models")
        return cls._instance

    def _select_model(self, weights, exclude=None):
        available_models = {k: v for k, v in weights.items() if k != exclude}
        if not available_models:
            raise ValueError("No available models to choose from")
        return random.choices(list(available_models.keys()), 
                              weights=list(available_models.values()), 
                              k=1)[0]

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        tried_models = set()
        while len(tried_models) < len(self.MODEL_WEIGHTS):
            model_type = self._select_model(self.MODEL_WEIGHTS, exclude=tried_models)
            tried_models.add(model_type)
            try:
                model = getattr(self, f"{model_type}_model")
                completion = await model.prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model")
                return completion
            except Exception as e:
                logger.error(f"Error in prompting {model_type} model: {str(e)}")
        
        raise Exception("All models failed to respond")
    
    async def coding_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        tried_models = set()
        while len(tried_models) < len(self.CODING_MODEL_WEIGHTS):
            model_type = self._select_model(self.CODING_MODEL_WEIGHTS, exclude=tried_models)
            tried_models.add(model_type)
            try:
                model = getattr(self, f"{model_type}_model")
                completion = await model.prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model")
                return completion
            except Exception as e:
                logger.error(f"Error in prompting {model_type} model: {str(e)}")
        
        raise Exception("All models failed to respond")

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        tried_models = set()
        while len(tried_models) < len(self.STREAM_MODEL_WEIGHTS):
            model_type = self._select_model(self.STREAM_MODEL_WEIGHTS, exclude=tried_models)
            tried_models.add(model_type)
            try:
                model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received streaming response from {model_type} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        final_response += content
                print()
                return final_response
            except Exception as e:
                logger.error(f"Error in streaming from {model_type} model: {str(e)}")
        
        raise Exception("All models failed to respond")

    def generate_image(self, prompt: str, size: str = "1024x1024"):
        dalle_model = Portkey(api_key=self.API_KEY, virtual_key=self.VIRTUAL_KEYS["dalle3"], config=self.CONFIG_ID)
        try:
            image = dalle_model.images.generate(prompt=prompt, size=size)
            logger.debug("Successfully generated image with DALL-E 3 model")
            return image
        except Exception as e:
            logger.error(f"Error in generating image with DALL-E 3: {str(e)}")
            raise
