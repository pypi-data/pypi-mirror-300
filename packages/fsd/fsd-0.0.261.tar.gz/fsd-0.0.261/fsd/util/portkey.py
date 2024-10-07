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
    allowing for seamless interaction with Azure, Bedrock, Google Gemini, and DALL-E 3 models.

    Attributes:
        portkey_clients (Dict[str, Portkey]): Dictionary of Portkey clients for each model type.
        model_usage (Dict[str, int]): Tracks usage count for each model.
        error_counts (Dict[str, int]): Tracks error count for each model.
        last_reset (float): Timestamp of the last reset of usage and error statistics.
        model_latencies (Dict[str, List[float]]): Tracks recent latencies for each model.
        model_costs (Dict[str, float]): Tracks estimated costs for each model.
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
        Initializes the AIGateway with advanced load balancing capabilities for multiple AI models.
        """
        self.models = ["azure", "bedrock", "gemini"]  # Exclude DALL-E 3 from general text models
        self.portkey_clients = {model: Portkey(api_key=self.API_KEY, virtual_key=key, config=self.CONFIG_ID) 
                                for model, key in self.VIRTUAL_KEYS.items()}
        self.model_usage = {model: 0 for model in self.models}
        self.error_counts = {model: 0 for model in self.models}
        self.last_reset = time.time()
        self.reset_interval = 3600  # Reset stats every hour
        self.model_latencies = {model: [] for model in self.models}
        self.model_costs = {model: 0.0 for model in self.models}
        self.max_latency_history = 100  # Keep track of the last 100 latencies

    async def _get_next_model(self):
        """
        Selects the next model to use based on a weighted combination of factors.
        """
        self._check_reset()
        
        weighted_scores = {}
        for model in self.models:
            usage_score = self.model_usage[model]
            error_score = self.error_counts[model] * 10  # Errors are weighted more heavily
            latency_score = sum(self.model_latencies[model]) / len(self.model_latencies[model]) if self.model_latencies[model] else 0
            cost_score = self.model_costs[model] * 100  # Cost is an important factor
            
            # Combine scores (lower is better)
            weighted_scores[model] = usage_score + error_score + latency_score + cost_score
        
        # Select the model with the lowest weighted score
        selected_model = min(weighted_scores, key=weighted_scores.get)
        
        logger.info(f"Model scores: {weighted_scores}")
        logger.info(f"Selected model: {selected_model}")
        
        return selected_model

    def _check_reset(self):
        """
        Resets usage and error statistics if the reset interval has passed.
        """
        current_time = time.time()
        if current_time - self.last_reset > self.reset_interval:
            self.model_usage = {model: 0 for model in self.models}
            self.error_counts = {model: 0 for model in self.models}
            self.model_costs = {model: 0.0 for model in self.models}
            self.last_reset = current_time
            logger.info("Reset model usage, error statistics, and costs.")

    def _update_model_stats(self, model: str, latency: float, estimated_cost: float):
        """
        Updates the statistics for a given model after use.
        """
        self.model_usage[model] += 1
        self.model_latencies[model].append(latency)
        if len(self.model_latencies[model]) > self.max_latency_history:
            self.model_latencies[model].pop(0)
        self.model_costs[model] += estimated_cost

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        """
        Sends messages to the AI model and receives responses with advanced load balancing.
        """
        start_time = time.time()
        models_to_try = list(self.models)
        while models_to_try:
            model = await self._get_next_model()
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
                elif model == "gemini":
                    common_params["model"] = "gemini-1.5-pro"

                logger.info(f"Attempting to use {model} model")
                completion = await asyncio.to_thread(self.portkey_clients[model].chat.completions.create, **common_params)
                
                end_time = time.time()
                latency = end_time - start_time
                estimated_cost = self._estimate_cost(model, max_tokens)
                self._update_model_stats(model, latency, estimated_cost)
                
                logger.info(f"Successfully received response from {model} model. Latency: {latency:.2f}s, Estimated cost: ${estimated_cost:.4f}")
                return completion
            except Exception as e:
                self.error_counts[model] += 1
                logger.warning(f"Error in prompting {model} model: {str(e)}. Updated error count: {self.error_counts[model]}. Trying next model.")
                if "Invalid bedrock provider" in str(e) and model == "bedrock":
                    logger.error("Bedrock configuration error detected. Removing Bedrock from available models.")
                    self.models.remove("bedrock")
                    del self.model_usage["bedrock"]
                    del self.error_counts["bedrock"]
                    del self.model_latencies["bedrock"]
                    del self.model_costs["bedrock"]
        
        # If we've exhausted all models
        raise Exception("All models failed to respond.")

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        """
        Sends messages to the AI model and receives responses in a streaming fashion with advanced load balancing.
        """
        start_time = time.time()
        models_to_try = list(self.models)
        while models_to_try:
            model = await self._get_next_model()
            models_to_try.remove(model)
            
            try:
                common_params = {
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True
                }

                if top_p != 0:
                    common_params["top_p"] = top_p

                if model == "bedrock":
                    common_params["model"] = "anthropic.claude-3-5-sonnet-20240620-v1:0"
                elif model == "gemini":
                    common_params["model"] = "gemini-1.5-pro"

                logger.info(f"Attempting to use {model} model for streaming")
                chat_completion_stream = await asyncio.to_thread(self.portkey_clients[model].chat.completions.create, **common_params)
                logger.info(f"Successfully received streaming response from {model} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        final_response += content

                print()  # Print a new line after streaming
                end_time = time.time()
                latency = end_time - start_time
                estimated_cost = self._estimate_cost(model, max_tokens)
                self._update_model_stats(model, latency, estimated_cost)
                
                logger.info(f"Completed streaming from {model} model. Latency: {latency:.2f}s, Estimated cost: ${estimated_cost:.4f}")
                return final_response
            except Exception as e:
                self.error_counts[model] += 1
                logger.warning(f"Error in streaming prompt from {model} model: {str(e)}. Updated error count: {self.error_counts[model]}. Trying next model.")
                if "Invalid bedrock provider" in str(e) and model == "bedrock":
                    logger.error("Bedrock configuration error detected. Removing Bedrock from available models.")
                    self.models.remove("bedrock")
                    del self.model_usage["bedrock"]
                    del self.error_counts["bedrock"]
                    del self.model_latencies["bedrock"]
                    del self.model_costs["bedrock"]
        
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
