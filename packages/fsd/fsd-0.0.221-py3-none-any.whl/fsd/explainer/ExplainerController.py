import os
import json
import asyncio
from .ExplainablePrePromptAgent import ExplainablePrePromptAgent
from .GeneralExplainerAgent import GeneralExplainerAgent
from .ExplainableFileFinderAgent import ExplainableFileFinderAgent
from .MainExplainerAgent import MainExplainerAgent
from fsd.util import utils
import sys
import subprocess
import re
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ExplainerController:

    def __init__(self, repo):
        self.repo = repo
        self.preprompt = ExplainablePrePromptAgent(repo)
        self.normalExplainer = GeneralExplainerAgent(repo)
        self.mainExplainer = MainExplainerAgent(repo)
        self.fileFinder = ExplainableFileFinderAgent(repo)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)

    async def get_normal_answer(self, user_prompt, language, role):
        """Generate idea plans based on user prompt and available files."""
        return await self.normalExplainer.get_normal_answer_plans(user_prompt, language, role)

    async def get_file_answer(self, user_prompt, language, files, role):
        """Generate idea plans based on user prompt and available files."""
        return await self.mainExplainer.get_answer_plans(user_prompt, language, files, role)

    async def get_explaining_files(self, prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileFinder.get_file_plannings(prompt)

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.debug(f"\n #### File does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### Attempt to read file `{file_path}` with `{encoding}` encoding failed: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### Binary read attempt for file `{file_path}` failed: `{e}`")

        return ""

    async def get_started(self, user_prompt):
        logger.info("\n #### The `Director Support Agent` will now begin processing your request.")
        logger.info("\n-------------------------------------------------")

        prePrompt = await self.get_prePrompt(user_prompt)
        finalPrompt = prePrompt['processed_prompt']
        pipeline = prePrompt['pipeline']
        language = prePrompt['original_prompt_language']
        role = prePrompt['role']

        if pipeline == "1":
            logger.debug("\n #### The `File Finder Agent` is currently embarking on a quest to locate relevant files.")
            file_result = await self.get_explaining_files(finalPrompt)
            working_files = file_result.get('working_files', [])
            await self.get_file_answer(finalPrompt, language, working_files, role)
        elif pipeline == "2":
            logger.debug("\n #### The `General Explainer Agent` is presently engaged in processing your query and formulating a comprehensive response.")
            await self.get_normal_answer(finalPrompt, language, role)

        logger.info("\n\n-------------------------------------------------")
