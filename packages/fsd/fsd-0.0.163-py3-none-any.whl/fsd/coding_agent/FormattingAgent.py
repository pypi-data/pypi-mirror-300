import os
import aiohttp
import asyncio
import json
import sys
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)
from fsd.util.portkey import AIGateway
from fsd.system.FileContentManager import FileContentManager

class FormattingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.conversation_history = []
        self.max_tokens = 4096
        self.ai = AIGateway()
        self.code_manager = FileContentManager()  # Initialize CodeManager in the constructor

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def initial_setup(self, user_prompt, role):
        """
        Initialize the conversation with a prompt for the assistant.

        Args:
            user_prompt (str): The user's prompt to initiate the conversation.
        """
        prompt = f"""You are a senior {role} working as a formatting agent. You will receive detailed instructions to work on. Follow these guidelines strictly:
                1. For ALL code changes, additions, or deletions, you MUST ALWAYS use the following *SEARCH/REPLACE block* format:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. Ensure that the SEARCH section exactly matches the existing code, including whitespace and comments.

                4. For large files, focus on the relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. For complex changes or large files, break them into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of the SEARCH/REPLACE block format. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a user's request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.
        """

        self.conversation_history.append({"role": "system", "content": prompt})
        self.conversation_history.append({"role": "user", "content": f"Cool, this is user request: {user_prompt}"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! I will follow exactly and respond ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed"})

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.debug(f"\n #### The `FormattingAgent` has detected that the file does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### The `FormattingAgent` encountered an error while reading `{file_path}` with `{encoding}` encoding: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### The `FormattingAgent` failed to read `{file_path}` in binary mode: `{e}`")

        return ""

    async def get_format(self, file):
        """
        Request code reformatting from Azure OpenAI API for a given file.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            file (str): Path to the file to be reformatted.

        Returns:
            str: Reformatted code or error reason.
        """
        file_content = self.read_file_content(file)
        if file_content:
            # Prepare payload for the API request
            prompt = f"Now work on this file, please follow exactly user's request. Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed: {file_content}"

            self.conversation_history.append({"role": "user", "content": prompt})

            try:
                logger.info(f"\n #### The `FormattingAgent` is initiating the code reformatting process for `{file}`")
                response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
                logger.debug(f"\n #### The `FormattingAgent` has successfully completed the code reformatting for `{file}`")
                return response.choices[0].message.content
            except Exception as e:
                logger.debug(f"\n #### The `FormattingAgent` encountered an error during the reformatting process: `{e}`")
                return {
                    "reason": str(e)
                }


    async def replace_all_code_in_file(self, file_path, result):
        """
        Replace the entire content of a file with the new code snippet.

        Args:
            file_path (str): Path to the file.
            new_code_snippet (str): New code to replace the current content.
        """
        if file_path:
            logger.debug(f"\n #### The `FormattingAgent` is initiating the process to replace the content of `{file_path}`")
            await self.code_manager.handle_coding_agent_response(file_path, result)
            logger.debug(f"\n #### The `FormattingAgent` has successfully replaced the content of `{file_path}`")
        else:
            logger.debug(f"\n #### The `FormattingAgent` could not locate the file: `{file_path}`")


    async def get_formats(self, files, prompt, role):
        """
        Format the content of all provided files using Azure OpenAI API.

        Args:
            files (list): List of file paths to be formatted.
            prompt (str): The user's prompt to initiate the formatting request.
        """
        # Step to remove all empty files from the list
        files = [file for file in files if file]

        file_paths = files
        self.initial_setup(prompt, role)
        for file in file_paths:
            logger.info(f"\n #### The `FormattingAgent` is beginning the formatting process for `{file}`")
            result = await self.get_format(file)
            if result:
                await self.replace_all_code_in_file(file, result)
                logger.debug(f"\n #### The `FormattingAgent` has successfully completed the formatting for `{file}`")
