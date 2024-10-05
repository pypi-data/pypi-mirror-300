import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ImageAnalysAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')
        self.project_path = self.repo.get_repo_path()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, style_files):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        style_files_path = style_files

        if style_files:
            for file_path in style_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"UI/UX designer for image analysis. Analyze files, describe images. FOLLOW:\n\n"
            f"1. Start: `cd {self.project_path}`\n"
            "2. Analyze style files\n"
            "3. Extract theme elements\n"
            "4. Determine image sizes\n"
            "5. Identify backgrounds\n"
            "6. Analyze existing images\n"
            "7. Describe images matching style\n"
            "8. Adapt to theme and sizes (1024x1024, 1792x1024, 1024x1792)\n"
            f"9. ALWAYS provide FULL PATH within `{self.project_path}` to save each image\n"
            "10. Support PNG, JPG, JPEG only\n\n"
            "Focus on analysis and description. No code changes.\n\n"
            "Use exact paths. Follow requirements strictly.\n\n"
            "Organize with clear headings (max ####) and spacing."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.info(f"\n #### The `ImageAnalysAgent` reports: File does not exist\n File path: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### The `ImageAnalysAgent` encountered an issue while reading a file\n File: {file_path}\n Encoding: {encoding}\n Error: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### The `ImageAnalysAgent` failed to read a file in binary mode\n File: {file_path}\n Error: {e}")

        return ""

    async def get_idea_plan(self, user_prompt):
        prompt = (
            f"Follow the user prompt strictly and provide a no code response:\n{user_prompt}\n\n"
            f"Return a nicely formatted response. Use appropriate spacing to ensure the text is clear and easy to read. "
            f"Use clear headings (maximum size #### for h4) to organize your response. "
            f"Utilize markdown for highlighting important points where necessary."
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            logger.debug("\n #### The `ImageAnalysAgent` is initiating the AI prompt for idea generation")
            response = await self.ai.stream_prompt(self.conversation_history, self.max_tokens, 0, 0)
            logger.debug("\n #### The `ImageAnalysAgent` has successfully received the AI response")
            return response
        except Exception as e:
            logger.error(f"\n #### The `ImageAnalysAgent` encountered an error during idea generation\n Error: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt):
        logger.debug("\n #### The `ImageAnalysAgent` is beginning the process of generating idea plans")
        plan = await self.get_idea_plan(user_prompt)
        logger.debug("\n #### The `ImageAnalysAgent` has completed generating idea plans")
        return plan
