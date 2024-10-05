import os
import aiohttp
import asyncio
import json
import sys

from json_repair import repair_json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class DependencyGuiderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def initial_setup(self, user_prompt):
        """Initialize the setup with the provided instructions and context."""
        # Step to remove all empty files from the list
        logger.debug("\n #### Initializing setup for `DependencyGuiderAgent`")

        all_file_contents = self.repo.print_tree()

        prompt = (
            "As a DevOps expert, analyze the project files and user prompt. Respond in JSON format:\n\n"
            "processed_prompt: Clarify and enhance the user's prompt. Translate if needed. Include project insights and strategies.\n"
            "pipeline: Choose 0 (no action), 1 (expert intervention needed), or 2 (automated resolution possible) for dependency management.\n"
            "explainer: For pipeline 1, explain why automation is impossible and provide manual steps. Use the user's language.\n\n"
            "Strict JSON structure:\n"
            "{\n"
            '    "processed_prompt": "Enhanced user directive",\n'
            '    "pipeline": "0, 1, or 2",\n'
            '    "explainer": "Technical rationale and guidance"\n'
            "}\n\n"
            f"Project context:\n{all_file_contents}\n"
        )

        self.conversation_history.append({"role": "system", "content": prompt})
        self.conversation_history.append({"role": "user", "content": f"{user_prompt}"})
        logger.debug("\n #### Setup completed for `DependencyGuiderAgent`")

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.debug("\n #### Clearing conversation history for `DependencyGuiderAgent`")
        self.conversation_history = []

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        logger.debug(f"\n #### `DependencyGuiderAgent` is attempting to read file: {file_path}")
        if not os.path.exists(file_path):
            logger.debug(f"\n #### `DependencyGuiderAgent`: File does not exist: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    logger.debug(f"\n #### `DependencyGuiderAgent` successfully read file: {file_path}")
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### `DependencyGuiderAgent`: Failed to read file {file_path} with {encoding} encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                logger.debug(f"\n #### `DependencyGuiderAgent` successfully read file in binary mode: {file_path}")
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### `DependencyGuiderAgent`: Failed to read file {file_path} in binary mode: {e}")

        return ""

    async def get_guider_plan(self, user_prompt):
        logger.debug("\n #### `DependencyGuiderAgent` is generating a guider plan")
        self.conversation_history.append({"role": "user", "content": f"{user_prompt}"})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            self.conversation_history.append({"role": "assistant", "content": f"{response.choices[0].message.content}"})
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### `DependencyGuiderAgent` successfully generated a guider plan")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### `DependencyGuiderAgent` encountered a JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### `DependencyGuiderAgent` successfully repaired and parsed JSON")
            return plan_json
        except Exception as e:
            logger.debug(f"\n #### `DependencyGuiderAgent` failed to generate plan: {e}")
            return {
                "reason": str(e)
            }

    async def get_guider_plans(self, user_prompt):
        logger.debug("\n #### `DependencyGuiderAgent` is processing user prompt for guider plans")
        plan = await self.get_guider_plan(user_prompt)
        logger.debug("\n #### `DependencyGuiderAgent` completed processing guider plans")
        return plan
