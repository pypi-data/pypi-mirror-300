import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ImageCheckSpecialAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_image_check_plan(self, user_prompt, original_prompt_language):
        """
        Get an image check plan from Azure OpenAI based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.
            original_prompt_language (str): The language to use for the response.

        Returns:
            dict: Image check plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    f"Analyze the user's request for ONLY PNG, JPG, JPEG, or .ico images. For each image mentioned, extract and return the following details:\n"
                    "- Save path (use the exact path mentioned in the user instruction)\n"
                    "- Name\n"
                    "- Dimension\n"
                    "- Description\n"
                    "Exclude all other types of assets. Respond only with the extracted image details.\n"
                    "Return a nicely formatted response. Use appropriate spacing to ensure the text is clear and easy to read. "
                    "Use clear headings (maximum size #### for h4) to organize your response. "
                    "Utilize markdown for highlighting important points where necessary.\n"
                    f"Provide the response in the following language: {original_prompt_language}"
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        response = await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
        return response

    async def get_image_check_plans(self, user_prompt, original_prompt_language):
        """
        Get image check plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image check plan or error reason.
        """
        logger.debug(f"\n #### The `ImageCheckSpecialAgent` is initiating the image check plan generation\n User prompt: {user_prompt}")
        plan = await self.get_image_check_plan(user_prompt, original_prompt_language)
        logger.debug(f"\n #### The `ImageCheckSpecialAgent` has completed generating the image check plan")
        return plan
