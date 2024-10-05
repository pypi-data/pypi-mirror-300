import os
import sys
import json
import subprocess
import asyncio
import re

from .ImagePrePromptAgent import CompilePrePromptAgent
from .ImageTaskPlanner import ImageTaskPlanner
from .ImageFileFinderAgent import ImageFileFinderAgent
from .ImageAnalysAgent import ImageAnalysAgent
from .ImageGenAgent import ImageGenAgent
from .ImageCheckAgent import ImageCheckAgent
from .ImageCheckSpecialAgent import ImageCheckSpecialAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ImageControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.preprompt = CompilePrePromptAgent(repo)
        self.lang = LanguageAgent(repo)
        self.fileFinder = ImageFileFinderAgent(repo)
        self.analysAgent = ImageAnalysAgent(repo)
        self.taskPlanner = ImageTaskPlanner(repo)
        self.imageGenAgent = ImageGenAgent(repo)
        self.imageCheckAgent = ImageCheckAgent(repo)
        self.imageCheckSpecialAgent = ImageCheckSpecialAgent(repo)

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

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def start_image_process(self, instruction):

        logger.info("\n #### Image generation needed. Click `Approve` to proceed or `Skip` to cancel.")
        logger.info(f" \n ### Press a or Approve to execute this step, or Enter to skip: ")
        user_permission = input()
        user_prompt, _ = parse_payload(user_permission)
        user_prompt = user_prompt.lower()
        
        if user_prompt != "a":
            logger.info("\n #### The `Image Generation Agent` has skipped as per user request")
            return
        
        logger.info("\n #### `Image Analysis Agent` is finding relevant style content")
        
        file_result = await self.fileFinder.get_style_file_plannings()

        style_files = file_result.get('style_files', [])

        self.analysAgent.initial_setup(style_files)

        logger.info("\n #### `Image Analysis Agent` is preparing an initial image plan for clarification")

        idea_plan = await self.analysAgent.get_idea_plans(instruction)

        while True:

            logger.info("\n #### The `Image Analysis Agent` is requesting feedback. Click `Yes` if you feel satisfied, or type your feedback below.")

            logger.info(
                "\n #### Are you satisfied with this plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

            user_prompt_json = input()
            user_prompt, _ = parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info(f"\n #### `Image Analysis Agent` is updating the image plan based on user feedback")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)

        self.analysAgent.clear_conversation_history()

        logger.info(f"\n #### `Image Task Planner` is organizing and preparing the task ")
        task = await self.taskPlanner.get_task_plan(idea_plan)
        await self.imageGenAgent.generate_images(task)
        logger.info(f"\n #### Image generation process completed.")


    async def process_creation(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_creating'):
            processes = data.get('Adding_new_files', [])
            await self.project.execute_files_creation(processes)


    async def get_started(self, user_prompt, original_prompt_language):
        """Start the processing of the user prompt."""
        
        logger.debug("\n #### Image generation agent initialized and ready to process image requests")

        prePrompt = await self.get_prePrompt(user_prompt)
        pipeline = prePrompt['pipeline']

        if pipeline == "0":
            print(user_prompt)
        elif pipeline == "1":
            finalPrompt = prePrompt['processed_prompt']
            await self.start_image_process(finalPrompt)

        logger.debug(f"\n #### Image generation process completed!")


    async def get_started_coding(self, user_prompt, original_prompt_language):
        """Start the processing of the user prompt."""
        
        logger.debug("\n #### Image generation agent initialized and ready to process image requests")

        result = await self.imageCheckAgent.get_image_check_plans(user_prompt)
        result = result['result']

        if result == "0":
            logger.info()
        elif result == "1":
            finalPrompt = await self.imageCheckSpecialAgent.get_image_check_plans(user_prompt)
            await self.start_image_process(finalPrompt)

        logger.debug(f"\n #### Image generation process completed!")
