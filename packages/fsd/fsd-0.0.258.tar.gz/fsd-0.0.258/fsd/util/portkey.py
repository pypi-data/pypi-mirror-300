from portkey_ai import Portkey
from typing import Dict, List, Optional
import random
from collections import deque
from datetime import datetime, timedelta

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class AIGateway:
    """
    A gateway for interfacing with various AI models provided by Portkey.

    This class provides an abstraction layer over different AI model types,
    allowing for seamless interaction with Azure, Bedrock, and Google Gemini models.

    Attributes:
        portkey_clients (Dict[str, Portkey]): Dictionary of Portkey clients for each model type.
    """

    # Constants for API configuration
    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    # Mapping of model types to their respective virtual keys
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure": "azure-7e4746",
        "bedrock": "bedrock-bfa916",
        "gemini": "gemini-b5d385"
    }

    def __init__(self):
        """
        Initializes the AIGateway with load balancing capabilities for multiple AI models.
        """
        self.model_types = list(self.VIRTUAL_KEYS.keys())
        self.portkey_clients = {
            model_type: Portkey(
                api_key=self.API_KEY,
                virtual_key=self.VIRTUAL_KEYS[model_type],
                config=self.CONFIG_ID
            ) for model_type in self.model_types
        }
        self.usage_counts = {model_type: 0 for model_type in self.model_types}
        self.error_counts = {model_type: 0 for model_type in self.model_types}
        self.success_counts = {model_type: 0 for model_type in self.model_types}
        self.last_reset_time = datetime.now()
        self.cooldown_until = {model_type: None for model_type in self.model_types}
        self.usage_history = deque(maxlen=100)  # Store last 100 usages
        self.error_threshold = 5  # Number of consecutive errors before cooldown
        self.cooldown_duration = timedelta(minutes=5)  # Cooldown duration after errors

    def _select_model(self):
        """
        Selects the next model to use based on usage history, error rates, and success rates.
        """
        now = datetime.now()
        
        # Reset counts every hour
        if now - self.last_reset_time > timedelta(hours=1):
            self.usage_counts = {model_type: 0 for model_type in self.model_types}
            self.error_counts = {model_type: 0 for model_type in self.model_types}
            self.success_counts = {model_type: 0 for model_type in self.model_types}
            self.last_reset_time = now

        # Filter out models in cooldown
        available_models = [model for model in self.model_types if not self.cooldown_until.get(model) or now > self.cooldown_until[model]]

        if not available_models:
            raise ValueError("All models are currently in cooldown. Please try again later.")

        # Calculate a score for each model (higher is better)
        scores = {}
        for model in available_models:
            usage_score = 1 / (self.usage_counts[model] + 1)  # Favor less used models
            error_score = 1 / (self.error_counts[model] + 1)  # Penalize models with more errors
            success_score = (self.success_counts[model] + 1) / (self.usage_counts[model] + 1)  # Favor models with higher success rates
            recent_usage = sum(1 for m in self.usage_history if m == model)
            recency_score = 1 / (recent_usage + 1)  # Favor models used less recently
            scores[model] = usage_score * error_score * success_score * recency_score

        # Select the model with the highest score
        selected_model = max(scores, key=scores.get)
        
        self.usage_counts[selected_model] += 1
        self.usage_history.append(selected_model)
        return selected_model

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        """
        Sends messages to the AI model and receives responses.

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
                selected_model = self._select_model()
                portkey_client = self.portkey_clients[selected_model]

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

                completion = portkey_client.chat.completions.create(**common_params)
                self.success_counts[selected_model] += 1
                self.error_counts[selected_model] = 0  # Reset error count on success
                logger.debug(f"Successfully received response from {selected_model} model")
                return completion

            except Exception as e:
                self.error_counts[selected_model] += 1
                logger.error(f"Error in prompting {selected_model} model: {str(e)}")

                if self.error_counts[selected_model] >= self.error_threshold:
                    self.cooldown_until[selected_model] = datetime.now() + self.cooldown_duration
                    logger.warning(f"{selected_model} model put in cooldown due to repeated errors")

                if attempt == max_retries - 1:
                    raise  # Raise the last exception if all retries failed

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        """
        Sends messages to the AI model and receives responses in a streaming fashion.

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
                selected_model = self._select_model()
                portkey_client = self.portkey_clients[selected_model]

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

                chat_completion_stream = portkey_client.chat.completions.create(**common_params)
                logger.debug(f"Successfully started streaming response from {selected_model} model")

                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        final_response += content

                print()  # Print a new line after streaming
                self.success_counts[selected_model] += 1
                self.error_counts[selected_model] = 0  # Reset error count on success
                return final_response

            except Exception as e:
                self.error_counts[selected_model] += 1
                logger.error(f"Error in streaming prompt from {selected_model} model: {str(e)}")

                if self.error_counts[selected_model] >= self.error_threshold:
                    self.cooldown_until[selected_model] = datetime.now() + self.cooldown_duration
                    logger.warning(f"{selected_model} model put in cooldown due to repeated errors")

                if attempt == max_retries - 1:
                    raise  # Raise the last exception if all retries failed

    

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

