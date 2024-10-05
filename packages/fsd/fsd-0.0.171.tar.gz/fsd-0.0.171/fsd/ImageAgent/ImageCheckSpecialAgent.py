import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
logger = get_logger(__name__)

class ImageCheckSpecialAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including image files.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.debug(f"\n #### The `ImageCheckSpecialAgent` is reporting: File does not exist\n File path: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### The `ImageCheckSpecialAgent` encountered an issue:\n Failed to read file with {encoding} encoding\n File path: {file_path}\n Error: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### The `ImageCheckSpecialAgent` encountered an issue:\n Failed to read file in binary mode\n File path: {file_path}\n Error: {e}")

        return ""

    async def get_image_check_plan(self, user_prompt):
        """
        Get an image check plan from Azure OpenAI based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image check plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "Analyze the user's request for ONLY PNG, JPG, or JPEG images. For each image mentioned, extract and return the following details:\n"
                    "- Save path (use the exact path mentioned in the user instruction)\n"
                    "- Name\n"
                    "- Dimension\n"
                    "- Description\n"
                    "Exclude all other types of assets such as svg. Respond only with the extracted image details.\n"
                    "Return a nicely formatted response. Use appropriate spacing to ensure the text is clear and easy to read. "
                    "Use clear headings (maximum size #### for h4) to organize your response. "
                    "Utilize markdown for highlighting important points where necessary."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        response = await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
        return response

    async def get_image_check_plans(self, user_prompt):
        """
        Get image check plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image check plan or error reason.
        """
        logger.debug(f"\n #### The `ImageCheckSpecialAgent` is initiating the image check plan generation\n User prompt: {user_prompt}")
        plan = await self.get_image_check_plan(user_prompt)
        logger.debug(f"\n #### The `ImageCheckSpecialAgent` has completed generating the image check plan")
        return plan
