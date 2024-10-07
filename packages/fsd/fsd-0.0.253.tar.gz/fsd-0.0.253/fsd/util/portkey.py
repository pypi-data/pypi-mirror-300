from portkey_ai import Portkey
from typing import Dict, List, Optional
import random

import base64
import io
from PIL import Image
import requests

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class AIGateway:
    """
    A gateway for interfacing with various AI models provided by Portkey.

    This class provides an abstraction layer over different AI model types,
    allowing for seamless interaction with Azure, Bedrock, DALL-E 3, and Google Gemini models.

    Attributes:
        portkey (Portkey): The Portkey client used to interact with the AI models.
        model_type (str): The type of AI model to use (e.g., "azure", "bedrock", "dalle3", "gemini").
    """

    # Constants for API configuration
    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    # Mapping of model types to their respective virtual keys
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure": "azure-7e4746",
        "bedrock": "bedrock-bfa916",
        "dalle3": "dalle3-ea9815",
        "gemini": "gemini-b5d385"
    }

    def __init__(self, model_type: str = "azure"):
        """
        Initializes the AIGateway with a specific type of AI model.

        Args:
            model_type (str): The type of AI model to use. Defaults to "azure".
                              Supported types: "azure", "bedrock", "dalle3", "gemini".

        Raises:
            ValueError: If an unsupported model type is provided.
        """
        if model_type not in self.VIRTUAL_KEYS:
            raise ValueError(f"Unsupported model type: {model_type}. Supported types are: {', '.join(self.VIRTUAL_KEYS.keys())}")

        self.model_type = model_type
        virtual_key = self.VIRTUAL_KEYS[model_type]

        self.portkey = Portkey(
            api_key=self.API_KEY,
            virtual_key=virtual_key,
            config=self.CONFIG_ID
        )
        #logger.debug(f"AIGateway initialized with model type: {model_type}")

    def _get_balanced_model(self):
        """
        Randomly selects a model type for load balancing.

        Returns:
            str: The selected model type ("azure", "bedrock", or "gemini").
        """
        return random.choice(["azure", "bedrock", "gemini"])

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        """
        Sends messages to a randomly selected AI model and receives responses.

        This method handles the differences in API calls between Azure, Bedrock, and Gemini models.

        Args:
            messages (List[Dict[str, str]]): The messages or prompts to send to the AI.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 4096.
            temperature (float): The randomness of the response. Defaults to 0.2.
            top_p (float): The nucleus sampling rate. Defaults to 0.

        Returns:
            Dict: The AI's response.

        Raises:
            Exception: If there's an error in making the API call.
        """
        try:
            selected_model = self._get_balanced_model()
            self.model_type = selected_model
            self.portkey.virtual_key = self.VIRTUAL_KEYS[selected_model]

            common_params = {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            if top_p != 0:
                common_params["top_p"] = top_p

            if selected_model == "bedrock":
                common_params["model"] = "anthropic.claude-3-5-sonnet-20240620-v1:0"
            elif selected_model == "gemini":
                common_params["model"] = "gemini-1.5-pro"

            completion = self.portkey.chat.completions.create(**common_params)
            #logger.debug(f"Successfully received response from {selected_model} model")
            return completion
        except Exception as e:
            logger.error(f"Error in prompting {selected_model} model: {str(e)}")
            raise

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        """
        Sends messages to a randomly selected AI model and receives responses in a streaming fashion.

        This method handles the differences in API calls between Azure, Bedrock, and Gemini models.

        Args:
            messages (List[Dict[str, str]]): The messages or prompts to send to the AI.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 4096.
            temperature (float): The randomness of the response. Defaults to 0.2.
            top_p (float): The nucleus sampling rate. Defaults to 0.

        Returns:
            str: The AI's response as a concatenated string.

        Raises:
            Exception: If there's an error in making the API call.
        """
        try:
            selected_model = self._get_balanced_model()
            self.model_type = selected_model
            self.portkey.virtual_key = self.VIRTUAL_KEYS[selected_model]

            common_params = {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }

            if top_p != 0:
                common_params["top_p"] = top_p

            if selected_model == "bedrock":
                common_params["model"] = "anthropic.claude-3-5-sonnet-20240620-v1:0"
            elif selected_model == "gemini":
                common_params["model"] = "gemini-1.5-pro"

            chat_completion_stream = self.portkey.chat.completions.create(**common_params)
            #logger.debug(f"Successfully received response from {selected_model} model")
            final_response = ""
            for chunk in chat_completion_stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end='', flush=True)
                    final_response += content

            print()  # Print a new line after streaming
            return final_response
                
        except Exception as e:
            logger.error(f"Error in prompting {selected_model} model: {str(e)}")
            raise

    def generate_image(self, prompt: str, size: str = "1024x1024"):
        if self.model_type != "dalle3":
            raise ValueError("Image generation is only supported with the DALL-E 3 model.")

        try:
            image = self.portkey.images.generate(
                prompt=prompt,
                size=size
            )
            return image
        except Exception as e:
            logger.error(f"Error in generating image with DALL-E 3: {str(e)}")
            raise

