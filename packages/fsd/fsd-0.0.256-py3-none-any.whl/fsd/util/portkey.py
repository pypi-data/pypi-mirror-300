from portkey_ai import Portkey
from typing import Dict, List, Optional
import random
from collections import deque
import time
import asyncio

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
        self.model_queue = deque(["azure", "bedrock", "gemini"])
        self.model_usage = {"azure": 0, "bedrock": 0, "gemini": 0}
        self.model_errors = {"azure": 0, "bedrock": 0, "gemini": 0}
        self.model_latencies = {"azure": [], "bedrock": [], "gemini": []}
        self.last_reset_time = time.time()
        self.reset_interval = 3600  # Reset usage stats every hour
        self.error_threshold = 5  # Number of consecutive errors before temporary model exclusion
        self.excluded_models = set()
        self.exclusion_time = {}
        self.lock = asyncio.Lock()

    async def _get_balanced_model(self):
        """
        Selects a model type for load balancing using a smart approach considering usage, errors, and latency.

        Returns:
            str: The selected model type ("azure", "bedrock", or "gemini").
        """
        async with self.lock:
            current_time = time.time()
            if current_time - self.last_reset_time > self.reset_interval:
                await self._reset_stats()

            # Check for models to be re-included
            for model, exclude_time in list(self.exclusion_time.items()):
                if current_time - exclude_time > 300:  # 5 minutes cooldown
                    self.excluded_models.remove(model)
                    del self.exclusion_time[model]

            available_models = [m for m in self.model_queue if m not in self.excluded_models]
            if not available_models:
                logger.warning("All models are currently excluded. Resetting exclusions.")
                self.excluded_models.clear()
                self.exclusion_time.clear()
                available_models = list(self.model_queue)

            # Calculate a score for each model based on usage, errors, and average latency
            model_scores = {}
            for model in available_models:
                usage_score = 1 / (self.model_usage[model] + 1)
                error_score = 1 / (self.model_errors[model] + 1)
                avg_latency = sum(self.model_latencies[model]) / len(self.model_latencies[model]) if self.model_latencies[model] else 1
                latency_score = 1 / avg_latency
                model_scores[model] = usage_score * error_score * latency_score

            # Select the model with the highest score
            selected_model = max(model_scores, key=model_scores.get)
            
            # Update the queue to prioritize less used models
            self.model_queue.remove(selected_model)
            self.model_queue.appendleft(selected_model)

            self.model_usage[selected_model] += 1
            return selected_model

    async def _reset_stats(self):
        """
        Resets the usage, error, and latency statistics for all models and shuffles the model queue.
        """
        self.model_usage = {model: 0 for model in self.model_usage}
        self.model_errors = {model: 0 for model in self.model_errors}
        self.model_latencies = {model: [] for model in self.model_latencies}
        self.last_reset_time = time.time()
        self.model_queue = deque(random.sample(list(self.model_queue), len(self.model_queue)))
        self.excluded_models.clear()
        self.exclusion_time.clear()
        logger.info("Model statistics reset and queue shuffled.")

    async def _handle_model_error(self, model: str):
        """
        Handles errors for a specific model, potentially excluding it temporarily.
        """
        self.model_errors[model] += 1
        if self.model_errors[model] >= self.error_threshold:
            self.excluded_models.add(model)
            self.exclusion_time[model] = time.time()
            logger.warning(f"Model {model} temporarily excluded due to repeated errors.")

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        """
        Sends messages to a balanced AI model and receives responses.

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
        max_retries = 3
        for attempt in range(max_retries):
            try:
                selected_model = await self._get_balanced_model()
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

                start_time = time.time()
                completion = self.portkey.chat.completions.create(**common_params)
                end_time = time.time()

                latency = end_time - start_time
                self.model_latencies[selected_model].append(latency)
                if len(self.model_latencies[selected_model]) > 10:
                    self.model_latencies[selected_model].pop(0)

                return completion
            except Exception as e:
                logger.error(f"Error in prompting {selected_model} model: {str(e)}")
                await self._handle_model_error(selected_model)
                if attempt == max_retries - 1:
                    raise

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        """
        Sends messages to a balanced AI model and receives responses in a streaming fashion.

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
        max_retries = 3
        for attempt in range(max_retries):
            try:
                selected_model = await self._get_balanced_model()
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

                start_time = time.time()
                chat_completion_stream = self.portkey.chat.completions.create(**common_params)
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        final_response += content

                end_time = time.time()
                latency = end_time - start_time
                self.model_latencies[selected_model].append(latency)
                if len(self.model_latencies[selected_model]) > 10:
                    self.model_latencies[selected_model].pop(0)

                print()  # Print a new line after streaming
                return final_response
            except Exception as e:
                logger.error(f"Error in streaming prompt from {selected_model} model: {str(e)}")
                await self._handle_model_error(selected_model)
                if attempt == max_retries - 1:
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
