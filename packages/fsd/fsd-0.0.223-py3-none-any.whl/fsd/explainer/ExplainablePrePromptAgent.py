import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)
class ExplainablePrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.debug(f"\n #### The `ExplainablePrePromptAgent` is reporting:\n File does not exist\n File path: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### The `ExplainablePrePromptAgent` encountered an issue:\n While reading a file\n File: {file_path}\n Encoding: {encoding}\n Error: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### The `ExplainablePrePromptAgent` failed:\n To read a file in binary mode\n File: {file_path}\n Error: {e}")

        return ""

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """

        tree = self.repo.print_tree()
        
        messages = [
            {
                "role": "system",
                "content": (
                    "Analyze the user prompt and project structure to respond in JSON format:\n"
                    "original_prompt_language: If the user specifies a language to respond in, use that. Otherwise, detect the language of the user's prompt.\n"
                    "processed_prompt: If not in English, translate to English. Ensure it's clear and concise.\n"
                    "pipeline: Choose '1' if the user is asking about specific files, code, or project-related questions. Choose '2' for general, non-project-related questions.\n"
                    "role: Determine the most suitable role to answer this question (e.g., 'C++ Engineer', 'iOS Engineer', 'Poet', or any other appropriate agent role).\n"
                    "Format:\n"
                    "{\n"
                    '    "role": "",\n'
                    '    "processed_prompt": "",\n'
                    '    "original_prompt_language": "",\n'
                    '    "pipeline": "1 or 2"\n'
                    "}\n"
                    "Provide only valid JSON in your response."
                )
            },
            {
                "role": "user",
                "content": f"User prompt:\n{user_prompt}\n\nProject structure:\n{tree}"
            }
        ]

        try:
            logger.debug("\n #### The `ExplainablePrePromptAgent` is initiating:\n A request to the AI for pre-prompt planning")
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            logger.debug("\n #### The `ExplainablePrePromptAgent` has successfully:\n Received the AI response for pre-prompt planning")
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### The `ExplainablePrePromptAgent` is attempting:\n To repair a JSON decoding error in the AI response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"\n #### The `ExplainablePrePromptAgent` encountered an error:\n While getting the pre-prompt plan\n Error: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `ExplainablePrePromptAgent` is beginning:\n The pre-prompt planning process")
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.debug("\n #### The `ExplainablePrePromptAgent` has finished:\n The pre-prompt planning process")
        return plan
