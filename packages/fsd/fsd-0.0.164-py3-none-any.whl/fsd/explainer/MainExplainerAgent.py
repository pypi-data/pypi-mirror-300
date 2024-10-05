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

class MainExplainerAgent:
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
            logger.debug(f"\n #### `File Manager Agent`: File does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### `File Manager Agent`: Attempt to read file `{file_path}` with `{encoding}` encoding failed: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### `File Manager Agent`: Binary read attempt for file `{file_path}` failed: `{e}`")

        return ""

    def read_all_file_content(self, all_path):
        all_context = ""

        for path in all_path:
            file_context = self.read_file_content(path)
            all_context += f"\n\nFile: {path}\n{file_context}"

        return all_context

    async def get_answer_plan(self, user_prompt, language, all_file_content, role):
        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Zinley.\n\n"
                    "Instructions:\n"
                    "1. If no context is provided, inform the user that no relevant files were found.\n"
                    "2. Provide a brief, concise guide on how to proceed or find relevant information.\n"
                    "3. Format your response for clarity and readability:\n"
                    "   - Use appropriate spacing\n"
                    "   - Ensure text is not crowded\n"
                    "   - Avoid weird symbols, unnecessary text, or distracting patterns\n"
                    "4. Use clear headings (no larger than h4) to organize information.\n"
                    "5. Keep the response short and to the point, avoiding unnecessary elaboration.\n"
                    "6. Respond in the language specified in the request.\n"
                    "7. If asked about the AI model you are using, mention that you are using a model configured by the Zinley team.\n"
                    "8. For any bash commands, use the following format:\n"
                    "   ```bash\n"
                    "   command here\n"
                    "   ```\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{all_file_content}\n\n"
                    f"User prompt:\n{user_prompt}\n\n"
                    f"You must respond in this language:\n{language}\n\n"
                )
            }
        ]

        try:
            logger.info(f"\n #### The `{role}` is in charge\n")
            await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
            return ""
        except Exception as e:
            logger.info(f"\n #### The `Technical Support Agent` encountered some errors\n")
            return {
                "reason": str(e)
            }


    async def get_answer_plans(self, user_prompt, language, files, role):
        files = [file for file in files if file]

        all_path = files
        logger.debug("\n #### `File Aggregator Agent`: Commencing file content aggregation for analysis")
        all_file_content = self.read_all_file_content(all_path)

        logger.debug("\n #### `Answer Plan Generator`: Initiating answer plan generation based on user input")
        plan = await self.get_answer_plan(user_prompt, language, all_file_content, role)
        return plan
