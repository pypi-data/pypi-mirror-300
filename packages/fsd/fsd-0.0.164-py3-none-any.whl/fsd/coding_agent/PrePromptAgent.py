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

class PrePromptAgent:
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
            logger.debug(f"The `PrePromptAgent` has detected that the file `{file_path}` does not exist")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"The `PrePromptAgent` encountered an error while reading file `{file_path}` with `{encoding}` encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"The `PrePromptAgent` failed to read file `{file_path}` in binary mode: {e}")

        return ""

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    "As a senior prompt engineer, analyze the project files and user prompt. Respond in JSON format:\n\n"
                    "role: Choose a specific engineer role best suited for the task.\n"
                    "processed_prompt: Translate non-English prompts, correct grammar, and provide a clear, concise version based on project insights. Exclude any mentions or questions about the AI model being used.\n"
                    "pipeline: Choose the most appropriate pipeline (1-8) based on these guidelines:\n"
                    "1. Run/compile, fix compile errors, open project\n"
                    "2. Create/add files or folders\n"
                    "3. Move files or folders\n"
                    "4. Format code, refactor, write comments\n"
                    "5. Main coding request, complex tasks, bug fixes, new features (requires development plan)\n"
                    "6. Install dependencies\n"
                    "7. Deployment\n"
                    "8. Generate images\n"
                    "original_prompt_language: If the user specifies a language to respond in, use that. Otherwise, detect the language of the user's prompt.\n"
                    "JSON format:\n"
                    "{\n"
                    '    "processed_prompt": "",\n'
                    '    "role": "",\n'
                    '    "pipeline": "1-8",\n'
                    '    "original_prompt_language": ""\n'
                    "}\n"
                    "Provide only valid JSON without additional text."
                )
            },
            {
                "role": "user",
                "content": f"User prompt:\n{user_prompt}\n\nProject structure:\n{all_file_contents}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.debug(f"The `PrePromptAgent` encountered an error during plan generation: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.debug(f"The `PrePromptAgent` has successfully completed preparing for the user prompt: {user_prompt}")
        return plan
