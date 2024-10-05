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

class CompilePrePromptAgent:
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
            logger.debug(f"\n #### The `CompilePrePromptAgent` encountered a non-existent file: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### The `CompilePrePromptAgent` failed to read file `{file_path}` with `{encoding}` encoding: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### The `CompilePrePromptAgent` failed to read file `{file_path}` in binary mode: `{e}`")

        return ""

    async def get_prePrompt_plan(self, all_file_contents, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You're an image generation specialist. Process requests for only PNG, JPG, JPEG formats only, excluding SVG. Respond in JSON:\n\n"
                    "processed_prompt: For supported formats, extract:\n"
                    "- Save path\n"
                    "- Name\n"
                    "- Dimension\n"
                    "- Description\n"
                    "Combine all image details into one string, separated by newlines. Translate non-English prompts. NO YAPPING OR UNNECESSARY EXPLANATIONS.\n"
                    "pipeline: \"0\" for unsupported/no request, \"1\" for supported.\n\n"
                    "JSON structure:\n"
                    "{\n"
                    '    "processed_prompt": "Path: [path], Name: [name], Dimension: [WxH], Description: [desc]\n..." (only if pipeline is "1", otherwise ""),\n'
                    '    "pipeline": "0" or "1"\n'
                    "}\n\n"
                    "Strict JSON only. Any unsupported format (including SVG) mention results in pipeline \"0\" and empty processed_prompt. STRICTLY ENFORCE no yapping in the response."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{all_file_contents}\n\nDirective:\n{user_prompt}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.debug(f"\n #### The `CompilePrePromptAgent` encountered an error: `{e}`")
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
        logger.debug("\n #### The `CompilePrePromptAgent` is initiating the pre-prompt planning process")
        all_file_contents = self.repo.print_summarize_with_tree()
        plan = await self.get_prePrompt_plan(all_file_contents, user_prompt)
        logger.debug(f"\n #### The `CompilePrePromptAgent` has completed the pre-prompt planning: `{plan}`")
        return plan
