from portkey_ai import Portkey
from typing import Dict, List, Optional
import random
from collections import deque
import time

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
    allowing for seamless interaction with Azure, Bedrock, Google Gemini, and DALL-E 3 models.

    Attributes:
        portkey_clients (Dict[str, Portkey]): Dictionary of Portkey clients for each model type.
        model_queue (deque): A queue of model types for load balancing.
        model_usage (Dict[str, int]): Tracks usage count for each model.
        error_counts (Dict[str, int]): Tracks error count for each model.
        last_reset (float): Timestamp of the last reset of usage and error statistics.
    """

    # Constants for API configuration
    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    # Mapping of model types to their respective virtual keys
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure": "azure-7e4746",
        "bedrock": "bedrock-bfa916",
        "gemini": "gemini-b5d385",
        "dalle3": "dalle3-ea9815"
    }

    def __init__(self):
        """
        Initializes the AIGateway with load balancing capabilities for multiple AI models.
        """
        self.models = ["azure", "bedrock", "gemini"]
        self.portkey_clients = {model: Portkey(api_key=self.API_KEY, virtual_key=key, config=self.CONFIG_ID) 
                                for model, key in self.VIRTUAL_KEYS.items()}
        self.model_queue = deque(self.models)
        self.model_usage = {model: 0 for model in self.models}
        self.error_counts = {model: 0 for model in self.models}
        self.last_reset = time.time()
        self.reset_interval = 3600  # Reset stats every hour
        self.current_model = None

    def _get_next_model(self):
        """
        Selects the next model to use based on usage and error statistics.
        """
        self._check_reset()
        
        # Sort models by least used and least errors
        sorted_models = sorted(self.models, key=lambda x: (self.model_usage[x], self.error_counts[x]))
        
        # Log the current stats
        logger.info(f"Current model stats - Usage: {self.model_usage}, Errors: {self.error_counts}")
        logger.info(f"Selected model: {sorted_models[0]}")
        
        # Set the current model
        self.current_model = sorted_models[0]
        
        # Return the best candidate
        return self.current_model

    def _check_reset(self):
        """
        Resets usage and error statistics if the reset interval has passed.
        """
        current_time = time.time()
        if current_time - self.last_reset > self.reset_interval:
            self.model_usage = {model: 0 for model in self.models}
            self.error_counts = {model: 0 for model in self.models}
            self.last_reset = current_time
            logger.info("Reset model usage and error statistics.")

    def _update_stats(self, success=True):
        """
        Updates the usage and error statistics for the current model.
        """
        if self.current_model:
            if success:
                self.model_usage[self.current_model] += 1
                logger.info(f"Updated usage for {self.current_model}: {self.model_usage[self.current_model]}")
            else:
                self.error_counts[self.current_model] += 1
                logger.info(f"Updated error count for {self.current_model}: {self.error_counts[self.current_model]}")

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        """
        Sends messages to the AI model and receives responses with load balancing.

        Args:
            messages (List[Dict[str, str]]): The messages or prompts to send to the AI.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 4096.
            temperature (float): The randomness of the response. Defaults to 0.2.
            top_p (float): The nucleus sampling rate. Defaults to 0.

        Returns:
            Dict: The AI's response.

        Raises:
            Exception: If there's an error in making the API call after trying all models.
        """
        models_to_try = ["azure", "bedrock"]
        while models_to_try:
            model = self._get_next_model()
            if model not in models_to_try:
                continue
            models_to_try.remove(model)
            
            try:
                common_params = {
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }

                if top_p != 0:
                    common_params["top_p"] = top_p

                if model == "bedrock":
                    common_params["model"] = "anthropic.claude-3-5-sonnet-20240620-v1:0"

                logger.info(f"Attempting to use {model} model")
                completion = self.portkey_clients[model].chat.completions.create(**common_params)
                self._update_stats(success=True)
                logger.info(f"Successfully received response from {model} model.")
                return completion
            except Exception as e:
                self._update_stats(success=False)
                logger.warning(f"Error in prompting {model} model: {str(e)}. Trying next model.")
                if "Invalid bedrock provider" in str(e) and model == "bedrock":
                    logger.error("Bedrock configuration error detected. Removing Bedrock from available models.")
                    self.models.remove("bedrock")
                    del self.model_usage["bedrock"]
                    del self.error_counts["bedrock"]
        
        # If we've exhausted all models
        raise Exception("All models failed to respond.")

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        """
        Sends messages to the AI model and receives responses in a streaming fashion with load balancing.

        Args:
            messages (List[Dict[str, str]]): The messages or prompts to send to the AI.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 4096.
            temperature (float): The randomness of the response. Defaults to 0.2.
            top_p (float): The nucleus sampling rate. Defaults to 0.

        Returns:
            str: The AI's response as a concatenated string.

        Raises:
            Exception: If there's an error in making the API call after trying all models.
        """
        models_to_try = ["azure", "bedrock", "gemini"]
        while models_to_try:
            current_model = self._get_next_model()
            if current_model not in models_to_try:
                continue
            models_to_try.remove(current_model)
            
            try:
                common_params = {
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True
                }

                if top_p != 0:
                    common_params["top_p"] = top_p

                if current_model == "bedrock":
                    common_params["model"] = "anthropic.claude-3-5-sonnet-20240620-v1:0"
                elif current_model == "gemini":
                    common_params["model"] = "gemini-1.5-pro"

                logger.info(f"Attempting to use {current_model} model for streaming")
                chat_completion_stream = self.portkey_clients[current_model].chat.completions.create(**common_params)
                logger.info(f"Successfully received streaming response from {current_model} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        final_response += content

                print()  # Print a new line after streaming
                self._update_stats(success=True)
                logger.info(f"Completed streaming from {current_model} model.")
                return final_response
            except Exception as e:
                self._update_stats(success=False)
                logger.warning(f"Error in streaming prompt from {current_model} model: {str(e)}. Trying next model.")
                if "Invalid bedrock provider" in str(e) and current_model == "bedrock":
                    logger.error("Bedrock configuration error detected. Removing Bedrock from available models.")
                    self.models.remove("bedrock")
                    del self.model_usage["bedrock"]
                    del self.error_counts["bedrock"]
        
        # If we've exhausted all models
        raise Exception("All models failed to respond in streaming mode.")

    def generate_image(self, prompt: str, size: str = "1024x1024"):
        """
        Generates an image using the DALL-E 3 model.

        Args:
            prompt (str): The text prompt for image generation.
            size (str): The size of the image to generate. Defaults to "1024x1024".

        Returns:
            The generated image.

        Raises:
            Exception: If there's an error in generating the image.
        """
        try:
            logger.info("Attempting to generate image with DALL-E 3")
            image = self.portkey_clients["dalle3"].images.generate(
                prompt=prompt,
                size=size
            )
            logger.info("Successfully generated image with DALL-E 3")
            return image
        except Exception as e:
            logger.error(f"Error in generating image with DALL-E 3: {str(e)}")
            raise
