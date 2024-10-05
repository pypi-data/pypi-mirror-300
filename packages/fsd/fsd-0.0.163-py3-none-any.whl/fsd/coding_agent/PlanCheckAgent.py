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

class PlanCheckAgent:
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
            logger.debug(f"\n #### The `DependencyCheckAgent` has detected that the file does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### The `DependencyCheckAgent` encountered an error while reading `{file_path}` with `{encoding}` encoding: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### The `DependencyCheckAgent` failed to read `{file_path}` in binary mode: `{e}`")

        return ""

    async def get_idea_check_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_summarize_with_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    f"Analyze the user request and provided context to determine the appropriate plan. "
                    f"Plan 1 is for comprehensive work requiring extensive setup, significant involvement, and substantial dependency setup. This typically involves more than 10 files or brand new projects, aiming for large-scale setup, module setup, and comprehensive configuration. "
                    f"Plan 2 is for regular, more focused tasks aiming for efficiency. "
                    f"Based on your analysis, respond with either '1' or '2' in this exact JSON format:\n"
                    f"{{\n"
                    f'    "result": "1" or "2"\n'
                    f"}}\n\n"
                    f"Project structure and file summaries:\n{all_file_contents}"
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        try:
            logger.debug("\n #### The `DependencyCheckAgent` is initiating a request to the AI Gateway")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `DependencyCheckAgent` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `DependencyCheckAgent` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `DependencyCheckAgent` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.debug(f"\n #### The `DependencyCheckAgent` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_idea_check_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `DependencyCheckAgent` is beginning to retrieve dependency check plans")
        plan = await self.get_idea_check_plan(user_prompt)
        logger.debug("\n #### The `DependencyCheckAgent` has successfully retrieved dependency check plans")
        return plan
